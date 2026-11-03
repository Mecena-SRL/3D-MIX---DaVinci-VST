// MIX3D pannello: stato dal server, tracce, scena 3D, analisi, ascolto e stampa.
import * as THREE from "three";
import { OrbitControls } from "./vendor/OrbitControls.js";

const $ = (id) => document.getElementById(id);
const COLORS = ["#4fb3ff", "#f5b942", "#3ccf8e", "#ff7aa8", "#b38cff", "#ff8c42", "#5ee0e0", "#d4e157", "#ff5d5d", "#9aa5b1"];
let S = null, DB = null, sel = null;

// --- utilità ------------------------------------------------------------------
const api = async (path, body) => {
  const r = await fetch(path, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {});
  const j = await r.json();
  if (j.errore) throw new Error(j.errore);
  return j;
};
const toast = (msg, err) => { const t = $("toast"); t.textContent = msg; t.className = "toast" + (err ? " err" : ""); t.hidden = false; clearTimeout(t._h); t._h = setTimeout(() => (t.hidden = true), 4000); };
const safe = (fn) => async (...a) => { try { await fn(...a); } catch (e) { toast(e.message, true); } };
const fmt = (s) => `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, "0")}`;
const color = (t) => COLORS[S.tracks.indexOf(t) % COLORS.length];
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
let pushT = null;
function push(patch, flush = true) { // modifica locale + invio al server con debounce
  clearTimeout(pushT);
  pushT = setTimeout(safe(async () => { S = await api("/api/state", patch); if (flush) player.flush(); scene.sync(); }), 120);
}
const pushTrack = (t, fields) => { Object.assign(t, fields); push({ tracks: [{ id: t.id, ...fields }] }); };

// --- tracce -------------------------------------------------------------------
function renderTracks() {
  const box = $("tracks");
  box.querySelectorAll(".trk").forEach((e) => e.remove());
  $("emptyTracks").hidden = S.tracks.length > 0;
  const profiles = DB.profili;
  for (const t of S.tracks) {
    const el = document.createElement("div");
    el.className = "trk" + (t.id === sel ? " sel" : "") + (t.confermato ? "" : " todo");
    el.style.setProperty("--c", color(t));
    const sug = new Set(t.suggeriti.map((s) => s.id));
    const opts = t.suggeriti.map((s) => `<option value="${s.id}">★ ${s.nome} (${Math.round(s.confidenza * 100)}%)</option>`).join("")
      + `<option disabled>──────────</option>` + profiles.filter((p) => !sug.has(p.id)).map((p) => `<option value="${p.id}">${p.nome}</option>`).join("");
    const sy = t.sync;
    const syncBadge = t.id === S.riferimento ? `<span class="badge ok">riferimento</span>`
      : !sy ? `<span class="badge">non sincronizzata</span>`
      : sy.errore ? `<span class="badge bad" title="${sy.errore}">sync fallito</span>`
      : `<span class="badge ${sy.fiducia > 0.6 ? "ok" : sy.fiducia > 0.3 ? "warn" : "bad"}" title="residuo ${sy.residuo_us} µs, fiducia ${sy.fiducia}">${(t.offset_s).toFixed(3)} s · ${sy.drift_ppm} ppm</span>`;
    el.innerHTML = `
      <div class="top"><span class="name" title="${t.file}">${t.nome}</span>${syncBadge}
        <button class="ms m ${t.mute ? "on" : ""}" title="Muto">M</button><button class="ms s ${t.solo ? "on" : ""}" title="Solo">S</button></div>
      <select class="prof" title="Combinazione pronta">${opts}</select>
      <div class="chain"><select class="rec" title="Registratore">${Object.entries(DB.registratori).map(([k, r]) => `<option value="${k}">${r.nome}</option>`).join("")}</select>
        <select class="mic" title="Microfono">${Object.entries(DB.microfoni).map(([k, m]) => `<option value="${k}">${m.nome}</option>`).join("")}</select></div>
      ${t.confermato ? "" : `<button class="confirm" title="${t.suggeriti[0].motivi.join(", ") || "nessun indizio"}">Conferma dispositivo</button>`}
      <canvas></canvas>
      <div class="meter"><i data-meter="${t.id}"></i></div>
      <div class="ctl"><span class="muted small">Gain</span><input type="range" min="-30" max="12" step="0.5" value="${t.gain_db}"><span class="small gv">${t.gain_db.toFixed(1)} dB</span></div>`;
    const s = el.querySelector(".prof");
    s.value = t.profile;
    for (const k of ["rec", "mic"]) {
      const c = el.querySelector(`.${k}`), field = k === "rec" ? "registratore" : "microfono";
      c.value = t[field];
      c.onclick = (e) => e.stopPropagation();
      c.onchange = () => { pushTrack(t, { [field]: c.value, confermato: true }); setTimeout(refresh, 300); };
    }
    s.onchange = () => { pushTrack(t, { profile: s.value, confermato: true }); setTimeout(refresh, 300); };
    s.onclick = (e) => e.stopPropagation();
    el.querySelector(".confirm")?.addEventListener("click", (e) => { e.stopPropagation(); pushTrack(t, { confermato: true }); el.classList.remove("todo"); e.target.remove(); });
    el.querySelector(".m").onclick = (e) => { e.stopPropagation(); pushTrack(t, { mute: !t.mute }); e.target.classList.toggle("on"); };
    el.querySelector(".s").onclick = (e) => { e.stopPropagation(); pushTrack(t, { solo: !t.solo }); e.target.classList.toggle("on"); };
    const g = el.querySelector("input[type=range]");
    g.onclick = (e) => e.stopPropagation();
    g.oninput = () => { el.querySelector(".gv").textContent = `${(+g.value).toFixed(1)} dB`; pushTrack(t, { gain_db: +g.value }); };
    el.onclick = () => select(t.id);
    box.appendChild(el);
    drawMiniWave(el.querySelector("canvas"), t);
  }
}

