// MIX3D pannello guidato: 6 passi, scena 3D con spazi, dispositivi, lobi polari e sorgenti.
import * as THREE from "three";
import { OrbitControls } from "./vendor/OrbitControls.js";

const $ = (id) => document.getElementById(id);
const COLORS = ["#4fb3ff", "#f5b942", "#3ccf8e", "#ff7aa8", "#b38cff", "#ff8c42", "#5ee0e0", "#d4e157", "#ff5d5d", "#9aa5b1"];
const CAMERAS = new Set(["fx6", "fx30", "a6300", "osmo_action"]);
const PATTERN = { omni: 1, cardioide: 0.5, supercardioide: 0.37, ipercardioide: 0.25, figura8: 0, ms: 0.5 };
let S = null, DB = null, SPACES = [], sel = null, step = 0, printed = false;

// --- utilità ------------------------------------------------------------------
const api = async (path, body) => {
  const r = await fetch(path, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {});
  const j = await r.json();
  if (j.errore) throw new Error(j.errore);
  return j;
};
const toast = (msg, err) => { const t = $("toast"); t.textContent = msg; t.className = "toast" + (err ? " err" : ""); t.hidden = false; clearTimeout(t._h); t._h = setTimeout(() => (t.hidden = true), 4500); };
const safe = (fn) => async (...a) => { try { await fn(...a); } catch (e) { toast(e.message, true); } };
const fmt = (s) => `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, "0")}`;
const color = (t) => COLORS[S.tracks.indexOf(t) % COLORS.length];
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const space = () => SPACES.find((s) => s.id === S.spazio);
const selected = () => S.tracks.find((t) => t.id === sel);
const mic = (t) => DB.microfoni[t.microfono];
const rec = (t) => DB.registratori[t.registratore];
let pushT = null;
function push(patch, flush = true) { // modifica locale + invio al server con debounce
  clearTimeout(pushT);
  pushT = setTimeout(safe(async () => { S = await api("/api/state", patch); if (flush) player.flush(); scene.sync(); renderSummary(); }), 120);
}
const pushTrack = (t, fields) => { Object.assign(t, fields); push({ tracks: [{ id: t.id, ...fields }] }); };

// stato di salute di una traccia: ok / warn / bad
function health(t) {
  const a = t.analisi, sy = t.sync;
  if (!a) return "warn";
  if (a.clip_campioni > 0 || sy?.errore) return "bad";
  if (a.peak_dbfs > -1 || (sy && sy.fiducia < 0.4) || chainRisks(t).length > 2) return "warn";
  return "ok";
}

// --- passi guidati ------------------------------------------------------------
const STEPS = [
  { t: "Sorgenti", h: "Porta dentro le registrazioni: dalla timeline di Resolve o da file.", done: () => S.tracks.length > 0 },
  { t: "Dispositivi", h: "Per ogni traccia scegli registratore e microfono. MIX3D suggerisce, tu confermi.", done: () => S.tracks.length > 0 && S.tracks.every((t) => t.confermato) },
  { t: "Spazio", h: "Scegli il tipo di sala. Dimensioni, riverbero e consigli si aggiornano; i dispositivi si piazzano da soli.", done: () => !!S.spazio },
  { t: "Analisi", h: "Livelli, rumore, spettro, loudness, sync al campione e stima della posizione delle sorgenti.", done: () => S.tracks.length > 0 && S.tracks.every((t) => t.analisi) },
  { t: "Ascolto e mix", h: "Sposta ascoltatore, microfoni e sorgenti nella scena e ascolta in tempo reale.", done: () => S.tracks.some((t) => t.analisi) },
  { t: "Stampa", h: "Render del mix su file o direttamente in una traccia di Resolve.", done: () => printed },
];
function renderSteps() {
  $("steps").innerHTML = STEPS.map((s, i) => `<button data-i="${i}" class="${i === step ? "cur" : ""} ${s.done() ? "done" : ""}"><i>${s.done() ? "✓" : i + 1}</i>${s.t}</button>`).join("");
  $("steps").querySelectorAll("button").forEach((b) => (b.onclick = () => go(+b.dataset.i)));
}
function go(i) {
  step = Math.max(0, Math.min(STEPS.length - 1, i));
  document.querySelectorAll(".step").forEach((e) => e.classList.toggle("on", +e.dataset.step === step));
  $("stepNum").textContent = `Passo ${step + 1} di ${STEPS.length}`;
  $("stepTitle").textContent = STEPS[step].t; $("stepHelp").textContent = STEPS[step].h;
  $("bPrev").disabled = step === 0; $("bNext").hidden = step === STEPS.length - 1;
  const slot = { 2: "sceneSlot3", 4: "sceneSlot5" }[step];
  $("sceneWrap").hidden = !slot;
  if (slot) $(slot).appendChild($("sceneWrap"));
  try { localStorage.setItem("mix3d.step", step); } catch {}
  renderSteps(); renderStep();
}
function renderStep() {
  if (step === 1) renderDevice();
  if (step === 2) renderSpaces();
  if (step === 3) { renderHealth(); renderAnalysis(); }
  if (step === 4) renderMixSide();
}

// --- riepilogo in alto -----------------------------------------------------------
function renderSummary() {
  const ts = S.tracks, n = ts.length, conf = ts.filter((t) => t.confermato).length;
  const synced = ts.filter((t) => t.sync && !t.sync.errore).length + (S.riferimento ? 1 : 0);
  const clips = ts.reduce((a, t) => a + (t.analisi?.clip_campioni || 0), 0);
  const peaks = ts.filter((t) => t.analisi).map((t) => t.analisi.peak_dbfs);
  const sp = space(), [s0, s1] = S.span || [0, 0];
  const k = [
    ["Tracce", n || "–", n ? "ok" : ""],
    ["Dispositivi", n ? `${conf}/${n}` : "–", conf === n && n ? "ok" : "warn"],
    ["Spazio", sp ? sp.nome : "da scegliere", sp ? "ok" : "warn"],
    ["Sync", n ? `${Math.min(synced, n)}/${n}` : "–", synced >= n && n ? "ok" : ""],
    ["Durata", s1 > s0 ? fmt(s1 - s0).split(".")[0] : "–", ""],
    ["Picco max", peaks.length ? `${Math.max(...peaks)} dBFS` : "–", peaks.some((p) => p > -1) ? "warn" : ""],
    ["Saturazioni", peaks.length ? clips : "–", clips ? "bad" : peaks.length ? "ok" : ""],
    ["Sorgenti", (S.sorgenti || []).length || "–", ""],
  ];
  $("summary").innerHTML = k.map(([a, b, c]) => `<div class="kpi ${c}"><span>${a}</span><b>${b}</b></div>`).join("");
  $("confPill").textContent = n ? `${conf} di ${n} confermati` : "";
  renderSteps();
}

