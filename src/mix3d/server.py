"""Pannello MIX3D: server locale (solo libreria standard) + API JSON.

Avvio: `mix3d ui` e apri http://127.0.0.1:8730. Ascolta solo in locale.
Lo stato è un progetto JSON (piano, M11) salvabile e ricaricabile.
"""
from __future__ import annotations

import io
import json
import os
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import numpy as np
import soundfile as sf

from . import analysis, autotune, devices, eq, fusion, geometry, localize, look, media, mixer, spazi, splat

WEB = Path(__file__).parent / "web"
AUDIO_EXT = {".wav", ".bwf", ".mp4", ".mov", ".mxf", ".m4a", ".aac", ".mp3", ".flac", ".aif", ".aiff"}


def new_project() -> dict:
    return {"nome": "Concerto", "sr": 48000, "sala": {"w": 20.0, "d": 30.0, "h": 8.0},
            "listener": [0.0, 1.7, 8.0], "master_db": -6.0, "correzione": True,
            "attenuazione": 0.5, "dist_ref_m": 5.0, "larghezza": 1.0,
            "riferimento": None, "resolve": None, "spazio": None, "palco": {"w": 12, "d": 4, "h": 0.6},
            "sorgenti": [], "lobi": True, "tracks": []}


STATE = {"project": new_project(), "jobs": {}, "rev": 0, "poll": 0.0, "mix": 0, "host": None, "host_rel": False}


def host_time(h: float) -> float:
    """Posizione del plugin in Fairlight -> secondi MIX3D (0 = inizio timeline).
    L'host può contare dall'inizio della timeline o dal timecode (01:00:00:00): se una posizione
    cade prima del timecode d'inizio, l'host conta dall'inizio e così resta."""
    r = STATE["project"].get("resolve")
    if not r:
        return h
    z = r["start_frame"] / r["fps"]
    if h < z - 1:
        STATE["host_rel"] = True
    return h if STATE["host_rel"] else h - z
