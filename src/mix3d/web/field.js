// Campo sonoro nella scena: onde in tempo reale e mappa di presenza (diretto/riverbero).
// Non è una simulazione fisica: le onde seguono il livello RMS delle sorgenti (ogni 100 ms),
// si smorzano con l'RT60 dello spazio; la mappa usa la distanza critica (D/R = (dc/r)^2).
import * as THREE from "three";

const SPEED = 7;          // m/s visivi (il suono vero va a 343 m/s: troppo veloce da vedere)
const SPAWN_S = 0.22;     // un fronte d'onda ogni 220 ms per sorgente attiva
const FLOOR_DB = -55;     // sotto questa soglia la sorgente è in silenzio
const TARGET_DR = 1;      // dB: poco più diretto che riverbero, presenza piena ma non "dentro" al palco
const forward = (cos) => 0.7 + 0.3 * cos; // irraggiamento un po' verso il pubblico (+z)

// colore della mappa per rapporto diretto/riverbero in dB
const STOPS = [[-12, [70, 110, 255]], [-4, [50, 190, 230]], [0, [70, 235, 140]], [5, [170, 240, 90]], [9, [255, 180, 60]], [14, [255, 80, 90]]];
function drColor(dr) {
  const i = STOPS.findIndex(([v]) => v >= dr);
  if (i <= 0) return STOPS[i < 0 ? STOPS.length - 1 : 0][1];
  const [a, ca] = STOPS[i - 1], [b, cb] = STOPS[i], k = (dr - a) / (b - a);
  return ca.map((c, j) => c + (cb[j] - c) * k);
}
export const drLabel = (dr) => dr > 9 ? "troppo dentro" : dr > 5 ? "molto diretto" : dr > 0 ? "presenza piena" : dr > -4 ? "equilibrio con la sala" : "domina il riverbero";

// geometria unitaria di un fronte d'onda: anello piatto con raggio forward(cos θ)
function frontGeometry() {
  const n = 96, pos = [], idx = [];
  for (let i = 0; i <= n; i++) {
    const a = (i / n) * 2 * Math.PI, r = forward(Math.cos(a));
    for (const k of [0.94, 1]) pos.push(Math.sin(a) * r * k, 0, Math.cos(a) * r * k);
    if (i < n) { const j = 2 * i; idx.push(j, j + 1, j + 2, j + 1, j + 3, j + 2); }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx);
  return g;
}