function drawMiniWave(cv, t) {
  const ctx = fit(cv), W = cv.width, H = cv.height;
  const ov = t.analisi?.overview;
  ctx.fillStyle = css("--panel2"); ctx.fillRect(0, 0, W, H);
  if (!ov) { ctx.fillStyle = css("--muted"); ctx.font = `${10 * devicePixelRatio}px sans-serif`; ctx.fillText("analisi da fare", 6, H / 2 + 4); return; }
  ctx.fillStyle = color(t);
  const n = ov.max.length;
  for (let i = 0; i < n; i++) {
    const x = (i / n) * W, y0 = H / 2 - ov.max[i] * H / 2, y1 = H / 2 - ov.min[i] * H / 2;
    ctx.fillRect(x, y0, Math.max(W / n, 1), Math.max(y1 - y0, 1));
  }
}

function select(id) {
  sel = id;
  document.querySelectorAll(".trk").forEach((e, i) => e.classList.toggle("sel", S.tracks[i]?.id === id));
  renderAnalysis(); renderDevice(); scene.highlight();
}
const selected = () => S.tracks.find((t) => t.id === sel);

// --- grafici su canvas ----------------------------------------------------------
function fit(cv) {
  const r = cv.getBoundingClientRect();
  cv.width = Math.max(r.width, 50) * devicePixelRatio;
  cv.height = (cv.classList.contains("square") ? r.width : (+cv.getAttribute("height") || r.height)) * devicePixelRatio;
  return cv.getContext("2d");
}

// grafico a linee: series = [{x, y, color}], xlog, range y
function lineChart(cv, series, { xlog = false, ymin, ymax, xlabel = (v) => v, ylabel = (v) => v } = {}) {
  const ctx = fit(cv), W = cv.width, H = cv.height, d = devicePixelRatio, pad = 34 * d;
  const xs = series.flatMap((s) => s.x).filter((v) => v != null), tx = xlog ? Math.log10 : (v) => v;
  const x0 = tx(Math.min(...xs)), x1 = tx(Math.max(...xs));
  const X = (v) => pad + ((tx(v) - x0) / (x1 - x0 || 1)) * (W - pad - 8 * d);
  const Y = (v) => 8 * d + (1 - (v - ymin) / (ymax - ymin || 1)) * (H - pad);
  ctx.font = `${10 * d}px sans-serif`; ctx.fillStyle = css("--muted"); ctx.strokeStyle = css("--line"); ctx.lineWidth = d;
  const yt = niceTicks(ymin, ymax, 5);
  for (const v of yt) { ctx.beginPath(); ctx.moveTo(pad, Y(v)); ctx.lineTo(W, Y(v)); ctx.stroke(); ctx.fillText(ylabel(v), 2 * d, Y(v) + 3 * d); }
  const xt = xlog ? [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000] : niceTicks(Math.min(...xs), Math.max(...xs), 6);
  for (const v of xt) { ctx.fillText(xlabel(v), X(v) - 8 * d, H - 6 * d); }
  for (const s of series) {
    ctx.strokeStyle = s.color; ctx.lineWidth = (s.w || 2) * d; ctx.beginPath();
    let started = false;
    s.x.forEach((xv, i) => { const yv = s.y[i]; if (yv == null) { started = false; return; } const px = X(xv), py = Y(Math.max(ymin, Math.min(ymax, yv))); started ? ctx.lineTo(px, py) : ctx.moveTo(px, py); started = true; });
    ctx.stroke();
  }
}
function niceTicks(a, b, n) {
  const step = Math.pow(10, Math.floor(Math.log10((b - a) / n || 1))) * [1, 2, 5, 10].find((m) => (b - a) / (Math.pow(10, Math.floor(Math.log10((b - a) / n || 1))) * m) <= n);
  const out = []; for (let v = Math.ceil(a / step) * step; v <= b; v += step) out.push(+v.toFixed(6)); return out;
}
const kHz = (v) => (v >= 1000 ? `${v / 1000}k` : `${v}`);