// --- tracce -------------------------------------------------------------------
function syncBadge(t) {
  const sy = t.sync;
  if (t.id === S.riferimento) return `<span class="badge ok">riferimento</span>`;
  if (!sy) return `<span class="badge">da sincronizzare</span>`;
  if (sy.errore) return `<span class="badge bad" title="${sy.errore}">sync fallito</span>`;
  const c = sy.fiducia > 0.6 ? "ok" : sy.fiducia > 0.3 ? "warn" : "bad";
  return `<span class="badge ${c}" title="residuo ${sy.residuo_us} µs, fiducia ${sy.fiducia}">${t.offset_s.toFixed(3)} s</span>`;
}
function renderTracks() {
  const box = $("tracks");
  box.innerHTML = "";
  $("emptyTracks").hidden = S.tracks.length > 0;
  $("trkCount").textContent = S.tracks.length ? `${S.tracks.length}` : "";
  for (const t of S.tracks) {
    const el = document.createElement("div");
    el.className = "trk" + (t.id === sel ? " sel" : "");
    el.style.setProperty("--c", color(t));
    el.innerHTML = `
      <div class="top-row"><span class="dot ${t.confermato ? health(t) : "warn"}"></span><span class="name" title="${t.file}">${t.nome}</span>${syncBadge(t)}
        <button class="ms m ${t.mute ? "on" : ""}" title="Muto">M</button><button class="ms s ${t.solo ? "on" : ""}" title="Solo">S</button></div>
      <div class="sub">${mic(t).nome} › ${rec(t).nome}${t.confermato ? "" : " · da confermare"}</div>
      <canvas></canvas>
      <div class="meter"><i data-meter="${t.id}"></i></div>
      <div class="ctl"><span class="muted small">Gain</span><input type="range" min="-30" max="12" step="0.5" value="${t.gain_db}"><span class="small gv">${t.gain_db.toFixed(1)} dB</span></div>`;
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
  const ctx = fit(cv), W = cv.width, H = cv.height, ov = t.analisi?.overview;
  ctx.fillStyle = css("--panel2"); ctx.fillRect(0, 0, W, H);
  if (!ov) { ctx.fillStyle = css("--muted"); ctx.font = `${10 * devicePixelRatio}px sans-serif`; ctx.fillText("analisi da fare", 6, H / 2 + 4); return; }
  ctx.fillStyle = color(t);
  const n = ov.max.length;
  for (let i = 0; i < n; i++) {
    const y0 = H / 2 - ov.max[i] * H / 2, y1 = H / 2 - ov.min[i] * H / 2;
    ctx.fillRect((i / n) * W, y0, Math.max(W / n, 1), Math.max(y1 - y0, 1));
  }
}
function select(id) {
  sel = id;
  document.querySelectorAll(".trk").forEach((e, i) => e.classList.toggle("sel", S.tracks[i]?.id === id));
  scene.highlight(); renderStep();
}

// --- grafici su canvas ----------------------------------------------------------
function fit(cv) {
  const r = cv.getBoundingClientRect();
  cv.width = Math.max(r.width, 50) * devicePixelRatio;
  cv.height = (cv.classList.contains("square") ? r.width : (+cv.getAttribute("height") || r.height)) * devicePixelRatio;
  return cv.getContext("2d");
}
function lineChart(cv, series, { xlog = false, ymin, ymax, xlabel = (v) => v, ylabel = (v) => v } = {}) {
  const ctx = fit(cv), W = cv.width, H = cv.height, d = devicePixelRatio, pad = 34 * d;
  const xs = series.flatMap((s) => s.x).filter((v) => v != null), tx = xlog ? Math.log10 : (v) => v;
  const x0 = tx(Math.min(...xs)), x1 = tx(Math.max(...xs));
  const X = (v) => pad + ((tx(v) - x0) / (x1 - x0 || 1)) * (W - pad - 8 * d);
  const Y = (v) => 8 * d + (1 - (v - ymin) / (ymax - ymin || 1)) * (H - pad);
  ctx.font = `${10 * d}px sans-serif`; ctx.fillStyle = css("--muted"); ctx.strokeStyle = css("--line"); ctx.lineWidth = d;
  for (const v of niceTicks(ymin, ymax, 5)) { ctx.beginPath(); ctx.moveTo(pad, Y(v)); ctx.lineTo(W, Y(v)); ctx.stroke(); ctx.fillText(ylabel(v), 2 * d, Y(v) + 3 * d); }
  const xt = xlog ? [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000] : niceTicks(Math.min(...xs), Math.max(...xs), 6);
  for (const v of xt) ctx.fillText(xlabel(v), X(v) - 8 * d, H - 6 * d);
  for (const s of series) {
    ctx.strokeStyle = s.color; ctx.lineWidth = (s.w || 2) * d; ctx.beginPath();
    let started = false;
    s.x.forEach((xv, i) => { const yv = s.y[i]; if (yv == null) { started = false; return; } const px = X(xv), py = Y(Math.max(ymin, Math.min(ymax, yv))); started ? ctx.lineTo(px, py) : ctx.moveTo(px, py); started = true; });
    ctx.stroke();
  }
}
function barChart(cv, labels, values, { max, unit = "" }) {
  const ctx = fit(cv), W = cv.width, H = cv.height, d = devicePixelRatio, n = values.length, bw = W / n;
  ctx.font = `${10 * d}px sans-serif`; ctx.textAlign = "center";
  values.forEach((v, i) => {
    const h = (v / max) * (H - 30 * d), x = i * bw + bw * 0.18;
    const g = ctx.createLinearGradient(0, H - 16 * d - h, 0, H - 16 * d); g.addColorStop(0, css("--accent2")); g.addColorStop(1, css("--accent"));
    ctx.fillStyle = g; ctx.fillRect(x, H - 16 * d - h, bw * 0.64, h);
    ctx.fillStyle = css("--text"); ctx.fillText(`${v}${unit}`, x + bw * 0.32, H - 20 * d - h);
    ctx.fillStyle = css("--muted"); ctx.fillText(labels[i], x + bw * 0.32, H - 3 * d);
  });
}
function niceTicks(a, b, n) {
  const p = Math.pow(10, Math.floor(Math.log10((b - a) / n || 1)));
  const step = p * [1, 2, 5, 10].find((m) => (b - a) / (p * m) <= n);
  const out = []; for (let v = Math.ceil(a / step) * step; v <= b; v += step) out.push(+v.toFixed(6)); return out;
}
const kHz = (v) => (v >= 1000 ? `${v / 1000}k` : `${v}`);

// --- passo 2: dispositivi ------------------------------------------------------------
function chainRisks(t) {
  const r = rec(t), m = mic(t);
  const out = [...new Set([...(r.rischi || []), ...(m.rischi || [])])].map((x) => DB.rischi[x]);
  const bits = t.info.bits;
  if (bits && r.bit.length && !r.bit.includes(bits)) out.unshift(`Il file è a ${bits === 32 ? "32 bit float" : bits + " bit"}: ${r.nome} non registra così, controlla il registratore`);
  return out;
}
function specRows(obj, keys) {
  const fid = obj.fiducia || {};
  return keys.filter(([k]) => obj[k] != null && obj[k] !== "").map(([k, label, f = (v) => v]) =>
    `<tr><td>${label}</td><td>${f(obj[k])}<span class="f ${fid[k] || "ipotizzato"}">${fid[k] || "ipotizzato"}</span></td></tr>`).join("");
}
const options = (entries, cur) => entries.map(([k, n]) => `<option value="${k}" ${k === cur ? "selected" : ""}>${n}</option>`).join("");
function renderDevice() {
  const t = selected();
  $("devEmpty").hidden = !!t; $("dev").hidden = !t;
  if (!t) return;
  const sug = new Set(t.suggeriti.map((s) => s.id));
  $("dProf").innerHTML = t.suggeriti.map((s) => `<option value="${s.id}">★ ${s.nome} (${Math.round(s.confidenza * 100)}%)</option>`).join("")
    + `<option disabled>──────────</option>` + DB.profili.filter((p) => !sug.has(p.id)).map((p) => `<option value="${p.id}">${p.nome}</option>`).join("");
  $("dProf").value = t.profile;
  $("dRec").innerHTML = options(Object.entries(DB.registratori).map(([k, r]) => [k, r.nome]), t.registratore);
  $("dMic").innerHTML = options(Object.entries(DB.microfoni).map(([k, m]) => [k, m.nome]), t.microfono);
  const p = DB.profili.find((x) => x.id === t.profile), m = mic(t), r = rec(t);
  $("devTitle").textContent = `${t.nome}: ${m.nome} › ${r.nome}`;
  $("devRole").textContent = `Ruolo nel mix: ${p?.ruolo || "-"} · posizione tipica: ${p?.posizione || "-"} · file ${t.info.bits === 32 ? "32 bit float" : (t.info.bits || "?") + " bit"}, ${t.info.sr / 1000} kHz`;
  const why = t.suggeriti[0]?.motivi || [];
  $("devWhy").innerHTML = t.confermato ? `<b>Confermato.</b> ${m.note || ""}` : `<b>Suggerito</b> perché: ${why.join(", ") || "nessun indizio dal file"}. <button id="bConfirm" class="primary small">Conferma</button>`;
  $("bConfirm")?.addEventListener("click", () => setChain(t, { confermato: true }));
  $("devMic").innerHTML = specRows(m, [
    ["capsula", "Capsula"], ["diagramma", "Diagramma"], ["banda", "Banda", (b) => `${b[0]} Hz – ${b[1] / 1000} kHz`],
    ["sensibilita_mv_pa", "Sensibilità", (v) => `${v} mV/Pa`], ["rumore_dba", "Rumore proprio", (v) => `${v} dB(A)`], ["spl_max", "SPL max", (v) => `${v} dB`]]);
  $("devRec").innerHTML = specRows(r, [
    ["formato", "Formato"], ["ein_dbu", "EIN preamp", (v) => `${v} dBu`], ["max_in_dbu_mic", "Max ingresso mic", (v) => `${v} dBu`],
    ["gamma_dinamica_db", "Gamma dinamica", (v) => `${v} dB`], ["clock_ppm", "Stabilità clock", (v) => `±${v} ppm`], ["timecode", "Timecode"], ["note", "Note"]]);
  const range = m.spl_max && m.rumore_dba ? `Gamma utile: ${m.spl_max - m.rumore_dba} dB (da ${m.rumore_dba} a ${m.spl_max} dB SPL)` : null;
  $("devRisks").innerHTML = [range, ...chainRisks(t)].filter(Boolean).map((w) => `<span class="chip">${w}</span>`).join("");
  const c = DB.curve[t.microfono];
  lineChart($("cEq"), [{ x: DB.f, y: c.risposta, color: css("--a") }, { x: DB.f, y: c.correzione, color: css("--b") }],
    { xlog: true, ymin: -18, ymax: 9, xlabel: kHz, ylabel: (v) => `${v} dB` });
  drawPolar($("cPolar"), c.polare);
  $("devSrc").innerHTML = [...(m.fonti || []), ...(r.fonti || [])].map((u, i) => `<a href="${u}" target="_blank" style="color:var(--accent)">[${i + 1}]</a>`).join(" ") || "nessuna (valori tipici)";
}
function setChain(t, fields) { pushTrack(t, fields); setTimeout(refresh, 300); }
$("dProf").onchange = (e) => setChain(selected(), { profile: e.target.value, confermato: true });
$("dRec").onchange = (e) => setChain(selected(), { registratore: e.target.value, confermato: true });
$("dMic").onchange = (e) => setChain(selected(), { microfono: e.target.value, confermato: true });
$("bConfirmAll").onclick = () => { push({ tracks: S.tracks.map((t) => ({ id: t.id, confermato: true })) }); setTimeout(refresh, 300); };
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

// --- passo 3: spazio -----------------------------------------------------------------
function renderSpaces() {
  $("spaces").innerHTML = SPACES.map((s) => `<button class="space ${s.id === S.spazio ? "on" : ""}" data-id="${s.id}">
    <span class="tag ${s.privato ? "priv" : ""}">${s.privato ? "privato" : s.tipo}</span><b>${s.nome}</b>
    <span>${s.sala.w}×${s.sala.d}×${s.sala.h} m${s.posti ? ` · ${s.posti} posti` : ""}${s.rt60?.["500"] ? ` · RT60 ${s.rt60["500"]} s` : ""}</span></button>`).join("");
  $("spaces").querySelectorAll(".space").forEach((b) => (b.onclick = safe(async () => {
    S = await api("/api/spazio", { id: b.dataset.id }); await refresh(); scene.home(); toast(`Spazio: ${space().nome}`);
  })));
  renderSpaceInfo();
}
function renderSpaceInfo() {
  const sp = space();
  if (!sp) { $("spaceInfo").innerHTML = `<div class="empty">Scegli uno spazio a sinistra: è il punto di partenza per posizioni, riverbero e consigli.</div>`; return; }
  const tiles = [["Volume", sp.volume_m3 ? `${sp.volume_m3.toLocaleString("it")} m³` : "-"], ["Posti", sp.posti || "-"],
    ["RT60 a 500 Hz", sp.rt60?.["500"] ? `${sp.rt60["500"]} s` : "-"], ["Distanza critica", sp.distanza_critica ? `${sp.distanza_critica} m` : "-"],
    ["Palco", `${sp.palco.w}×${sp.palco.d} m`], ["All'aperto", sp.aperto ? "sì" : "no"]];
  $("spaceInfo").innerHTML = `
    <div class="panel"><h4>${sp.nome}</h4><p class="muted">${sp.descrizione || ""}</p>
      <div class="tiles">${tiles.map(([k, v]) => `<div class="tile"><span>${k}</span><b>${v}</b></div>`).join("")}</div></div>
    <div class="panel"><h4>Tempo di riverbero per banda</h4><canvas id="cRt" class="chart" height="150"></canvas>
      <p class="muted small">Oltre la distanza critica (anello tratteggiato nella scena) domina il riverbero: lì i mic d'ambiente, prima i mic di presenza.</p></div>
    <div class="panel"><h4>Consigli di ripresa</h4><ul>${(sp.consigli || []).map((c) => `<li>${c}</li>`).join("") || "<li class='muted'>Nessuno</li>"}</ul></div>
    <div class="panel"><h4>Quanto ogni mic "vede" le sorgenti</h4>${polarMatrix()}</div>`;
  const rt = sp.rt60 || {}, bands = Object.keys(rt);
  if (bands.length) barChart($("cRt"), bands, bands.map((b) => rt[b]), { max: Math.max(...Object.values(rt)) * 1.2, unit: " s" });
}
function polarMatrix() {
  const src = S.sorgenti || [], ms = S.tracks.filter((t) => mic(t).diagramma !== "nessuno");
  if (!src.length || !ms.length) return `<p class="muted">Aggiungi sorgenti con "+ Sorgente…" sotto la scena (o lancia l'analisi per stimarle): qui vedrai il guadagno polare di ogni microfono verso ognuna.</p>`;
  const cell = (t, s) => { const g = polarGainDb(t, s.pos); const c = g > -3 ? "ok" : g > -10 ? "warn" : "bad"; return `<td><span class="badge ${c}">${g.toFixed(0)} dB</span></td>`; };
  return `<table class="health"><tr><th>Mic</th>${src.map((s) => `<th>${s.nome}</th>`).join("")}</tr>
    ${ms.map((t) => `<tr><td>${t.nome}</td>${src.map((s) => cell(t, s)).join("")}</tr>`).join("")}</table>`;
}

// direzione del mic: da orient [yaw, pitch] in gradi, altrimenti verso il centro del palco
function micDir(t) {
  if (t.orient) {
    const [y, p] = t.orient.map((v) => (v * Math.PI) / 180);
    return new THREE.Vector3(Math.sin(y) * Math.cos(p), Math.sin(p), -Math.cos(y) * Math.cos(p));
  }
  const target = new THREE.Vector3(0, (S.palco?.h || 0.6) + 1.5, -(S.palco?.d || 4) / 2);
  return target.sub(new THREE.Vector3(...t.pos)).normalize();
}
const polarR = (a, cos) => Math.abs(a + (1 - a) * cos);
function polarGainDb(t, pos) {
  const a = PATTERN[mic(t).diagramma] ?? 1, v = new THREE.Vector3(...pos).sub(new THREE.Vector3(...t.pos)).normalize();
  return 20 * Math.log10(Math.max(polarR(a, micDir(t).dot(v)), 1e-3));
}

// --- passo 4: analisi ------------------------------------------------------------------
function renderHealth() {
  const ts = S.tracks;
  $("health").innerHTML = !ts.length ? "" : `<tr><th></th><th>Traccia</th><th>Dispositivo</th><th>Picco</th><th>Rumore</th><th>LUFS</th><th>Saturati</th><th>Sync</th></tr>` +
    ts.map((t) => { const a = t.analisi || {}; return `<tr data-id="${t.id}" class="${t.id === sel ? "sel" : ""}"><td><span class="dot ${health(t)}"></span></td><td>${t.nome}</td>
      <td class="muted">${mic(t).nome}</td><td>${a.peak_dbfs ?? "–"}</td><td>${a.rumore_dbfs ?? "–"}</td><td>${a.lufs ?? "–"}</td><td>${a.clip_campioni ?? "–"}</td><td>${syncBadge(t)}</td></tr>`; }).join("");
  $("health").querySelectorAll("tr[data-id]").forEach((r) => (r.onclick = () => select(r.dataset.id)));
}
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
  const cv = $("cWave"), ctx = fit(cv), W = cv.width, H = cv.height, n = a.overview.max.length;
  for (let i = 0; i < n; i++) {
    const y0 = H / 2 - a.overview.max[i] * H / 2, y1 = H / 2 - a.overview.min[i] * H / 2;
    ctx.fillStyle = Math.max(a.overview.max[i], -a.overview.min[i]) >= 0.999 ? css("--bad") : color(t);
    ctx.fillRect((i / n) * W, y0, Math.max(W / n, 1), Math.max(y1 - y0, 1));
  }
  if (a.spettro) {
    const c = DB.curve[t.microfono], i1k = a.spettro.f.findIndex((f) => f >= 1000), base = a.spettro.db[i1k] ?? -60;
    const ys = a.spettro.db.filter((v) => v != null);
    lineChart($("cSpec"), [{ x: a.spettro.f, y: a.spettro.db, color: color(t) }, { x: DB.f, y: c.risposta.map((v) => v + base), color: css("--b"), w: 1.5 }],
      { xlog: true, ymin: Math.min(...ys) - 6, ymax: Math.max(...ys) + 6, xlabel: kHz, ylabel: (v) => `${Math.round(v)}` });
  }
  const lc = a.lufs_curva;
  if (lc.length) lineChart($("cLufs"), [{ x: lc.map((_, i) => i), y: lc, color: css("--ok") }],
    { ymin: Math.max(-60, Math.min(...lc) - 3), ymax: Math.max(...lc) + 3, xlabel: (v) => fmt(v).split(".")[0], ylabel: (v) => `${v}` });
}