export function createField(sc) {
  const group = new THREE.Group(), waves = [], pulses = new Map(), FRONT = frontGeometry();
  sc.add(group);
  let ctx = null, levels = [], spawnT = 0, mapKey = "";
  const cv = document.createElement("canvas");
  const map = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(cv), transparent: true, opacity: 0.6, depthWrite: false }));
  map.rotation.x = -Math.PI / 2; map.position.y = 0.02; sc.add(map);

  // rapporto diretto/riverbero (dB) nel punto p ad altezza orecchie, somma pesata sulle sorgenti
  function drAt(x, z, srcs = ctx.sources, w = weights()) {
    let s = 0;
    srcs.forEach((src, i) => {
      const dx = x - src.pos[0], dz = z - src.pos[2], dy = 1.2 - src.pos[1];
      const r2 = Math.max(dx * dx + dy * dy + dz * dz, 0.25), cos = dz / Math.sqrt(r2);
      s += w[i] * forward(cos) * (ctx.dc * ctx.dc) / r2;
    });
    return 10 * Math.log10(s + 1e-9);
  }
  // pesi in potenza delle sorgenti: dai livelli in ascolto, altrimenti uguali
  function weights() {
    const p = ctx.sources.map((_, i) => (levels[i] > FLOOR_DB ? 10 ** (levels[i] / 10) : 0));
    const tot = p.reduce((a, b) => a + b, 0);
    return tot > 0 ? p.map((v) => v / tot) : ctx.sources.map(() => 1 / ctx.sources.length);
  }

  function drawMap() {
    const { w, d, z0 } = ctx.room, W = 120, H = Math.round((W * (d - z0)) / w);
    if (cv.width !== W || cv.height !== H) { // la texture WebGL non cambia misura: se ne crea una nuova
      cv.width = W; cv.height = H;
      map.material.map.dispose(); map.material.map = new THREE.CanvasTexture(cv);
    }
    const g = cv.getContext("2d"), img = g.createImageData(W, H), wt = weights();
    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
      const x = -w / 2 + ((i + 0.5) / W) * w, z = z0 + ((j + 0.5) / H) * (d - z0);
      const dr = drAt(x, z, ctx.sources, wt), [r, gg, b] = drColor(dr), o = 4 * (j * W + i);
      const band = Math.abs(dr - TARGET_DR) < 0.35 ? 90 : 0; // isolinea del punto d'ascolto ideale
      img.data.set([r + band, gg + band, b + band, z < 0 ? 50 : 150 + band], o);
    }
    g.putImageData(img, 0, 0); map.material.map.needsUpdate = true;
    map.scale.set(w, d - z0, 1); map.position.set(0, 0.02, (d + z0) / 2);
  }

  function spawn(src, i) {
    const amp = Math.min(1, (levels[i] - FLOOR_DB) / 40);
    if (amp <= 0) return;
    const m = new THREE.Mesh(FRONT, new THREE.MeshBasicMaterial({ color: src.color, transparent: true, opacity: amp, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
    m.position.set(src.pos[0], 0.06 + Math.min(src.pos[1], 1.5) * 0.5, src.pos[2]);
    m.userData = { r: 0.2, amp };
    group.add(m); waves.push(m);
  }
  function pulse(src, i) {
    let p = pulses.get(i);
    if (!p) { p = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 14), new THREE.MeshBasicMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })); group.add(p); pulses.set(i, p); }
    const amp = Math.max(0, Math.min(1, (levels[i] - FLOOR_DB) / 40));
    p.material.color.set(src.color); p.material.opacity = 0.08 + 0.3 * amp;
    p.position.set(...src.pos); p.scale.setScalar(p.scale.x + (0.35 + 1.4 * amp - p.scale.x) * 0.3);
  }

  return {
    // contesto: sorgenti [{pos, color}], sala, distanza critica, durata del riverbero
    set(c) {
      ctx = c;
      const key = JSON.stringify([c.sources.map((s) => s.pos), c.room, c.dc]);
      if (key !== mapKey && c.showMap) { mapKey = key; drawMap(); }
      map.visible = c.showMap; group.visible = c.showWaves;
      for (const [i, p] of pulses) if (i >= c.sources.length) { group.remove(p); pulses.delete(i); }
    },
    levels(db) { levels = db; if (ctx?.showMap) { mapKey = ""; drawMap(); } },
    silence() { levels = []; mapKey = ""; if (ctx?.showMap) drawMap(); },
    update(dt) {
      if (!ctx?.showWaves) return;
      spawnT += dt;
      if (spawnT > SPAWN_S) { spawnT = 0; ctx.sources.forEach(spawn); }
      ctx.sources.forEach(pulse);
      const rmax = ctx.reach;
      for (let k = waves.length - 1; k >= 0; k--) {
        const m = waves[k], u = m.userData;
        u.r += SPEED * dt;
        const life = 1 - u.r / rmax;
        if (life <= 0) { group.remove(m); m.material.dispose(); waves.splice(k, 1); continue; }
        m.scale.setScalar(u.r); m.material.opacity = u.amp * life * life * Math.min(1, 1.5 / u.r + 0.25);
      }
    },
    dr: (x, z) => (ctx ? drAt(x, z) : null),
    // punto d'ascolto suggerito: D/R vicino a TARGET_DR, in platea, il più centrale possibile
    suggest() {
      const { w, d } = ctx.room;
      let best = null;
      for (let z = 1; z <= d - 1; z += 0.25) for (let x = -w / 2 + 1; x <= w / 2 - 1; x += 0.25) {
        const cost = Math.abs(drAt(x, z) - TARGET_DR) + 0.15 * Math.abs(x);
        if (!best || cost < best.cost) best = { x, z, cost };
      }
      return best && [+best.x.toFixed(2), 1.2, +best.z.toFixed(2)];
    },
  };
}