// --- analisi ----------------------------------------------------------------------
function renderAnalysis() {
  const t = selected(), a = t?.analisi;
  $("anaEmpty").hidden = !!a; $("ana").hidden = !a;
  if (!a) return;
  $("anaTitle").textContent = t.nome;
  const sy = t.sync && !t.sync.errore ? t.sync : null;
  const tiles = [["Picco", `${a.peak_dbfs} dBFS`], ["RMS mediano", `${a.rms_dbfs} dBFS`], ["Rumore di fondo", `${a.rumore_dbfs} dBFS`],
    ["Dinamica", `${a.dinamica_db} dB`], ["Loudness", `${a.lufs} LUFS`], ["Banda utile", a.banda_utile_hz ? `${(a.banda_utile_hz / 1000).toFixed(1)} kHz` : "-"],
    ["Campioni saturi", a.clip_campioni], ["Offset", `${t.offset_s.toFixed(4)} s`],
    ["Drift", sy ? `${sy.drift_ppm} ppm` : "-"], ["Fiducia sync", sy ? `${Math.round(sy.fiducia * 100)}%` : t.id === S.riferimento ? "riferimento" : "-"]];
  $("anaTiles").innerHTML = tiles.map(([k, v]) => `<div class="tile"><span>${k}</span><b>${v}</b></div>`).join("");
  $("anaWarn").innerHTML = [...a.avvisi, ...chainRisks(t)].map((w) => `<span class="chip">${w}</span>`).join("");
  // forma d'onda con indicatori di clipping
  const cv = $("cWave"), ctx = fit(cv), W = cv.width, H = cv.height, n = a.overview.max.length;
  ctx.fillStyle = color(t);
  for (let i = 0; i < n; i++) {
    const y0 = H / 2 - a.overview.max[i] * H / 2, y1 = H / 2 - a.overview.min[i] * H / 2;
    if (Math.max(a.overview.max[i], -a.overview.min[i]) >= 0.999) ctx.fillStyle = css("--bad"); else ctx.fillStyle = color(t);
    ctx.fillRect((i / n) * W, y0, Math.max(W / n, 1), Math.max(y1 - y0, 1));
  }
  // spettro + risposta stimata del microfono (allineata a 0 dB sul livello a 1 kHz)
  if (a.spettro) {
    const mic = DB.curve[t.microfono];
    const i1k = a.spettro.f.findIndex((f) => f >= 1000), base = a.spettro.db[i1k] ?? -60;
    const ys = a.spettro.db.filter((v) => v != null);
    lineChart($("cSpec"), [
      { x: a.spettro.f, y: a.spettro.db, color: color(t) },
      { x: DB.f, y: mic.risposta.map((v) => v + base), color: css("--b"), w: 1.5 },
    ], { xlog: true, ymin: Math.min(...ys) - 6, ymax: Math.max(...ys) + 6, xlabel: kHz, ylabel: (v) => `${Math.round(v)}` });
  }
  const lc = a.lufs_curva;
  if (lc.length) lineChart($("cLufs"), [{ x: lc.map((_, i) => i), y: lc, color: css("--ok") }],
    { ymin: Math.max(-60, Math.min(...lc) - 3), ymax: Math.max(...lc) + 3, xlabel: (v) => fmt(v).split(".")[0], ylabel: (v) => `${v}` });
}