// --- passo 5: mix -----------------------------------------------------------------------
function renderMixSide() {
  $("oMaster").textContent = `${(+S.master_db).toFixed(1)} dB`;
  $("oWidth").textContent = `${Math.round(S.larghezza * 100)}%`;
  $("oAtten").textContent = `${Math.round(S.attenuazione * 100)}%`;
  $("mixMeters").innerHTML = S.tracks.map((t) => `<div><span style="color:${color(t)}">${t.nome}</span><div class="meter"><i data-meter="${t.id}"></i></div></div>`).join("");
}

// --- scena 3D -------------------------------------------------------------------------
const scene = (() => {
  const box = $("scene"), sc = new THREE.Scene(), cam = new THREE.PerspectiveCamera(50, 1, 0.1, 800);
  const rend = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  rend.setPixelRatio(devicePixelRatio); rend.setClearColor(0x0b0e14, 1); box.appendChild(rend.domElement);
  const ctl = new OrbitControls(cam, rend.domElement);
  ctl.enableDamping = true;
  sc.add(new THREE.HemisphereLight(0xdfe8ff, 0x1a1d26, 2.0));
  const sun = new THREE.DirectionalLight(0xffffff, 1.2); sun.position.set(10, 30, 20); sc.add(sun);
  sc.fog = new THREE.Fog(0x0b0e14, 60, 260);
  const room = new THREE.Group(), devs = new Map(), lobes = new Map(), srcs = new Map(), labels = new Map();
  sc.add(room);
  const listener = new THREE.Mesh(new THREE.ConeGeometry(0.35, 0.9, 20), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0x333333 }));
  listener.rotation.x = -Math.PI / 2; listener.userData = { kind: "listener" }; sc.add(listener);
  const ray = new THREE.Raycaster(), floor = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
  let drag = null, last = null;

  const mat = (c, o = 1) => new THREE.MeshStandardMaterial({ color: c, transparent: o < 1, opacity: o, roughness: 0.85 });
  const add = (geo, m, x, y, z) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); room.add(o); return o; };
  const boxAt = (w, h, d, x, y, z, c, o) => add(new THREE.BoxGeometry(w, h, d), mat(c, o), x, y, z);
  const lineLoop = (pts, y, c) => room.add(new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts.map(([x, z]) => new THREE.Vector3(x, y, z))), new THREE.LineBasicMaterial({ color: c })));
  const ELEM_COLOR = { palco: 0x3b2f4a, platea: 0x1d2a3a, galleria: 0x34405a, boccascena: 0x4a3a2a, cappella: 0x2f3a2f, coro: 0x3a3550, organo: 0x5a4a2a };

  // elementi a poligono (file privati): estrusi dal pavimento, o lastra a quota per gallerie e cori
  function polyElement(e, h) {
    if (e.punto) return boxAt(0.6, 2.2, 0.15, e.punto[0], 1.1, e.punto[1], 0x8a6a3a);
    const shape = new THREE.Shape(e.poligono.map(([x, z]) => new THREE.Vector2(x, -z)));
    const base = e.quota ?? 0, top = e.quota != null ? 0.3 : Math.max(e.altezza || 0, 0.02);
    const geo = new THREE.ExtrudeGeometry(shape, { depth: Math.min(top, h), bevelEnabled: false });
    geo.rotateX(-Math.PI / 2);
    const o = new THREE.Mesh(geo, mat(ELEM_COLOR[e.tipo] ?? 0x2a3140, e.tipo === "platea" ? 0.6 : 0.9));
    o.position.y = base; room.add(o);
  }
  // elementi parametrici dei preset inclusi
  const BUILD = {
    box: (e) => boxAt(...e.size, ...e.pos, e.colore || 0x3a3f4a, 0.85),
    palchi: (e, s) => {
      const { w, d } = s.sala, p = e.profondita;
      for (let i = 0; i < e.ordini; i++) {
        const y = 1.8 + i * e.altezza;
        boxAt(p, 0.25, d - 2, -w / 2 + p / 2, y, d / 2 + 1, 0x6a2a35, 0.8);
        boxAt(p, 0.25, d - 2, w / 2 - p / 2, y, d / 2 + 1, 0x6a2a35, 0.8);
        boxAt(w, 0.25, p, 0, y, d - p / 2, 0x6a2a35, 0.8);
      }
    },
    colonne: (e) => {
      for (const x of e.x) for (let z = e.da; z <= e.a; z += e.passo) add(new THREE.CylinderGeometry(e.diametro / 2, e.diametro / 2, e.altezza, 16), mat(0x8c8577), x, e.altezza / 2, z);
    },
    gradinate: (e) => {
      const dz = (e.a - e.da) / e.file;
      for (let i = 0; i < e.file; i++) {
        const r = e.da + i * dz, h = (i + 1) * e.alzata;
        if (!e.arco) { boxAt(S.sala.w * 0.9, h, dz, 0, h / 2, r + dz / 2, 0x2b3242); continue; }
        const th = (e.arco * Math.PI) / 180;
        const g = new THREE.RingGeometry(r, r + dz * 0.95, 48, 1, Math.PI / 2 - th / 2 + Math.PI, th);
        g.rotateX(-Math.PI / 2);
        const o = add(g, mat(0x2b3242), 0, h, 0); o.material.side = THREE.DoubleSide;
      }
    },
    abside: (e, s) => {
      const g = new THREE.CylinderGeometry(e.raggio, e.raggio, s.sala.h, 32, 1, true, Math.PI / 2, Math.PI);
      const o = add(g, mat(0x4a4440, 0.35), 0, s.sala.h / 2, -s.palco.d); o.material.side = THREE.DoubleSide;
    },
    portico: (e, s) => {
      const { w, d } = s.sala, p = e.profondita, y = e.altezza;
      const z0 = -s.palco.d, D = d - z0, zc = (d + z0) / 2;
      boxAt(p, 0.3, D, -w / 2 + p / 2, y, zc, 0x6b5a48); boxAt(p, 0.3, D, w / 2 - p / 2, y, zc, 0x6b5a48);
      boxAt(w, 0.3, p, 0, y, z0 + p / 2, 0x6b5a48); boxAt(w, 0.3, p, 0, y, d - p / 2, 0x6b5a48);
    },
  };

  function buildRoom() {
    room.clear();
    const sp = space(), { w, d, h } = S.sala, pal = S.palco || { w: 12, d: 4, h: 0.6 }, z0 = -pal.d;
    const grid = new THREE.GridHelper(Math.max(w, d - z0) + 10, Math.max(w, d - z0) + 10, 0x253042, 0x182030);
    grid.position.z = (d + z0) / 2; room.add(grid);
    if (sp?.pianta?.poligono) {
      lineLoop(sp.pianta.poligono, 0.01, 0x5a6b88); lineLoop(sp.pianta.poligono, h, 0x2f3a4c);
      for (const e of sp.pianta.elementi || []) polyElement(e, h);
    } else {
      const walls = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(w, h, d - z0)), new THREE.LineBasicMaterial({ color: sp?.aperto ? 0x253042 : 0x4a5568 }));
      walls.position.set(0, h / 2, (d + z0) / 2); room.add(walls);
      boxAt(pal.w, pal.h, pal.d, 0, pal.h / 2, -pal.d / 2, 0x3b2f4a);
      for (const e of sp?.elementi || []) BUILD[e.tipo]?.(e, { ...sp, sala: S.sala, palco: pal });
    }
    if (sp?.distanza_critica) { // anello della distanza critica attorno al centro del palco
      const pts = Array.from({ length: 97 }, (_, i) => { const a = (i / 96) * 2 * Math.PI; return new THREE.Vector3(Math.sin(a) * sp.distanza_critica, 0.03, -pal.d / 2 + Math.cos(a) * sp.distanza_critica); });
      const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineDashedMaterial({ color: 0x8f7bff, dashSize: 0.4, gapSize: 0.3 }));
      l.computeLineDistances(); room.add(l);
    }
  }

  // icona del dispositivo: camera, mixer, registratore portatile o microfono
  function deviceMesh(t) {
    const g = new THREE.Group(), c = color(t), m = mat(c);
    if (CAMERAS.has(t.registratore)) {
      g.add(new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.3, 0.5), m));
      const lens = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.12, 0.3, 16), mat(0x222222)); lens.rotation.x = Math.PI / 2; lens.position.z = 0.38; g.add(lens);
    } else if (t.registratore === "mixer") {
      g.add(new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.12, 0.45), m));
    } else {
      const body = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 0.45, 12), m); body.rotation.x = Math.PI / 2; g.add(body);
      const cap = new THREE.Mesh(new THREE.SphereGeometry(0.1, 12, 10), mat(0xcccccc)); cap.position.z = 0.25; g.add(cap);
    }
    g.userData = { kind: "track", id: t.id };
    return g;
  }
  // lobo polare 3D: r(θ) = |a + (1-a)cos θ| attorno all'asse +z locale, scala 1.6 m
  function lobeMesh(a, c) {
    const geo = new THREE.SphereGeometry(1, 40, 24), p = geo.attributes.position, v = new THREE.Vector3();
    for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); v.multiplyScalar(1.6 * Math.max(polarR(a, v.z), 0.02)); p.setXYZ(i, v.x, v.y, v.z); }
    geo.computeVertexNormals();
    const g = new THREE.Group();
    g.add(new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: 0.22, depthWrite: false })));
    g.add(new THREE.LineSegments(new THREE.WireframeGeometry(geo), new THREE.LineBasicMaterial({ color: c, transparent: true, opacity: 0.35 })));
    return g;
  }
  function label(key, cls) {
    if (!labels.has(key)) { const l = document.createElement("div"); l.className = "lbl " + cls; box.appendChild(l); labels.set(key, l); }
    return labels.get(key);
  }
  function prune(map, keep, extra) {
    for (const [id, o] of map) if (!keep.has(id)) { sc.remove(o); map.delete(id); extra?.delete(id); labels.get(id)?.remove(); labels.delete(id); }
  }

  function sync() {
    if (!S) return;
    const key = JSON.stringify([S.sala, S.palco, S.spazio]);
    if (room.userData.key !== key) { const first = !room.userData.key; buildRoom(); room.userData.key = key; if (first) home(); }
    const ids = new Set(S.tracks.map((t) => t.id));
    prune(devs, ids); prune(lobes, ids);
    for (const t of S.tracks) {
      const sig = `${t.registratore}|${color(t)}`;
      let d = devs.get(t.id);
      if (d?.userData.sig !== sig) { if (d) sc.remove(d); d = deviceMesh(t); d.userData.sig = sig; sc.add(d); devs.set(t.id, d); }
      if (drag?.obj !== d) d.position.set(...t.pos);
      const dir = micDir(t);
      d.lookAt(d.position.clone().add(dir));
      label(t.id, "").textContent = `${t.nome}${t.pos_mode === "manuale" ? " ✋" : ""}`;
      const pat = mic(t).diagramma, lsig = `${pat}|${color(t)}`;
      let l = lobes.get(t.id);
      if (l?.userData.sig !== lsig) { if (l) sc.remove(l); l = pat === "nessuno" ? new THREE.Group() : lobeMesh(PATTERN[pat] ?? 1, color(t)); l.userData.sig = lsig; sc.add(l); lobes.set(t.id, l); }
      l.position.copy(d.position); l.lookAt(d.position.clone().add(dir));
      l.visible = $("showLobes").checked;
    }
    const sids = new Set((S.sorgenti || []).map((s) => s.id));
    prune(srcs, sids);
    for (const s of S.sorgenti || []) {
      let o = srcs.get(s.id);
      if (!o) { o = new THREE.Mesh(new THREE.OctahedronGeometry(0.32), new THREE.MeshStandardMaterial({ color: s.stimata ? 0xb38cff : 0xffc857, emissive: s.stimata ? 0x3a2a66 : 0x5a3a00 })); o.userData = { kind: "src", id: s.id }; sc.add(o); srcs.set(s.id, o); }
      if (drag?.obj !== o) o.position.set(...s.pos);
      o.visible = $("showSources").checked;
      label(s.id, "src").textContent = s.stimata ? `${s.nome} ±${s.errore_m} m` : s.nome;
    }
    if (drag?.obj !== listener) listener.position.set(...S.listener);
    highlight();
  }
  function highlight() { for (const [id, d] of devs) d.scale.setScalar(id === sel ? 1.5 : 1); }
  function resize() { const r = box.getBoundingClientRect(); if (!r.width) return; rend.setSize(r.width, r.height); cam.aspect = r.width / r.height; cam.updateProjectionMatrix(); }
  function pick(e) {
    const r = rend.domElement.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1), cam);
  }
  function hitObject(e) {
    pick(e);
    let o = ray.intersectObjects([...devs.values(), ...srcs.values(), listener], true)[0]?.object;
    while (o && !o.userData.kind) o = o.parent;
    return o;
  }
  rend.domElement.addEventListener("pointerdown", (e) => {
    const o = hitObject(e);
    if (!o) return;
    drag = { obj: o, rotate: e.altKey && o.userData.kind === "track" }; last = [e.clientX, e.clientY]; ctl.enabled = false;
    if (o.userData.kind === "track") select(o.userData.id);
  });
  rend.domElement.addEventListener("dblclick", (e) => {
    const o = hitObject(e);
    if (o?.userData.kind !== "src") return;
    S.sorgenti = S.sorgenti.filter((s) => s.id !== o.userData.id); push({ sorgenti: S.sorgenti }, false); sync();
  });
  addEventListener("pointermove", (e) => {
    if (!drag) return;
    const [dx, dy] = [e.clientX - last[0], e.clientY - last[1]]; last = [e.clientX, e.clientY];
    const o = drag.obj;
    if (drag.rotate) {
      const t = S.tracks.find((x) => x.id === o.userData.id), v = micDir(t);
      const yaw = (Math.atan2(v.x, -v.z) * 180) / Math.PI + dx * 0.6, pitch = Math.max(-85, Math.min(85, (Math.asin(v.y) * 180) / Math.PI - dy * 0.6));
      t.orient = [+yaw.toFixed(1), +pitch.toFixed(1)]; sync(); return;
    }
    if (e.shiftKey) { o.position.y = Math.max(0, o.position.y - dy * 0.02); return; }
    pick(e); const p = new THREE.Vector3();
    if (ray.ray.intersectPlane(floor, p)) { o.position.x = p.x; o.position.z = p.z; }
    if (o.userData.kind === "track") { lobes.get(o.userData.id)?.position.copy(o.position); }
  });
  addEventListener("pointerup", () => {
    if (!drag) return;
    const o = drag.obj, pos = o.position.toArray().map((v) => +v.toFixed(2)), k = o.userData.kind;
    const t = S.tracks.find((x) => x.id === o.userData.id);
    if (drag.rotate) pushTrack(t, { orient: t.orient });
    else if (k === "listener") { S.listener = pos; push({ listener: pos }); }
    else if (k === "src") { S.sorgenti.find((s) => s.id === o.userData.id).pos = pos; push({ sorgenti: S.sorgenti }, false); }
    else pushTrack(t, { pos, pos_mode: "manuale" });
    drag = null; ctl.enabled = true;
    if (step === 2) renderSpaceInfo();
  });
  function home() {
    const { w, d } = S.sala, pd = S.palco?.d || 4, R = Math.max(w, d + pd), zc = (d - pd) / 2;
    cam.position.set(R * 0.55, R * 0.6, zc + R * 0.85); ctl.target.set(0, 0, zc); ctl.update();
  }
  function top() { const { w, d } = S.sala, pd = S.palco?.d || 4, zc = (d - pd) / 2; cam.position.set(0, Math.max(w, d + pd) * 1.25, zc + 0.01); ctl.target.set(0, 0, zc); ctl.update(); }
  function loop() {
    requestAnimationFrame(loop);
    if (!box.offsetParent) return;
    ctl.update(); rend.render(sc, cam);
    const r = box.getBoundingClientRect();
    const place = (key, obj, dy) => {
      const l = labels.get(key); if (!l) return;
      const v = obj.position.clone(); v.y += dy; v.project(cam);
      l.style.left = `${(v.x + 1) / 2 * r.width}px`; l.style.top = `${(1 - v.y) / 2 * r.height}px`; l.hidden = v.z > 1 || !obj.visible;
    };
    for (const [id, d] of devs) place(id, d, 0.4);
    for (const [id, s] of srcs) place(id, s, 0.5);
  }
  new ResizeObserver(resize).observe(box);
  loop();
  return { sync, highlight, top, home };
})();

