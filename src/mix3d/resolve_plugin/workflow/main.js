// Pannello MIX3D dentro Resolve (Workspace > Workflow Integrations > MIX3D).
// Avvia l'app MIX3D senza browser se non è già aperta e ne mostra il pannello in una finestra di Resolve.
const { app, BrowserWindow } = require("electron");
const { execFile } = require("child_process");
const http = require("http");

const URL = "http://127.0.0.1:8730/";
const page = (msg) => "data:text/html;charset=utf-8," + encodeURIComponent(
  `<body style="background:#121417;color:#8b939e;font:14px -apple-system,sans-serif;padding:40px">${msg}</body>`);

const isUp = (cb) => http.get(URL, (r) => { r.resume(); cb(true); }).on("error", () => cb(false));

function load(win, tries = 60) {
  isUp((ok) => {
    if (ok) return win.loadURL(URL + "#resolve");
    if (tries) return setTimeout(() => load(win, tries - 1), 500);
    win.loadURL(page("MIX3D non risponde. È installata in Applicazioni? Aprila una volta a mano (tasto destro &gt; Apri)."));
  });
}

function createWindow() {
  const win = new BrowserWindow({ width: 1440, height: 900, title: "MIX3D", backgroundColor: "#121417" });
  win.loadURL(page("Avvio MIX3D…"));
  isUp((ok) => {
    if (!ok) execFile("open", ["-g", "-a", "MIX3D", "--args", "--no-browser"]);
    load(win);
  });
}

app.whenReady().then(createWindow);
app.on("window-all-closed", () => app.quit());