// avvisi della catena registratore + microfono, più il controllo sul formato reale del file
function chainRisks(t) {
  const rec = DB.registratori[t.registratore], mic = DB.microfoni[t.microfono];
  const out = [...new Set([...(rec.rischi || []), ...(mic.rischi || [])])].map((r) => DB.rischi[r]);
  const bits = t.info.bits;
  if (bits && rec.bit.length && !rec.bit.includes(bits)) out.unshift(`Il file è a ${bits === 32 ? "32 bit float" : bits + " bit"}: ${rec.nome} non registra così, controlla il registratore`);
  return out;
}

// --- dispositivo --------------------------------------------------------------------
function specRows(obj, keys) {
  const fid = obj.fiducia || {};
  return keys.filter(([k]) => obj[k] != null && obj[k] !== "").map(([k, label, f = (v) => v]) =>
    `<tr><td>${label}</td><td>${f(obj[k])}<span class="f ${fid[k] || "ipotizzato"}">${fid[k] || "ipotizzato"}</span></td></tr>`).join("");
}
function renderDevice() {
  const t = selected();
  $("devEmpty").hidden = !!t; $("dev").hidden = !t;
  if (!t) return;
  const p = DB.profili.find((x) => x.id === t.profile), mic = DB.microfoni[t.microfono], rec = DB.registratori[t.registratore];
  $("devTitle").textContent = `${t.nome} → ${mic.nome} in ${rec.nome}`;
  $("devRole").textContent = `Ruolo nel mix: ${p.ruolo} · posizione tipica: ${p.posizione || "-"}${mic.note ? " · " + mic.note : ""}`;
  $("devMic").innerHTML = `<tr><td>Modello</td><td>${mic.nome}</td></tr>` + specRows(mic, [
    ["capsula", "Capsula"], ["diagramma", "Diagramma"], ["banda", "Banda", (b) => `${b[0]} Hz – ${b[1] / 1000} kHz`],
    ["sensibilita_mv_pa", "Sensibilità", (v) => `${v} mV/Pa`], ["rumore_dba", "Rumore proprio", (v) => `${v} dB(A)`], ["spl_max", "SPL max", (v) => `${v} dB`]]);
  $("devRec").innerHTML = `<tr><td>Modello</td><td>${rec.nome}</td></tr>` + specRows(rec, [
    ["formato", "Formato"], ["ein_dbu", "EIN preamp", (v) => `${v} dBu`], ["max_in_dbu_mic", "Max ingresso mic", (v) => `${v} dBu`],
    ["gamma_dinamica_db", "Gamma dinamica", (v) => `${v} dB`], ["clock_ppm", "Stabilità clock", (v) => `±${v} ppm`], ["timecode", "Timecode"], ["note", "Note"]]);
  const range = mic.spl_max && mic.rumore_dba ? `Gamma utile del microfono: ${mic.spl_max - mic.rumore_dba} dB (da ${mic.rumore_dba} a ${mic.spl_max} dB SPL)` : null;
  $("devRisks").innerHTML = [range, ...chainRisks(t)].filter(Boolean).map((w) => `<span class="chip">${w}</span>`).join("");
  const c = DB.curve[t.microfono];
  lineChart($("cEq"), [{ x: DB.f, y: c.risposta, color: css("--a") }, { x: DB.f, y: c.correzione, color: css("--b") }],
    { xlog: true, ymin: -18, ymax: 9, xlabel: kHz, ylabel: (v) => `${v} dB` });
  drawPolar($("cPolar"), c.polare);
  $("devSrc").innerHTML = [...(mic.fonti || []), ...(rec.fonti || [])].map((u, i) => `<a href="${u}" target="_blank" style="color:var(--accent)">[${i + 1}]</a>`).join(" ") || "nessuna (valori tipici)";
}
function drawPolar(cv, g) {
  const ctx = fit(cv), W = cv.width, R = W / 2 - 16 * devicePixelRatio, cx = W / 2, cy = W / 2;
  ctx.strokeStyle = css("--line"); ctx.lineWidth = devicePixelRatio;
  for (const r of [0.25, 0.5, 0.75, 1]) { ctx.beginPath(); ctx.arc(cx, cy, R * r, 0, 2 * Math.PI); ctx.stroke(); }
  ctx.beginPath(); ctx.moveTo(cx, cy - R); ctx.lineTo(cx, cy + R); ctx.moveTo(cx - R, cy); ctx.lineTo(cx + R, cy); ctx.stroke();
  ctx.strokeStyle = css("--a"); ctx.lineWidth = 2 * devicePixelRatio; ctx.beginPath();
  g.forEach((v, i) => { const th = (i / (g.length - 1)) * 2 * Math.PI; const x = cx + Math.sin(th) * v * R, y = cy - Math.cos(th) * v * R; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
  ctx.stroke();
  ctx.fillStyle = css("--muted"); ctx.font = `${10 * devicePixelRatio}px sans-serif`; ctx.fillText("0° fronte", cx + 4, cy - R + 10 * devicePixelRatio);
}

// --- scena 3D -------------------------------------------------------------------------
const scene = (() => {
  const box = $("scene"), sc = new THREE.Scene(), cam = new THREE.PerspectiveCamera(50, 1, 0.1, 500);
  const rend = new THREE.WebGLRenderer({ antialias: true });
  rend.setPixelRatio(devicePixelRatio); rend.setClearColor(0x121417); box.appendChild(rend.domElement);
  const ctl = new OrbitControls(cam, rend.domElement);
  sc.add(new THREE.HemisphereLight(0xffffff, 0x222233, 2.2));
  const room = new THREE.Group(); sc.add(room);
  const mics = new Map(), labels = new Map();
  const listener = new THREE.Mesh(new THREE.ConeGeometry(0.35, 0.9, 16), new THREE.MeshStandardMaterial({ color: 0xffffff }));
  listener.rotation.x = -Math.PI / 2; listener.userData.listener = true; sc.add(listener);
  const ray = new THREE.Raycaster(), floor = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  let drag = null, dragY = 0;

  function buildRoom() {
    room.clear();
    const { w, d, h } = S.sala;
    const walls = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(w, h, d + 4)), new THREE.LineBasicMaterial({ color: 0x3a414c }));
    walls.position.set(0, h / 2, (d - 4) / 2); room.add(walls);
    const grid = new THREE.GridHelper(Math.max(w, d + 4), Math.max(w, d + 4), 0x2e333b, 0x22262d); grid.position.z = (d - 4) / 2; room.add(grid);
    const stage = new THREE.Mesh(new THREE.BoxGeometry(Math.min(w, 12), 0.6, 4), new THREE.MeshStandardMaterial({ color: 0x3b2f4a }));
    stage.position.set(0, 0.3, -2); room.add(stage);
  }
  function sync() {
    if (!S) return;
    if (room.userData.key !== JSON.stringify(S.sala)) { buildRoom(); if (!room.userData.key) home(); room.userData.key = JSON.stringify(S.sala); }
    const ids = new Set(S.tracks.map((t) => t.id));
    for (const [id, m] of mics) if (!ids.has(id)) { sc.remove(m); mics.delete(id); labels.get(id).remove(); labels.delete(id); }
    for (const t of S.tracks) {
      let m = mics.get(t.id);
      if (!m) {
        m = new THREE.Mesh(new THREE.SphereGeometry(0.28, 20, 16), new THREE.MeshStandardMaterial({ color: color(t) }));
        m.userData.id = t.id; sc.add(m); mics.set(t.id, m);
        const l = document.createElement("div"); l.className = "lbl"; box.appendChild(l); labels.set(t.id, l);
      }
      if (drag !== m) m.position.set(...t.pos);
      m.material.color.set(color(t)); m.material.opacity = t.mute ? 0.3 : 1; m.material.transparent = t.mute;
      labels.get(t.id).textContent = `${t.nome}${t.pos_mode === "manuale" ? " ✋" : ""}`;
    }
    if (drag !== listener) listener.position.set(...S.listener);
  }
  function highlight() { for (const [id, m] of mics) m.scale.setScalar(id === sel ? 1.6 : 1); }
  function resize() { const r = box.getBoundingClientRect(); rend.setSize(r.width, r.height); cam.aspect = r.width / r.height; cam.updateProjectionMatrix(); }
  function pick(e) {
    const r = rend.domElement.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1), cam);
  }
  rend.domElement.addEventListener("pointerdown", (e) => {
    pick(e);
    const hit = ray.intersectObjects([...mics.values(), listener])[0];
    if (!hit) return;
    drag = hit.object; dragY = e.clientY; ctl.enabled = false;
    if (drag.userData.id) select(drag.userData.id);
  });
  addEventListener("pointermove", (e) => {
    if (!drag) return;
    if (e.shiftKey) { drag.position.y = Math.max(0, drag.position.y + (dragY - e.clientY) * 0.02); dragY = e.clientY; return; }
    pick(e); floor.constant = -0; const p = new THREE.Vector3();
    if (ray.ray.intersectPlane(floor, p)) { drag.position.x = p.x; drag.position.z = p.z; }
  });
  addEventListener("pointerup", () => {
    if (!drag) return;
    const pos = drag.position.toArray().map((v) => +v.toFixed(2));
    if (drag === listener) { S.listener = pos; push({ listener: pos }); }
    else { const t = S.tracks.find((x) => x.id === drag.userData.id); pushTrack(t, { pos, pos_mode: "manuale" }); }
    drag = null; ctl.enabled = true;
  });
  function home() { cam.position.set(S.sala.w * 0.9, S.sala.h * 2.2, S.sala.d + 8); ctl.target.set(0, 0, S.sala.d / 3); ctl.update(); }
  function top() { cam.position.set(0, Math.max(S.sala.w, S.sala.d) * 1.3, S.sala.d / 2); ctl.target.set(0, 0, S.sala.d / 2 - 2); ctl.update(); }
  function loop() {
    requestAnimationFrame(loop);
    if (box.offsetParent) {
      rend.render(sc, cam);
      const r = box.getBoundingClientRect();
      for (const [id, m] of mics) {
        const v = m.position.clone(); v.y += 0.3; v.project(cam);
        const l = labels.get(id); l.style.left = `${(v.x + 1) / 2 * r.width}px`; l.style.top = `${(1 - v.y) / 2 * r.height}px`; l.hidden = v.z > 1;
      }
    }
  }
  new ResizeObserver(resize).observe(box);
  loop();
  return { sync, highlight, top };
})();