# timeline mandata dallo script MIX3D dentro Resolve (Workspace > Scripts > MIX3D)
SESSION = Path.home() / ".mix3d" / "resolve" / "sessione.json"
LOCK = threading.Lock()
WORKERS = max(1, min(4, (os.cpu_count() or 2) // 2))  # metà dei core: l'ascolto resta fluido


# --- tracce -----------------------------------------------------------------

def apply_profile(t: dict, pid: str):
    p = devices.profile(pid)
    t.update(profile=pid, registratore=p["registratore"], microfono=p["microfono"], posizione_tipica=p["posizione"],
             ruolo=p["ruolo"], mute=p["gain_db"] is None, gain_db=p["gain_db"] or 0.0)
    # profilo mono (es. audio macchina mono): solo il primo canale; gli altri profili tornano ai canali del file
    orig = t.setdefault("canali_file", t["channels"])
    t["channels"] = orig[:1] if p.get("mono") else orig


def tracks_from_file(path: str, offset_s: float = 0.0, name: str | None = None) -> list[dict]:
    info = media.probe(path)
    wav = path  # letto direttamente (WAV) o a pezzi con ffmpeg (video): nessuna copia decodificata
    n = info["channels"]
    groups = [[c] for c in range(1, n + 1)] if n == 1 else [[c, c + 1] if c < n else [c] for c in range(1, n + 1, 2)]
    out = []
    for ch in groups:
        sug = devices.suggest({**info, "ch_index": ch[0]})
        t = {"id": uuid.uuid4().hex[:8], "file": path, "wav": wav, "channels": ch, "info": info,
             "nome": f"{name or info['name']} ch{'-'.join(map(str, ch))}" if n > 2 else (name or info["name"]),
             "offset_s": offset_s, "drift_ppm": 0.0, "sync": None, "suggeriti": sug,
             "confermato": False, "solo": False, "pan": 0.0, "pos_mode": "auto", "pos": [0, 1.5, 3],
             "analisi": None}
        apply_profile(t, sug[0]["id"])
        if (hit := info.get("rilevato")) and t["registratore"] != hit["id"]:
            t["registratore"] = hit["id"]  # nessun profilo pronto: il registratore viene comunque dai metadati
        out.append(t)
    return out


def split_track(p: dict, tid: str) -> list[dict]:
    """Una traccia a due canali diventa due tracce mono (es. ch1 microfono, ch2 linea dal mixer)."""
    i, t = next((i, t) for i, t in enumerate(p["tracks"]) if t["id"] == tid)
    if t.get("destra"):  # era un doppio mono unito: torna com'era
        right = t.pop("destra")  # la traccia destra era conservata intera
        right.pop("delta_s", None)
        t["nome"] = t["nome"].split(" + ")[0]
        p["tracks"].insert(i + 1, right)
        return [t, right]
    if len(t["channels"]) < 2:
        raise ValueError("la traccia è già mono")
    base = t["nome"].rsplit(" ch", 1)[0]
    parts = [{**t, "id": t["id"] if k == 0 else uuid.uuid4().hex[:8], "channels": [c], "canali_file": [c], "nome": f"{base} ch{c}",
              "analisi": None, "sync": None} for k, c in enumerate(t["channels"])]
    p["tracks"][i:i + 1] = parts
    return parts


def join_tracks(p: dict, left_id: str, right_id: str) -> dict:
    """Due tracce mono diventano una stereo: la prima a sinistra, la seconda a destra
    (es. uscita L/R del mixer su due ingressi del Tascam o dell'FX6)."""
    left = next(t for t in p["tracks"] if t["id"] == left_id)
    right = next(t for t in p["tracks"] if t["id"] == right_id)
    if len(left["channels"]) != 1 or len(right["channels"]) != 1 or left.get("destra") or right.get("destra"):
        raise ValueError("si uniscono solo due tracce mono")
    if left["wav"] == right["wav"]:  # stesso file: basta leggere i due canali insieme
        left["channels"] = left["canali_file"] = [left["channels"][0], right["channels"][0]]
    else:
        left["destra"] = {**right, "delta_s": right["offset_s"] - left["offset_s"]}
    left["nome"] = f"{left['nome']} + {right['nome']}"
    left["analisi"] = None
    p["tracks"].remove(right)
    return left


def auto_place(p: dict):
    auto = [t for t in p["tracks"] if t["pos_mode"] == "auto"]
    if any("extra_dist_m" not in t for t in auto):  # costoso (GCC): solo con tracce nuove
        try:
            extra = geometry.same_clock_distances(auto)
        except Exception:  # file troppo corti o illeggibili: resta la stima tipica
            extra = {}
        for t in auto:
            t["extra_dist_m"] = extra.get(t["id"], 0.0)
    for tid, pos in geometry.auto_positions(auto, p["sala"]).items():
        next(t for t in auto if t["id"] == tid)["pos"] = pos
    fuse_scene(p)  # con le immagini dell'analisi le posizioni tipiche sono solo il punto di partenza


# --- lavori in background ---------------------------------------------------

def start_job(kind: str, fn) -> str:
    jid = uuid.uuid4().hex[:8]
    job = {"id": jid, "tipo": kind, "progress": 0.0, "msg": "", "done": False, "error": None, "result": None}
    STATE["jobs"][jid] = job

    def run():
        try:
            job["result"] = fn(job)
        except Exception as e:  # l'errore va al pannello, non nel vuoto
            job["error"] = f"{type(e).__name__}: {e}"
        job["done"] = True
    threading.Thread(target=run, daemon=True).start()
    return jid


def job_analyze(job):
    p = STATE["project"]
    ts = p["tracks"]
    done = {}  # avanzamento per traccia: le analisi girano in parallelo (ffmpeg decodifica in processi separati)

    def one(t):
        step = lambda f: (done.__setitem__(t["id"], f), job.update(progress=sum(done.values()) / len(ts) * 0.6,
                                                                    msg=f"analisi {sum(v >= 1 for v in done.values())}/{len(ts)}"))
        t["analisi"] = analysis.analyze(t["wav"], t["channels"], t["info"]["duration"], t["info"].get("bits") == 32,
                                        progress=step)
        step(1.0)
    with ThreadPoolExecutor(WORKERS) as ex:
        list(ex.map(one, ts))
    # riferimento: quello scelto, altrimenti la registrazione più lunga (di solito il registratore principale)
    ref = next((t for t in ts if t["id"] == p["riferimento"]), max(ts, key=lambda t: t["info"]["duration"], default=None))
    if ref:
        p["riferimento"] = ref["id"]
    others = [t for t in ts if ref and t is not ref]
    synced = []

    def sync(t):
        try:
            s = analysis.sync_pair(ref, t)
            t.update(offset_s=s["offset_s"], drift_ppm=s["drift_ppm"], sync_t0=s["sync_t0"], sync=s)
        except Exception as e:  # es. clip senza parte comune con il riferimento: resta il sync di Resolve
            t["sync"] = {"errore": str(e), "fiducia": 0}
        synced.append(t)
        job.update(msg=f"sync {len(synced)}/{len(others)}", progress=0.6 + 0.3 * len(synced) / max(len(others), 1))
    with ThreadPoolExecutor(WORKERS) as ex:
        list(ex.map(sync, others))
    job["msg"] = "posizionamento e stima delle sorgenti"
    p["spazio_stimato"] = estimate_space(ts)
    p["immagini"] = sound_images(p, ref)
    auto_place(p)
    job["progress"] = 1.0
    return {"tracce": len(ts)}


def fuse_scene(p: dict):
    """Allinea le immagini dei mic in un'unica scena: posizioni dei mic in automatico e sorgenti
    stimate. I mic posizionati a mano restano fermi e fanno da ancora. Veloce: niente audio."""
    imgs, sc = p.get("immagini") or {}, None
    if imgs.get("tracce"):
        mics = {t["id"]: t for t in p["tracks"] if t["id"] in imgs["tracce"] or t["id"] == imgs["riferimento"]}
        mics = {i: t for i, t in mics.items() if not mixer.is_line(t)}
        try:
            sc = fusion.fuse(imgs, {i: t["pos"] for i, t in mics.items()},
                             {i for i, t in mics.items() if t["pos_mode"] != "auto"}, p.get("palco", {"w": 12, "d": 4}))
        except Exception as e:  # dati insufficienti: resta il posizionamento tipico
            sc = {"errore": str(e)[:160]}
    p["scena"] = sc
    est = []
    if sc and "mic" in sc:
        for i, m in sc["mic"].items():
            t = next(t for t in p["tracks"] if t["id"] == i)
            if t["pos_mode"] == "auto":
                t["pos"] = m["pos"]
        est = [{"id": f"stima_{s['k']}", "nome": f"Sorgente {s['k'] + 1}", "pos": s["pos"], "stimata": True,
                "errore_m": s["incertezza_m"]} for s in sc["sorgenti"]]
    p["sorgenti"] = [x for x in p.get("sorgenti", []) if not x.get("stimata")] + est
    p["campo"] = sound_field(p)


def sound_field(p: dict) -> dict | None:
    """Gaussian splatting sonoro: sorgenti come gaussiane (raggio, energia per ottava) + diffuso della sala,
    ottimizzate perché ogni mic senta quello che ha registrato. Parte dalla scena fusa."""
    imgs, sc = p.get("immagini") or {}, p.get("scena") or {}
    if not sc.get("sorgenti"):
        return None
    tracks = {t["id"]: t for t in p["tracks"]}
    db = devices.load()["microfoni"]
    mics = {i: {"pos": m["pos"], "a": splat.PATTERN.get(db.get(tracks[i].get("microfono") or "", {}).get("diagramma"), 1.0)}
            for i, m in sc["mic"].items() if i in tracks}
    obs = [(i, e["k"], e["bande_db"]) for i, g in imgs.get("tracce", {}).items() if i in mics
           for e in g["sorgenti"] if e.get("bande_db")]
    try:
        return splat.fit(obs, mics, sc["sorgenti"], p.get("palco", {"w": 12, "d": 4}))
    except Exception as e:
        return {"errore": str(e)[:160]}


def sound_images(p: dict, ref: dict | None) -> dict | None:
    """Cosa sente ogni mic (sorgenti, ritardi, direzione, distanza) rispetto alla linea del mixer,
    o al riferimento se non c'è linea. Facoltativo: se le tracce non bastano si va avanti senza."""
    ts = p["tracks"]  # anche le tracce mute: la linea del mixer spesso è muta nel mix ma è il miglior riferimento
    line = next((t for t in ts if mixer.is_line(t)), None)
    ref = line or ref
    if not ref or len(ts) < 2:
        return None
    rt60 = (p.get("spazio_stimato") or {}).get("rt60") or 1.5
    try:
        return localize.images(ts, ref, p["sala"], rt60, devices.load()["microfoni"], line=bool(line))
    except Exception as e:
        return {"errore": str(e)[:160]}


def estimate_space(ts: list[dict]) -> dict | None:
    """Sala stimata dalle registrazioni (RT60 dalle discese libere) e preset più simile: solo un suggerimento."""
    rts = [t["analisi"]["rt60_stima"] for t in ts if (t.get("analisi") or {}).get("rt60_stima")]
    if not rts:
        return None
    rt = round(float(np.median(rts)), 2)
    near = min(spazi.all_spaces(), key=lambda s: abs((s.get("rt60") or {}).get("500", 99) - rt))
    return {"rt60": rt, "tracce": len(rts), "simile": near["id"], "nome": near["nome"]}


def job_eq_auto(job, ids):
    p = STATE["project"]
    if ids == ["master"]:
        return {"master": autotune.run_master(p, progress=lambda f: job.update(progress=f))}
    rt60 = spazi.get(p["spazio"]).get("rt60") if p.get("spazio") else None
    return autotune.run(p, rt60, ids, progress=lambda f: job.update(progress=f))


def eq_curve(tid: str) -> dict:
    """Curva dell'EQ (a riposo e con le dinamiche al massimo) e spettro prima/dopo."""
    p = STATE["project"]
    t = ({"eq": p.get("eq_master"), "eq_analisi": p.get("eq_master_analisi")} if tid == "master"
         else next(t for t in p["tracks"] if t["id"] == tid))
    a = t.get("eq_analisi")
    f = np.array(a["f"]) if a else autotune.GRID
    r = {"f": np.round(f, 1).tolist(),
         "statica": np.round(eq.response_db(t.get("eq") or [], f), 2).tolist(),
         "dinamica": np.round(eq.response_db(t.get("eq") or [], f, dynamic=True), 2).tolist()}
    if tid == "master":
        r["look"] = np.round(look.curve(p, f), 2).tolist()
    if a:
        r.update(prima=a["db"], dopo=np.round(np.array(a["db"]) + r["statica"] + np.array(r.get("look", 0)), 1).tolist(), sorgente=a["sorgente"])
    return r


def job_print(job, opts):
    """Stampa su file; con Resolve: su traccia nuova/esistente o sulla regione
    (marker "MIX3D" o In/Out), sostituendo la stampa precedente sulla traccia MIX3D."""
    p = STATE["project"]
    path = os.path.expanduser(opts.get("path") or "~/Desktop/MIX3D.wav")
    target = opts.get("target", "file")
    r = p.get("resolve") or {}
    fps = float(r.get("fps") or 25)
    rng = resolve = None
    if target != "file":
        from . import resolve_bridge as rb
        resolve = rb.connect()
        if opts.get("regione"):
            reg = rb.region(resolve)
            if reg is None:
                raise RuntimeError('nessun marker "MIX3D" con durata né In/Out sulla timeline')
            rng = (reg[0] / fps, reg[1] / fps)
            job["msg"] = f"regione da {reg[2]}"
    stem, ext = os.path.splitext(path)
    if rng:
        path = f"{stem}_{int(rng[0] * fps)}{ext}"  # una stampa per regione: nomi diversi
    job["msg"] = "render"
    res = mixer.print_mix(p, path, target_lufs=opts.get("lufs", -14.0), rng=rng,
                          progress=lambda f: job.update(progress=f * 0.95))
    if resolve:
        from . import resolve_bridge as rb
        frame = int(round(res["inizio_s"] * fps))
        track = None if target == "new" else int(target) if str(target).isdigit() else rb.mix3d_track(resolve)
        if track and opts.get("regione"):
            res["sostituite"] = rb.clear_range(resolve, track, int(r.get("start_frame", 0)) + frame,
                                               int(r.get("start_frame", 0)) + frame + int(res["durata_s"] * fps))
        job["msg"] = "reimport in Resolve"
        res["traccia"] = rb.reimport_wav(resolve, path, int(r.get("start_frame", 0)) + frame, track_index=track)
    job["progress"] = 1.0
    return res


def import_resolve(info: dict | None = None) -> int:
    """Clip della timeline: da `info` (script dentro Resolve) o via API esterna (Studio).
    Le tracce lette prima da Resolve vengono sostituite, non duplicate."""
    if info is None:
        from .resolve_bridge import connect, read_audio_clips
        info = read_audio_clips(connect())
    p = STATE["project"]
    p["tracks"] = [t for t in p["tracks"] if not t.get("da_resolve")]
    fps = float(info["fps"])
    p["resolve"] = {"start_frame": info["start_frame"], "fps": fps, "timeline": info["timeline"]}
    STATE["host_rel"] = False
    added, seen, errors = 0, set(), []
    clips = sorted(info["clips"], key=lambda c: c.get("kind", "audio") != "audio")
    key = lambda c: (c["file_path"], c["start_frame"] - c["left_offset"])
    lane = lambda c: f"{'V' if c.get('kind') == 'video' else 'A'}{c['track']}"
    lanes: dict = {}  # file e posizione -> tracce di Resolve dove compare (FX6: ch1-2 su A1, ch3-4 su A2)
    for c in clips:
        if lane(c) not in lanes.setdefault(key(c), []):
            lanes[key(c)].append(lane(c))
    # prima le clip audio (nomi A1, A2…), poi le video: stesso file e posizione = una sola traccia
    for c in clips:
        # una clip video compare su più tracce audio (es. FX6 ch1-2 su A1, ch3-4 su A2):
        # il file si importa una volta sola, con tutti i suoi canali
        if not c["file_path"] or key(c) in seen:
            continue
        seen.add(key(c))
        off = (c["start_frame"] - c["left_offset"] - info["start_frame"]) / fps
        label = f"{'V' if c.get('kind') == 'video' else 'A'}{c['track']} {c['name']}"
        try:
            new = tracks_from_file(c["file_path"], off, label)
        except media.NoAudio:  # clip video senza audio: niente da ascoltare, non è un errore
            continue
        except Exception as e:  # file mancante, offline o illeggibile: le altre clip arrivano lo stesso
            errors.append(f"{c['name']}: {e}")
            continue
        ln = lanes[key(c)]
        p["tracks"] += [{**t, "da_resolve": True, "canale": ln[min(i, len(ln) - 1)]} for i, t in enumerate(new)]
        added += 1
    p["resolve"]["non_lette"] = errors
    return added


# --- dati per il pannello ---------------------------------------------------

def devices_payload() -> dict:
    db = devices.load()
    f = np.array(analysis.THIRD_OCT)
    th = np.linspace(0, 2 * np.pi, 73)
    curves = {k: {"risposta": np.round(devices.response_db(m, f), 1).tolist(),
                  "correzione": np.round(devices.correction_db(m, f), 1).tolist(),
                  "polare": np.round(devices.polar_gain(m, th), 3).tolist()}
              for k, m in db["microfoni"].items()}
    return {**db, "f": np.round(f, 1).tolist(), "curve": curves, "compat": devices.compat_matrix()}


def public_state() -> dict:
    p = STATE["project"]
    span = mixer.span(p) if p["tracks"] else (0, 0)
    return {**p, "span": span}


def browse(d: str, ext: str | None = None) -> dict:
    d = os.path.expanduser(d or "~")
    entries = []
    for e in sorted(os.scandir(d), key=lambda e: (not e.is_dir(), e.name.lower())):
        if e.name.startswith("."):
            continue
        if e.is_dir() or Path(e.name).suffix.lower() in ({f".{ext}"} if ext else AUDIO_EXT):
            entries.append({"nome": e.name, "path": e.path, "dir": e.is_dir()})
    return {"dir": d, "su": str(Path(d).parent), "voci": entries}


def wav_bytes(x: np.ndarray, sr: int) -> bytes:
    buf = io.BytesIO()
    sf.write(buf, np.clip(x, -1, 1), sr, "PCM_16", format="WAV")
    return buf.getvalue()


# --- HTTP -------------------------------------------------------------------

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(WEB), **kw)

    def log_message(self, *a):
        pass

    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            if u.path == "/api/state":
                return self.send_json(public_state())
            if u.path == "/api/devices":
                return self.send_json(devices_payload())
            if u.path == "/api/resolve/integration":
                from . import resolve_install
                return self.send_json(resolve_install.status())
            if u.path == "/api/browse":
                return self.send_json(browse(q.get("dir", ""), q.get("ext")))
            if u.path == "/api/rev":  # il pannello (e il plugin, con p=1) controllano cosa è cambiato
                if q.get("p") != "1":
                    STATE["poll"] = time.time()
                h = STATE["host"]
                return self.send_json({"rev": STATE["rev"], "mix": STATE["mix"],
                                       "tracce": len(mixer.active(STATE["project"]["tracks"])),
                                       "host": {**h, "age": time.time() - h["at"]} if h and time.time() - h["at"] < 1 else None})
            if u.path == "/api/update":
                from . import updater
                return self.send_json(updater.check(q.get("force") == "1"))
            if u.path == "/api/spazi":
                return self.send_json([{**s, "distanza_critica": spazi.critical_distance(s)} for s in spazi.all_spaces()])
            if u.path.startswith("/api/jobs/"):
                return self.send_json(STATE["jobs"][u.path.rsplit("/", 1)[1]])
            if u.path == "/api/look":
                return self.send_json(look.catalog())
            if u.path == "/api/eq/curve":
                return self.send_json(eq_curve(q["track"]))
            if u.path == "/api/render":
                p, t0 = STATE["project"], float(q["t0"])
                if "pos" in q:  # richiesta del plugin: tempi dell'host, playhead in `pos`
                    t0 = host_time(t0)
                    STATE["host"] = {"t": host_time(float(q["pos"])), "play": q.get("play") == "1", "at": time.time()}
                x, lv = mixer.render(p, t0, float(q.get("dur", 2)), q.get("b") == "1")
                if "pos" in q:
                    STATE["host"]["lv"] = lv
                b, lv = wav_bytes(x, p["sr"]), json.dumps(lv)
                self.send_response(200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("X-Levels", lv)
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                return self.wfile.write(b)
        except Exception as e:
            return self.send_json({"errore": f"{type(e).__name__}: {e}"}, 500)
        return super().do_GET()

    def do_POST(self):
        u = urlparse(self.path)
        p = STATE["project"]
        try:
            b = self.body()
            with LOCK:
                STATE["mix"] += 1  # ogni modifica: il plugin butta l'audio già preparato
                if u.path == "/api/files":
                    for path in b["paths"]:
                        p["tracks"] += tracks_from_file(path)
                    auto_place(p)
                elif u.path == "/api/tracce/dividi":
                    split_track(p, b["id"])
                elif u.path == "/api/tracce/unisci":
                    join_tracks(p, b["sinistra"], b["destra"])
                elif u.path == "/api/resolve/import":
                    import_resolve()
                    auto_place(p)
                elif u.path == "/api/resolve/push":
                    aperto = time.time() - STATE["poll"] < 6  # un pannello sta controllando /api/rev
                    n = import_resolve(json.loads(SESSION.read_text()))
                    auto_place(p)
                    STATE["rev"] += 1
                    return self.send_json({"clip": n, "pannello": aperto})
                elif u.path == "/api/state":
                    for k, v in b.items():
                        if k != "tracks":
                            p[k] = v
                    for patch in b.get("tracks", []):
                        t = next(t for t in p["tracks"] if t["id"] == patch["id"])
                        if "profile" in patch and patch["profile"] != t["profile"]:
                            apply_profile(t, patch["profile"])
                        t.update({k: v for k, v in patch.items() if k != "profile"})
                    # un mic spostato a mano diventa un'ancora: la scena si riallinea attorno
                    if "sala" in b or "palco" in b or any("pos" in x or x.get("pos_mode") == "auto" for x in b.get("tracks", [])):
                        auto_place(p)
                elif u.path == "/api/spazio":
                    sp = spazi.get(b["id"])
                    p.update(spazio=sp["id"], sala=dict(sp["sala"]), palco=dict(sp["palco"]),
                             listener=list(sp["ascoltatore"]))
                    auto_place(p)
                elif u.path == "/api/spazi/import":
                    return self.send_json(spazi.import_file(b["path"]))
                elif u.path == "/api/remove":
                    p["tracks"] = [t for t in p["tracks"] if t["id"] != b["id"]]
                elif u.path == "/api/fondi":  # ricalcola la scena dopo una correzione a mano
                    auto_place(p)
                elif u.path == "/api/analyze":
                    return self.send_json({"job": start_job("analisi", job_analyze)})
                elif u.path == "/api/eq/auto":
                    return self.send_json({"job": start_job("eq", lambda j: job_eq_auto(j, b.get("tracks")))})
                elif u.path == "/api/update/install":
                    from . import updater
                    return self.send_json({"job": start_job("aggiornamento", updater.install)})
                elif u.path == "/api/print":
                    return self.send_json({"job": start_job("stampa", lambda j: job_print(j, b))})
                elif u.path == "/api/save":
                    path = os.path.expanduser(b.get("path") or "~/Desktop/mix3d_progetto.json")
                    Path(path).write_text(json.dumps(p, ensure_ascii=False, indent=1))
                    return self.send_json({"path": path})
                elif u.path == "/api/load":
                    STATE["project"] = {**new_project(), **json.loads(Path(os.path.expanduser(b["path"])).read_text())}
                    for t in STATE["project"]["tracks"]:  # progetti precedenti senza catena
                        t.setdefault("microfono", devices.profile(t["profile"])["microfono"])
                elif u.path == "/api/resolve/install":
                    from . import resolve_install
                    return self.send_json(resolve_install.install(b.get("pannello", True)))
                elif u.path == "/api/quit":
                    threading.Timer(0.3, os._exit, (0,)).start()
                    return self.send_json({"ok": True})
                elif u.path == "/api/new":
                    STATE["project"] = new_project()
                else:
                    return self.send_json({"errore": "endpoint sconosciuto"}, 404)
            return self.send_json(public_state())
        except Exception as e:
            return self.send_json({"errore": f"{type(e).__name__}: {e}"}, 400)


def serve(port: int = 8730, open_browser: bool = True):
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError:  # già aperto (es. doppio clic sull'app): riapri solo il browser
        if open_browser:
            import webbrowser
            webbrowser.open(f"http://127.0.0.1:{port}")
        return
    url = f"http://127.0.0.1:{port}"
    try:
        from . import resolve_install
        resolve_install.refresh_script()
    except OSError:
        pass
    if SESSION.exists() and time.time() - SESSION.stat().st_mtime < 120:  # avviata dallo script in Resolve
        try:
            import_resolve(json.loads(SESSION.read_text()))
            auto_place(STATE["project"])
        except Exception as e:
            print(f"timeline di Resolve non importata: {e}")
    print(f"MIX3D pannello: {url}  (Ctrl+C per uscire)")
    if open_browser:
        import webbrowser
        webbrowser.open(url)
    srv.serve_forever()
