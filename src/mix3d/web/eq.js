// Pannello EQ (passo "Ascolto e mix"): bande illimitate, dinamiche, auto-taratura spiegata.
// Trascina un punto: frequenza/guadagno. Rotella: Q. Doppio clic sul vuoto: nuova banda; su un punto: la togli.
const $ = (id) => document.getElementById(id);
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const TIPI = { campana: "Campana", shelf_basso: "Shelf basso", shelf_alto: "Shelf alto", passa_alto: "Passa-alto", passa_basso: "Passa-basso" };
const F0 = 20, F1 = 20000, GMAX = 18;
let tracks = [], master = [], st = {}, LOOKS = null, tid = null, bands = [], curve = null, focus = null, drag = null, saveT = null;

const api = async (path, body) => {
  const r = await fetch(path, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {});
  const j = await r.json();
  if (j.errore) throw new Error(j.errore);
  return j;
};
const fx = (f, W) => (Math.log(f / F0) / Math.log(F1 / F0)) * W;
const xf = (x, W) => F0 * (F1 / F0) ** (x / W);
const gy = (g, H) => H / 2 - (g / GMAX) * (H / 2);
const yg = (y, H) => ((H / 2 - y) / (H / 2)) * GMAX;
const cut = (b) => b.tipo.startsWith("passa");
const kHz = (f) => (f >= 1000 ? `${+(f / 1000).toFixed(1)}k` : `${Math.round(f)}`);

function mount() {
  const side = $("place"); // dopo Ascolto e Posizione
  if (!side || $("eqPanel")) return;
  side.insertAdjacentHTML("afterend", `<div id="eqPanel" class="panel eq">
    <h4>EQ dinamico</h4>
    <div class="eq-bar"><select id="eqTrack"></select>
      <button id="eqAuto" class="small primary" title="Analizza la traccia e propone le bande">Auto-tara</button>
      <button id="eqAutoAll" class="small" title="Tutte le tracce (con il mascheramento fra loro), poi il master">Tutte</button></div>
    <div id="lookBox" class="look" hidden>
      <label>Look <select id="lookSel"></select></label>
      <label>Carattere <select id="lookCar"></select></label>
      <label class="slider">Intensità <input type="range" id="lookAmt" min="0" max="1" step="0.05"><output id="oLookAmt"></output></label>
      <p id="lookDesc" class="hint"></p></div>
    <canvas id="eqCv" class="chart" height="200"></canvas>
    <p class="hint">Trascina i punti · rotella = Q · doppio clic = aggiungi/togli · viola tratteggiata = dinamiche al massimo · verde = look</p>
    <div id="eqList" class="eq-list"></div></div>`);
  $("eqTrack").onchange = (e) => select(e.target.value);
  $("eqAuto").onclick = () => auto([tid]);
  $("eqAutoAll").onclick = () => auto(null);
  $("lookSel").onchange = (e) => { const lk = LOOKS.look.find((l) => l.id === e.target.value); setLook({ look: lk?.id ?? null, look_carattere: lk?.carattere ?? "" }); };
  $("lookCar").onchange = (e) => setLook({ look_carattere: e.target.value });
  $("lookAmt").oninput = (e) => { $("oLookAmt").textContent = `${Math.round(e.target.value * 100)}%`; setLook({ look_intensita: +e.target.value }); };
  const cv = $("eqCv");
  cv.addEventListener("pointerdown", down);
  cv.addEventListener("pointermove", (e) => drag && move(e));
  cv.addEventListener("pointerup", () => (drag = null));
  cv.addEventListener("dblclick", dbl);
  cv.addEventListener("wheel", wheel, { passive: false });
  new IntersectionObserver((es) => es[0].isIntersecting && load()).observe($("eqPanel"));
  addEventListener("resize", draw);
}

async function load() {
  st = await api("/api/state");
  LOOKS ??= await api("/api/look");
  tracks = st.tracks; master = st.eq_master || [];
  if (tid !== "master" && !tracks.some((t) => t.id === tid)) tid = tracks[0]?.id ?? null;
  $("eqTrack").innerHTML = [...tracks, { id: "master", nome: "Master (tutto il mix)" }]
    .map((t) => `<option value="${t.id}" ${t.id === tid ? "selected" : ""}>${t.nome}</option>`).join("");
  if (tid) select(tid);
}

async function select(id) {
  tid = id;
  bands = structuredClone((id === "master" ? master : tracks.find((t) => t.id === id)?.eq) || []);
  focus = null;
  lookBox();
  await refresh();
}