// --- ascolto in tempo reale: blocchi renderizzati dal server, buffer in anticipo ------------
const player = (() => {
  const CHUNK = 1.0, AHEAD = 3; // secondi per blocco, blocchi in anticipo
  let ctx = null, an = null, playing = false, pos = 0, nextT = 0, nextWhen = 0, queue = [], bypass = false, timer = null, inflight = false, gen = 0;
  function init() {
    ctx = new AudioContext({ sampleRate: S.sr });
    const split = ctx.createChannelSplitter(2); an = [ctx.createAnalyser(), ctx.createAnalyser()];
    const gain = ctx.createGain(); gain.connect(ctx.destination); gain.connect(split);
    split.connect(an[0], 0); split.connect(an[1], 1); an.forEach((a) => (a.fftSize = 1024));
    ctx.out = gain; meters();
  }
  async function fill() {
    if (!playing || inflight) return;
    const [, end] = S.span;
    while (playing && nextWhen - ctx.currentTime < AHEAD * CHUNK && nextT < end) {
      inflight = true;
      const t0 = nextT, g = gen;
      const r = await fetch(`/api/render?t0=${t0}&dur=${CHUNK}&b=${bypass ? 1 : 0}`);
      if (g !== gen) return; // flush o stop nel frattempo: blocco vecchio scartato
      inflight = false;
      if (!r.ok) { toast((await r.json()).errore, true); stop(); return; }
      const lv = JSON.parse(r.headers.get("X-Levels") || "{}");
      const buf = await ctx.decodeAudioData(await r.arrayBuffer());
      const src = ctx.createBufferSource(); src.buffer = buf; src.connect(ctx.out);
      const when = Math.max(nextWhen, ctx.currentTime + 0.05);
      src.start(when);
      queue.push({ src, t0, when, lv });
      nextT += CHUNK; nextWhen = when + buf.duration;
    }
    if (nextT >= end && !queue.some((q) => q.when + CHUNK > ctx.currentTime)) stop();
  }
  function now() {
    if (!playing) return pos;
    const cur = [...queue].reverse().find((q) => q.when <= ctx.currentTime);
    return cur ? cur.t0 + (ctx.currentTime - cur.when) : pos;
  }
  function tick() {
    const t = now(), [s, e] = S.span;
    $("time").textContent = fmt(t);
    $("seekBar").style.width = `${((t - s) / (e - s || 1)) * 100}%`;
    $("bufBar").style.left = `${((t - s) / (e - s || 1)) * 100}%`;
    $("bufBar").style.width = playing ? `${((nextT - t) / (e - s || 1)) * 100}%` : "0";
    const cur = [...queue].reverse().find((q) => q.when <= ctx?.currentTime);
    if (cur) {
      for (const [id, db] of Object.entries(cur.lv)) { const m = document.querySelector(`[data-meter="${id}"]`); if (m) m.style.width = `${Math.max(0, (db + 60) / 60) * 100}%`; }
      $("lufsLive").textContent = `picco ${cur.lv.master} dBFS`;
      $("lufsLive").style.color = cur.lv.master > -1 ? css("--bad") : "";
    }
    queue = queue.filter((q) => q.when + CHUNK > (ctx?.currentTime ?? 0) - 1);
    fill();
  }
  function meters() {
    const d = new Float32Array(1024);
    const loop = () => { requestAnimationFrame(loop); an.forEach((a, i) => { a.getFloatTimeDomainData(d); let p = 0; for (const v of d) p = Math.max(p, Math.abs(v)); $(i ? "mR" : "mL").style.width = `${Math.max(0, (20 * Math.log10(p + 1e-9) + 60) / 60) * 100}%`; }); };
    loop();
  }
  function start(at) {
    if (!S.tracks.length) return toast("Nessuna traccia da ascoltare", true);
    if (!ctx) init();
    ctx.resume(); gen++; inflight = false; playing = true; pos = at ?? pos; nextT = pos; nextWhen = ctx.currentTime + 0.1; queue = [];
    $("bPlay").textContent = "❚❚"; clearInterval(timer); timer = setInterval(tick, 100); fill();
  }
  function stop() { pos = now(); gen++; playing = false; queue.forEach((q) => q.src.stop()); queue = []; $("bPlay").textContent = "▶"; }
  function flush() { // i parametri sono cambiati: butta il buffer non ancora suonato
    if (!playing) return;
    gen++;
    const keep = ctx.currentTime + 0.15;
    queue.filter((q) => q.when > keep).forEach((q) => q.src.stop());
    queue = queue.filter((q) => q.when <= keep);
    const last = queue[queue.length - 1];
    nextT = last ? last.t0 + CHUNK : now(); nextWhen = last ? last.when + CHUNK : ctx.currentTime + 0.1; inflight = false;
    fill();
  }
  function setBypass(b) { bypass = b; flush(); }
  return { start, stop, flush, setBypass, toggle: () => (playing ? stop() : start()), seek: (t) => (playing ? start(t) : ((pos = t), tick())), tick, get pos() { return pos; } };
})();

