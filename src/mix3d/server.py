"""Pannello MIX3D: server locale (solo libreria standard) + API JSON.

Avvio: `mix3d ui` e apri http://127.0.0.1:8730. Ascolta solo in locale.
Lo stato è un progetto JSON (piano, M11) salvabile e ricaricabile.
"""
from __future__ import annotations

import io
import json
import os
import threading
import uuid
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import numpy as np
import soundfile as sf

from . import analysis, autotune, devices, eq, geometry, media, mixer, spazi

WEB = Path(__file__).parent / "web"
AUDIO_EXT = {".wav", ".bwf", ".mp4", ".mov", ".mxf", ".m4a", ".aac", ".mp3", ".flac", ".aif", ".aiff"}


def new_project() -> dict:
    return {"nome": "Concerto", "sr": 48000, "sala": {"w": 20.0, "d": 30.0, "h": 8.0},
            "listener": [0.0, 1.7, 8.0], "master_db": -6.0, "correzione": True,
            "attenuazione": 0.5, "dist_ref_m": 5.0, "larghezza": 1.0,
            "riferimento": None, "resolve": None, "spazio": None, "palco": {"w": 12, "d": 4, "h": 0.6},
            "sorgenti": [], "lobi": True, "tracks": []}


STATE = {"project": new_project(), "jobs": {}}
LOCK = threading.Lock()


# --- tracce -----------------------------------------------------------------

def apply_profile(t: dict, pid: str):
    p = devices.profile(pid)
    t.update(profile=pid, registratore=p["registratore"], microfono=p["microfono"], posizione_tipica=p["posizione"],
             ruolo=p["ruolo"], mute=p["gain_db"] is None, gain_db=p["gain_db"] or 0.0)


def tracks_from_file(path: str, offset_s: float = 0.0, name: str | None = None) -> list[dict]:
    info = media.probe(path)
    wav = media.decoded(path)
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
        out.append(t)
    return out


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
    for i, t in enumerate(ts):
        job["msg"] = f"analisi {t['nome']}"
        is_float = t["info"].get("bits") == 32
        t["analisi"] = analysis.analyze(t["wav"], t["channels"], t["info"]["duration"], is_float,
                                        progress=lambda f, i=i: job.update(progress=(i + f) / len(ts) * 0.6))
    ref = next((t for t in ts if t["id"] == p["riferimento"]), ts[0] if ts else None)
    if ref:
        p["riferimento"] = ref["id"]
    others = [t for t in ts if ref and t is not ref]
    for i, t in enumerate(others):
        job["msg"] = f"sync {t['nome']}"
        try:
            s = analysis.sync_pair(ref, t)
            t.update(offset_s=s["offset_s"], drift_ppm=s["drift_ppm"], sync_t0=s["sync_t0"], sync=s)
        except Exception as e:
            t["sync"] = {"errore": str(e), "fiducia": 0}
        job["progress"] = 0.6 + 0.3 * (i + 1) / max(len(others), 1)
    job["msg"] = "posizionamento e stima delle sorgenti"
    auto_place(p)
    try:
        est = geometry.estimate_sources(ts, p["sala"], p.get("palco", {}).get("d", 4))
    except Exception:  # stima facoltativa: se i file non bastano si va avanti senza
        est = []
    p["sorgenti"] = [x for x in p.get("sorgenti", []) if not x.get("stimata")] + est
    job["progress"] = 1.0
    return {"tracce": len(ts)}


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
    if a:
        r.update(prima=a["db"], dopo=np.round(np.array(a["db"]) + r["statica"], 1).tolist(), sorgente=a["sorgente"])
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


def import_resolve() -> int:
    from .resolve_bridge import connect, read_audio_clips

    info = read_audio_clips(connect())
    p = STATE["project"]
    fps = float(info["fps"])
    p["resolve"] = {"start_frame": info["start_frame"], "fps": fps, "timeline": info["timeline"]}
    added, seen = 0, set()
    for c in info["clips"]:
        # una clip video compare su più tracce audio (es. FX6 ch1-2 su A1, ch3-4 su A2):
        # il file si importa una volta sola, con tutti i suoi canali
        key = (c["file_path"], c["start_frame"] - c["left_offset"])
        if not c["file_path"] or key in seen:
            continue
        seen.add(key)
        off = (c["start_frame"] - c["left_offset"] - info["start_frame"]) / fps
        for t in tracks_from_file(c["file_path"], off, f"A{c['track']} {c['name']}"):
            p["tracks"].append({**t, "da_resolve": True})
        added += 1
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
    return {**db, "f": np.round(f, 1).tolist(), "curve": curves}


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
            if u.path == "/api/spazi":
                return self.send_json([{**s, "distanza_critica": spazi.critical_distance(s)} for s in spazi.all_spaces()])
            if u.path.startswith("/api/jobs/"):
                return self.send_json(STATE["jobs"][u.path.rsplit("/", 1)[1]])
            if u.path == "/api/eq/curve":
                return self.send_json(eq_curve(q["track"]))
            if u.path == "/api/render":
                p = STATE["project"]
                x, lv = mixer.render(p, float(q["t0"]), float(q.get("dur", 2)), q.get("b") == "1")
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
                if u.path == "/api/files":
                    for path in b["paths"]:
                        p["tracks"] += tracks_from_file(path)
                    auto_place(p)
                elif u.path == "/api/resolve/import":
                    import_resolve()
                    auto_place(p)
                elif u.path == "/api/state":
                    for k, v in b.items():
                        if k != "tracks":
                            p[k] = v
                    for patch in b.get("tracks", []):
                        t = next(t for t in p["tracks"] if t["id"] == patch["id"])
                        if "profile" in patch and patch["profile"] != t["profile"]:
                            apply_profile(t, patch["profile"])
                        t.update({k: v for k, v in patch.items() if k != "profile"})
                    if "sala" in b or any(x.get("pos_mode") == "auto" for x in b.get("tracks", [])):
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
                elif u.path == "/api/analyze":
                    return self.send_json({"job": start_job("analisi", job_analyze)})
                elif u.path == "/api/eq/auto":
                    return self.send_json({"job": start_job("eq", lambda j: job_eq_auto(j, b.get("tracks")))})
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
    print(f"MIX3D pannello: {url}  (Ctrl+C per uscire)")
    if open_browser:
        import webbrowser
        webbrowser.open(url)
    srv.serve_forever()