// --- ascolto in tempo reale: blocchi renderizzati dal server, buffer in anticipo ------------
const player = (() => {
  const CHUNK = 1.0, AHEAD = 3;
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
      if (g !== gen) return;
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
      for (const [id, db] of Object.entries(cur.lv)) document.querySelectorAll(`[data-meter="${id}"]`).forEach((m) => (m.style.width = `${Math.max(0, (db + 60) / 60) * 100}%`));
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
  function flush() {
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
  return { start, stop, flush, setBypass, toggle: () => (playing ? stop() : start()), seek: (t) => (playing ? start(t) : ((pos = t), tick())), tick };
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
  renderTracks(); renderSummary(); scene.sync(); renderStep(); player.tick();
}

$("bPrev").onclick = () => go(step - 1);
$("bNext").onclick = () => go(step + 1);
$("pname").onchange = (e) => push({ nome: e.target.value }, false);
for (const k of ["roomW", "roomD", "roomH"]) $(k).onchange = () => { S.sala = { w: +$("roomW").value, d: +$("roomD").value, h: +$("roomH").value }; push({ sala: S.sala }); };
const slider = (id, key) => ($(id).oninput = (e) => { S[key] = +e.target.value; renderMixSide(); push({ [key]: +e.target.value }); });
slider("master", "master_db"); slider("width", "larghezza"); slider("atten", "attenuazione");
$("corr").onchange = (e) => push({ correzione: e.target.checked });
$("showLobes").onchange = () => scene.sync();
$("showSources").onchange = () => scene.sync();
$("srcType").onchange = (e) => {
  const nome = e.target.value; e.target.value = "";
  if (!nome) return;
  const n = (S.sorgenti || []).length, pal = S.palco || { d: 4, h: 0.6 };
  S.sorgenti = [...(S.sorgenti || []), { id: `src_${Date.now()}`, nome, pos: [((n % 5) - 2) * 1.5, pal.h + 1.2, -pal.d / 2] }];
  push({ sorgenti: S.sorgenti }, false); scene.sync(); if (step === 2) renderSpaceInfo();
};
$("bAuto").onclick = () => { push({ tracks: S.tracks.map((t) => ({ id: t.id, pos_mode: "auto", orient: null })) }); setTimeout(refresh, 400); };
$("bTop").onclick = () => scene.top();
$("bPlay").onclick = () => player.toggle();
$("bA").onclick = () => { $("bA").classList.add("on"); $("bB").classList.remove("on"); player.setBypass(false); };
$("bB").onclick = () => { $("bB").classList.add("on"); $("bA").classList.remove("on"); player.setBypass(true); };
$("seek").onclick = (e) => { const r = e.currentTarget.getBoundingClientRect(), [s, en] = S.span; player.seek(s + ((e.clientX - r.left) / r.width) * (en - s)); };
addEventListener("keydown", (e) => { if (e.code === "Space" && !["INPUT", "SELECT"].includes(e.target.tagName)) { e.preventDefault(); player.toggle(); } });
$("bAnalyze").onclick = safe(async () => {
  if (!S.tracks.length) return toast("Aggiungi prima delle tracce", true);
  await runJob("/api/analyze", {}, "Analisi"); await refresh(); toast("Analisi e sync completati");
});
$("bResolve").onclick = safe(async () => { S = await api("/api/resolve/import", {}); await refresh(); toast("Timeline di Resolve letta"); go(1); });
$("bSave").onclick = safe(async () => { const r = await api("/api/save", {}); toast(`Salvato in ${r.path}`); });
$("bQuit").onclick = async () => { if (!confirm("Chiudere MIX3D? Salva prima il progetto.")) return; player.stop(); await fetch("/api/quit", { method: "POST" }).catch(() => {}); document.body.innerHTML = "<p style='padding:40px'>MIX3D chiuso.</p>"; };
$("bOpen").onclick = () => $("dlgOpen").showModal();
$("opCancel").onclick = () => $("dlgOpen").close();
$("opOk").onclick = safe(async () => { await api("/api/load", { path: $("opPath").value }); $("dlgOpen").close(); await refresh(); });

// selettore file sul Mac (il browser non dà i percorsi: li elenca il server locale)
const picked = new Set();
let pickMode = "audio";
async function browse(dir) {
  const ext = pickMode === "spazio" ? "&ext=json" : "";
  const r = await api(`/api/browse?dir=${encodeURIComponent(dir)}${ext}`);
  $("fsDir").textContent = r.dir; $("fsUp").onclick = () => browse(r.su);
  $("fsList").innerHTML = "";
  for (const v of r.voci) {
    const li = document.createElement("li");
    li.textContent = `${v.dir ? "📁" : pickMode === "spazio" ? "🏛" : "🎵"} ${v.nome}`; li.classList.toggle("sel", picked.has(v.path));
    li.onclick = () => {
      if (v.dir) return browse(v.path);
      if (pickMode === "spazio") picked.clear();
      picked.has(v.path) ? picked.delete(v.path) : picked.add(v.path);
      $("fsList").querySelectorAll("li").forEach((x) => x.classList.toggle("sel", x === li && picked.has(v.path)));
      if (pickMode === "audio") li.classList.toggle("sel", picked.has(v.path));
      $("fsCount").textContent = `${picked.size} selezionati`;
    };
    $("fsList").appendChild(li);
  }
}
async function openPicker(mode) {
  pickMode = mode; picked.clear(); $("fsCount").textContent = "";
  $("fsTitle").textContent = mode === "spazio" ? "Importa uno spazio (.json)" : "Aggiungi file audio o video";
  $("fsOk").textContent = mode === "spazio" ? "Importa" : "Aggiungi";
  let dir = ""; try { dir = localStorage.getItem(`mix3d.dir.${mode}`) || ""; } catch {}
  await browse(dir); $("dlgFiles").showModal();
}
$("bAdd").onclick = safe(() => openPicker("audio"));
$("bImportSpace").onclick = safe(() => openPicker("spazio"));
$("fsCancel").onclick = () => $("dlgFiles").close();
$("fsOk").onclick = safe(async () => {
  try { localStorage.setItem(`mix3d.dir.${pickMode}`, $("fsDir").textContent); } catch {}
  $("dlgFiles").close();
  if (!picked.size) return;
  if (pickMode === "spazio") {
    const sp = await api("/api/spazi/import", { path: [...picked][0] });
    SPACES = await api("/api/spazi");
    S = await api("/api/spazio", { id: sp.id }); await refresh(); scene.home();
    return toast(`Spazio importato: ${sp.nome}. Resta solo su questo Mac.`);
  }
  toast("Lettura file…"); S = await api("/api/files", { paths: [...picked] }); await refresh();
  toast("Controlla i dispositivi suggeriti"); go(1);
});

// integrazione in Resolve: stato e installazione
async function integr() {
  const st = await api("/api/resolve/integration");
  $("itStatus").innerHTML = !st.macos ? "Disponibile solo su macOS." :
    `Pannello: <b>${st.pannello ? "installato ✓" : "non installato"}</b> · Script: <b>${st.script ? "installato ✓" : "non installato"}</b>`;
}
$("bIntegr").onclick = safe(async () => { await integr(); $("dlgIntegr").showModal(); });
$("itClose").onclick = () => $("dlgIntegr").close();
const installIt = (pannello) => safe(async () => { await api("/api/resolve/install", { pannello }); await integr(); toast("Installato: riavvia Resolve"); });
$("itOk").onclick = installIt(true);
$("itScript").onclick = installIt(false);

$("prOk").onclick = safe(async () => {
  const tr = $("prTrack").value, lufs = $("prLufs").value, regione = $("prRegion").checked;
  const target = tr ? +tr : regione && $("prTarget").value === "file" ? "mix3d" : $("prTarget").value;
  const r = await runJob("/api/print", { path: $("prPath").value, target, regione, lufs: lufs === "" ? null : +lufs }, "Stampa");
  printed = true; renderSteps();
  $("printResult").innerHTML = `<div class="result">✓ ${r.path}<br>${r.lufs} LUFS · picco ${r.picco_dbfs} dBFS${r.traccia ? ` · traccia A${r.traccia} in Resolve` : ""}${r.sostituite ? ` · ${r.sostituite} stampa/e precedente/i sostituita/e` : ""}</div>`;
});

[DB, SPACES] = await Promise.all([api("/api/devices"), api("/api/spazi")]);
await refresh();
let saved = 0; try { saved = +(localStorage.getItem("mix3d.step") || 0); } catch {}
go(S.tracks.length ? saved : 0);

addEventListener("mix3d:eq", () => player.flush()); // l'EQ (eq.js) è cambiato: rifai l'ascolto