// --- lavori lunghi (analisi, stampa) con barra di avanzamento -------------------------------
async function runJob(path, body, label) {
  const { job } = await api(path, body);
  $("job").hidden = false;
  for (;;) {
    const j = await api(`/api/jobs/${job}`);
    $("jobMsg").textContent = `${label}: ${j.msg}`; $("jobBar").style.width = `${j.progress * 100}%`;
    if (j.done) { $("job").hidden = true; if (j.error) throw new Error(j.error); return j.result; }
    await new Promise((r) => setTimeout(r, 400));
  }
}

// --- comandi --------------------------------------------------------------------------
async function refresh() {
  S = await api("/api/state");
  $("pname").value = S.nome; $("roomW").value = S.sala.w; $("roomD").value = S.sala.d; $("roomH").value = S.sala.h;
  $("master").value = S.master_db; $("width").value = S.larghezza; $("atten").value = S.attenuazione; $("corr").checked = S.correzione;
  if (!selected()) sel = S.tracks[0]?.id ?? null;
  renderTracks(); scene.sync(); select(sel); player.tick();
}

$("pname").onchange = (e) => push({ nome: e.target.value }, false);
for (const k of ["roomW", "roomD", "roomH"]) $(k).onchange = () => { S.sala = { w: +$("roomW").value, d: +$("roomD").value, h: +$("roomH").value }; push({ sala: S.sala }); };
$("master").oninput = (e) => push({ master_db: +e.target.value });
$("width").oninput = (e) => push({ larghezza: +e.target.value });
$("atten").oninput = (e) => push({ attenuazione: +e.target.value });
$("corr").onchange = (e) => push({ correzione: e.target.checked });
$("bAuto").onclick = () => push({ tracks: S.tracks.map((t) => ({ id: t.id, pos_mode: "auto" })) });
$("bTop").onclick = () => scene.top();
$("bPlay").onclick = () => player.toggle();
$("bA").onclick = () => { $("bA").classList.add("on"); $("bB").classList.remove("on"); player.setBypass(false); };
$("bB").onclick = () => { $("bB").classList.add("on"); $("bA").classList.remove("on"); player.setBypass(true); };
$("seek").onclick = (e) => { const r = e.currentTarget.getBoundingClientRect(), [s, en] = S.span; player.seek(s + ((e.clientX - r.left) / r.width) * (en - s)); };
addEventListener("keydown", (e) => { if (e.code === "Space" && !["INPUT", "SELECT"].includes(e.target.tagName)) { e.preventDefault(); player.toggle(); } });
document.querySelectorAll(".tabs button").forEach((b) => (b.onclick = () => {
  document.querySelectorAll(".tabs button, .tab").forEach((x) => x.classList.remove("on"));
  b.classList.add("on"); $(`tab-${b.dataset.tab}`).classList.add("on"); renderAnalysis(); renderDevice();
}));
$("bAnalyze").onclick = safe(async () => {
  if (!S.tracks.length) return toast("Aggiungi prima delle tracce", true);
  await runJob("/api/analyze", {}, "Analisi"); await refresh(); toast("Analisi e sync completati");
});
$("bResolve").onclick = safe(async () => { S = await api("/api/resolve/import", {}); await refresh(); toast("Timeline di Resolve letta"); });
$("bSave").onclick = safe(async () => { const r = await api("/api/save", {}); toast(`Salvato in ${r.path}`); });
$("bQuit").onclick = async () => { if (!confirm("Chiudere MIX3D? Salva prima il progetto.")) return; player.stop(); await fetch("/api/quit", { method: "POST" }).catch(() => {}); document.body.innerHTML = "<p style='padding:40px'>MIX3D chiuso.</p>"; };
$("bOpen").onclick = () => $("dlgOpen").showModal();
$("opCancel").onclick = () => $("dlgOpen").close();
$("opOk").onclick = safe(async () => { await api("/api/load", { path: $("opPath").value }); $("dlgOpen").close(); await refresh(); });