function lookBox() { // uscita della pipeline: solo sul master
  $("lookBox").hidden = tid !== "master";
  const opt = (k, n, cur) => `<option value="${k}" ${k === cur ? "selected" : ""}>${n}</option>`;
  $("lookSel").innerHTML = opt("", "Nessun look (resta neutro)", st.look ?? "") + LOOKS.look.map((l) => opt(l.id, `${l.nome} · ${l.progetto}`, st.look)).join("");
  const car = st.look_carattere ?? LOOKS.look.find((l) => l.id === st.look)?.carattere ?? "";
  $("lookCar").innerHTML = opt("", "Nessuno", car) + Object.entries(LOOKS.caratteri).map(([k, n]) => opt(k, n, car)).join("");
  $("lookCar").disabled = !st.look;
  $("lookAmt").value = st.look_intensita ?? 1; $("oLookAmt").textContent = `${Math.round((st.look_intensita ?? 1) * 100)}%`;
  $("lookDesc").textContent = LOOKS.look.find((l) => l.id === st.look)?.descrizione ?? "Ogni mic entra raddrizzato a neutro; il look dà l'identità sonora al master.";
}

function setLook(patch) {
  Object.assign(st, patch);
  lookBox();
  clearTimeout(saveT);
  saveT = setTimeout(async () => { await api("/api/state", patch); dispatchEvent(new Event("mix3d:eq")); await refresh(); }, 90);
}

async function refresh() {
  curve = tid ? await api(`/api/eq/curve?track=${tid}`) : null;
  draw(); list();
}

function save() { // invio al server, curva aggiornata, ascolto rifatto
  clearTimeout(saveT);
  saveT = setTimeout(async () => {
    if (tid === "master") { await api("/api/state", { eq_master: bands }); master = structuredClone(bands); }
    else { await api("/api/state", { tracks: [{ id: tid, eq: bands }] }); tracks.find((t) => t.id === tid).eq = structuredClone(bands); }
    dispatchEvent(new Event("mix3d:eq"));
    await refresh();
  }, 90);
}

async function auto(ids) {
  const btn = ids ? $("eqAuto") : $("eqAutoAll");
  btn.disabled = true; btn.textContent = "Analisi…";
  try { // "Tutte": prima le tracce, poi il master che ascolta il mix già equalizzato
    for (const t of ids ? [ids] : [null, ["master"]]) {
      const { job } = await api("/api/eq/auto", { tracks: t });
      let j;
      do { await new Promise((r) => setTimeout(r, 400)); j = await api(`/api/jobs/${job}`); btn.textContent = `${Math.round(j.progress * 100)}%`; } while (!j.done);
      if (j.error) throw new Error(j.error);
    }
    await load();
    dispatchEvent(new Event("mix3d:eq"));
  } catch (e) { alert(e.message); }
  btn.disabled = false; btn.textContent = ids ? "Auto-tara" : "Tutte";
}

// --- grafico -----------------------------------------------------------------
function draw() {
  const cv = $("eqCv"); if (!cv) return;
  const d = devicePixelRatio, r = cv.getBoundingClientRect();
  cv.width = Math.max(r.width, 50) * d; cv.height = (+cv.getAttribute("height")) * d;
  const ctx = cv.getContext("2d"), W = cv.width, H = cv.height;
  ctx.clearRect(0, 0, W, H);
  ctx.strokeStyle = css("--line"); ctx.fillStyle = css("--muted"); ctx.font = `${10 * d}px sans-serif`; ctx.lineWidth = d;
  for (const f of [50, 100, 200, 500, 1000, 2000, 5000, 10000]) { const x = fx(f, W); ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); ctx.fillText(kHz(f), x + 3 * d, H - 4 * d); }
  for (const g of [-12, -6, 0, 6, 12]) { const y = gy(g, H); ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); ctx.fillText(`${g}`, 3 * d, y - 3 * d); }
  if (!curve) return;
  const path = (ys, map) => { ctx.beginPath(); curve.f.forEach((f, i) => { const x = fx(f, W), y = map(ys[i]); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); };
  if (curve.prima) { // spettro: 0 dB in cima, -60 dB in fondo
    const top = Math.max(...curve.prima), sy = (v) => H * Math.min(1, (top - v) / 60);
    path(curve.prima, sy); ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.fillStyle = css("--panel2"); ctx.fill();
    path(curve.dopo, sy); ctx.strokeStyle = css("--b"); ctx.globalAlpha = 0.6; ctx.stroke(); ctx.globalAlpha = 1;
  }
  ctx.setLineDash([4 * d, 4 * d]); path(curve.dinamica, (g) => gy(g, H)); ctx.strokeStyle = css("--accent2"); ctx.stroke(); ctx.setLineDash([]);
  if (curve.look) { ctx.setLineDash([2 * d, 3 * d]); path(curve.look, (g) => gy(g, H)); ctx.strokeStyle = css("--ok"); ctx.lineWidth = 1.5 * d; ctx.stroke(); ctx.setLineDash([]); ctx.lineWidth = d; }
  path(curve.statica, (g) => gy(g, H)); ctx.strokeStyle = css("--a"); ctx.lineWidth = 2 * d; ctx.stroke();
  bands.forEach((b, i) => {
    const x = fx(b.f, W), y = gy(cut(b) ? 0 : b.g || 0, H);
    ctx.beginPath(); ctx.arc(x, y, (i === focus ? 7 : 5) * d, 0, 7);
    ctx.fillStyle = b.on === false ? css("--muted") : b.auto ? css("--accent2") : css("--a"); ctx.fill();
    if (b.dyn) { ctx.beginPath(); ctx.arc(x, y, 9 * d, 0, 7); ctx.strokeStyle = css("--warn"); ctx.lineWidth = d; ctx.stroke(); }
    ctx.fillStyle = css("--text"); ctx.fillText(`${i + 1}`, x - 3 * d, y - 10 * d);
  });
}