// selettore file sul Mac (il browser non dà i percorsi: li elenca il server locale)
const picked = new Set();
async function browse(dir) {
  const r = await api(`/api/browse?dir=${encodeURIComponent(dir)}`);
  $("fsDir").textContent = r.dir; $("fsUp").onclick = () => browse(r.su);
  $("fsList").innerHTML = "";
  for (const v of r.voci) {
    const li = document.createElement("li");
    li.textContent = `${v.dir ? "📁" : "🎵"} ${v.nome}`; li.classList.toggle("sel", picked.has(v.path));
    li.onclick = () => { if (v.dir) return browse(v.path); picked.has(v.path) ? picked.delete(v.path) : picked.add(v.path); li.classList.toggle("sel"); $("fsCount").textContent = `${picked.size} selezionati`; };
    $("fsList").appendChild(li);
  }
}
$("bAdd").onclick = safe(async () => { picked.clear(); $("fsCount").textContent = ""; await browse(localStorage.getItem("mix3d.dir") || ""); $("dlgFiles").showModal(); });
$("fsCancel").onclick = () => $("dlgFiles").close();
$("fsOk").onclick = safe(async () => {
  try { localStorage.setItem("mix3d.dir", $("fsDir").textContent); } catch {}
  $("dlgFiles").close();
  if (!picked.size) return;
  toast("Lettura file…"); S = await api("/api/files", { paths: [...picked] }); await refresh();
  toast("Controlla i dispositivi suggeriti (bordo giallo) e avvia l'analisi");
});

$("bPrint").onclick = () => $("dlgPrint").showModal();
$("prCancel").onclick = () => $("dlgPrint").close();
$("prOk").onclick = safe(async () => {
  $("dlgPrint").close();
  const tr = $("prTrack").value, lufs = $("prLufs").value;
  const r = await runJob("/api/print", { path: $("prPath").value, target: tr ? +tr : $("prTarget").value, lufs: lufs === "" ? null : +lufs }, "Stampa");
  toast(`Stampato ${r.path}: ${r.lufs} LUFS, picco ${r.picco_dbfs} dBFS${r.traccia ? `, traccia A${r.traccia} in Resolve` : ""}`);
});

DB = await api("/api/devices");
await refresh();