const pt = (e) => { const r = e.target.getBoundingClientRect(), d = devicePixelRatio; return [(e.clientX - r.left) * d, (e.clientY - r.top) * d, e.target.width, e.target.height]; };
function hit(e) {
  const [x, y, W, H] = pt(e);
  return bands.findIndex((b) => Math.hypot(fx(b.f, W) - x, gy(cut(b) ? 0 : b.g || 0, H) - y) < 10 * devicePixelRatio);
}
function down(e) { const i = hit(e); if (i >= 0) { drag = i; focus = i; e.target.setPointerCapture(e.pointerId); draw(); list(); } }
function move(e) {
  const [x, y, W, H] = pt(e), b = bands[drag];
  b.f = Math.round(Math.min(F1, Math.max(F0, xf(x, W))));
  if (!cut(b)) b.g = Math.round(Math.max(-GMAX, Math.min(GMAX, yg(y, H))) * 2) / 2;
  b.auto = false; save(); draw();
}
function dbl(e) {
  const i = hit(e);
  if (i >= 0) { bands.splice(i, 1); focus = null; }
  else { const [x, y, W, H] = pt(e); bands.push({ id: Math.random().toString(16).slice(2, 8), tipo: "campana", f: Math.round(xf(x, W)), g: Math.round(yg(y, H)), q: 1, on: true, auto: false, dyn: null, perche: "" }); focus = bands.length - 1; }
  save();
}
function wheel(e) {
  const i = hit(e) >= 0 ? hit(e) : focus; if (i == null || i < 0 || cut(bands[i])) return;
  e.preventDefault();
  bands[i].q = Math.round(Math.max(0.2, Math.min(20, (bands[i].q || 1) * (e.deltaY < 0 ? 1.12 : 1 / 1.12))) * 100) / 100;
  bands[i].auto = false; save();
}

// --- elenco bande -------------------------------------------------------------
function list() {
  const el = $("eqList"); if (!el) return;
  const num = (i, k, v, step, w = 54) => `<input type="number" data-i="${i}" data-k="${k}" value="${v ?? ""}" step="${step}" style="width:${w}px">`;
  el.innerHTML = (curve?.sorgente ? `<p class="hint">Sorgente riconosciuta: <b>${curve.sorgente}</b></p>` : "") + bands.map((b, i) => `
    <div class="eq-row ${i === focus ? "focus" : ""}">
      <label class="check"><input type="checkbox" data-i="${i}" data-k="on" ${b.on !== false ? "checked" : ""}>${i + 1}</label>
      <select data-i="${i}" data-k="tipo">${Object.entries(TIPI).map(([k, n]) => `<option value="${k}" ${k === b.tipo ? "selected" : ""}>${n}</option>`).join("")}</select>
      ${num(i, "f", b.f, 1, 64)} Hz
      ${cut(b) ? `${num(i, "pendenza", b.pendenza || 12, 6)} dB/ott` : `${num(i, "g", b.g, 0.5)} dB Q ${num(i, "q", b.q, 0.1, 48)}`}
      ${cut(b) ? "" : `<label class="check"><input type="checkbox" data-i="${i}" data-k="dyn" ${b.dyn ? "checked" : ""}>dinamica</label>`}
      ${b.dyn ? `<span class="small">soglia ${num(i, "soglia_db", b.dyn.soglia_db, 1, 52)} dB · rapp. ${num(i, "rapporto", b.dyn.rapporto, 0.5, 44)}</span>` : ""}
      ${b.perche ? `<div class="hint">${b.auto ? "auto · " : ""}${b.perche}</div>` : ""}
    </div>`).join("");
  el.querySelectorAll("[data-k]").forEach((inp) => (inp.onchange = () => edit(+inp.dataset.i, inp.dataset.k, inp)));
}
function edit(i, k, inp) {
  const b = bands[i];
  if (k === "on") b.on = inp.checked;
  else if (k === "tipo") b.tipo = inp.value;
  else if (k === "dyn") b.dyn = inp.checked ? { soglia_db: -30, rapporto: 2, attacco_ms: 10, rilascio_ms: 120 } : null;
  else if (k === "soglia_db" || k === "rapporto") b.dyn[k] = +inp.value;
  else b[k] = +inp.value;
  b.auto = false; focus = i; save();
}

mount();
