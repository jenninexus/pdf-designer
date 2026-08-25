"use strict";

// This is intentionally only application chrome.  Rendering remains in the
// bundled local Python runtime, where PDF Designer already uses Playwright.
const { app, BrowserWindow } = require("electron");
const { spawn, execFile } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const STARTUP_TIMEOUT_MS = 30_000;
let runtimeChild = null;
let runtimeUrl = null;

function packagedResource(...parts) {
  return app.isPackaged
    ? path.join(process.resourcesPath, ...parts)
    : path.join(__dirname, ...parts);
}

function documentsLooksCloudRedirected(documentsPath) {
  const normalized = documentsPath.replace(/\//g, "\\").toLowerCase();
  return normalized.includes("\\onedrive")
    || normalized.includes("\\dropbox")
    || normalized.includes("\\icloud")
    || normalized.includes("\\google drive");
}

function seedWorkspace() {
  const documents = app.getPath("documents");
  const workspace = path.join(documents, "PDF Designer");
  const seed = packagedResource("workspace-seed");

  // Follow Windows Documents, including Known Folder Move. PDF Designer does
  // not create a cloud account; a redirected Documents folder is the user's
  // OS policy. See docs/WINDOWS-ELECTRON.md.
  if (documentsLooksCloudRedirected(documents)) {
    console.warn(
      "Documents is redirected to a sync provider. The workspace stays at",
      workspace,
      "and may be synced by that provider."
    );
  }

  // A user's existing workspace is authoritative: this shell never merges or
  // replaces it.  The seed is copied only on a genuinely first run.
  if (!fs.existsSync(workspace)) {
    fs.cpSync(seed, workspace, { recursive: true, force: false, errorOnExist: false });
  }
  return workspace;
}

function readReadyUrl(readyFile) {
  if (!fs.existsSync(readyFile)) return null;
  const value = fs.readFileSync(readyFile, "utf8").trim();
  const match = /^http:\/\/127\.0\.0\.1:([1-9][0-9]{0,4})\/$/.exec(value);
  if (!match || Number(match[1]) > 65535) return null;
  return value;
}

function waitForRuntimeUrl(readyFile, child) {
  return new Promise((resolve, reject) => {
    const deadline = Date.now() + STARTUP_TIMEOUT_MS;
    const timer = setInterval(() => {
      const readyUrl = readReadyUrl(readyFile);
      if (readyUrl) {
        clearInterval(timer);
        resolve(readyUrl);
        return;
      }
      if (child.exitCode !== null || Date.now() >= deadline) {
        clearInterval(timer);
        reject(new Error("The local runtime did not become ready in time."));
      }
    }, 100);
  });
}

async function startRuntime(workspace) {
  const runtime = packagedResource("runtime", "pdf-designer-runtime", "pdf-designer-runtime.exe");
  const readyFile = path.join(app.getPath("userData"), "runtime-ready.txt");
  fs.mkdirSync(path.dirname(readyFile), { recursive: true });
  fs.rmSync(readyFile, { force: true });

  runtimeChild = spawn(
    runtime,
    ["--port", "0", "--no-open", "--ready-file", readyFile, workspace],
    { stdio: ["ignore", "ignore", "pipe"], windowsHide: true, shell: false }
  );
  runtimeChild.stderr.on("data", (data) => console.error(`[pdf-designer runtime] ${data}`));
  runtimeChild.on("error", (error) => console.error("Unable to start local runtime:", error));

  return waitForRuntimeUrl(readyFile, runtimeChild);
}

function isAllowedRuntimeUrl(url) {
  try {
    const expected = new URL(runtimeUrl);
    const candidate = new URL(url);
    // Permit Design Hub's own local routes, but never another origin, port, or
    // protocol. The ready file itself remains restricted to the exact root URL.
    return candidate.protocol === "http:"
      && candidate.hostname === "127.0.0.1"
      && candidate.port === expected.port;
  } catch {
    return false;
  }
}

function createMainWindow() {
  const window = new BrowserWindow({
    width: 1360,
    height: 900,
    minWidth: 960,
    minHeight: 680,
    show: false,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });
  window.removeMenu();
  window.webContents.setWindowOpenHandler(() => ({ action: "deny" }));
  window.webContents.on("will-attach-webview", (event) => event.preventDefault());
  window.webContents.on("will-navigate", (event, target) => {
    if (!isAllowedRuntimeUrl(target)) event.preventDefault();
  });
  window.once("ready-to-show", () => window.show());
  const launch = new URL(runtimeUrl);
  launch.searchParams.set("splash", "1");
  window.loadURL(launch.href);
}

function showStartupError(error) {
  console.error("PDF Designer startup failed:", error);
  const window = new BrowserWindow({
    width: 720,
    height: 460,
    resizable: false,
    webPreferences: { contextIsolation: true, nodeIntegration: false, sandbox: true }
  });
  window.removeMenu();
  window.webContents.setWindowOpenHandler(() => ({ action: "deny" }));
  window.webContents.on("will-attach-webview", (event) => event.preventDefault());
  window.loadFile(path.join(__dirname, "startup-error.html"));
}

function stopRuntime() {
  const child = runtimeChild;
  runtimeChild = null;
  if (!child || !child.pid || child.exitCode !== null) return;
  // Deliberately target only the PID created above (and its child tree).
  execFile("taskkill", ["/pid", String(child.pid), "/t", "/f"], { windowsHide: true }, () => {});
}

if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on("second-instance", () => {
    const window = BrowserWindow.getAllWindows()[0];
    if (window) {
      if (window.isMinimized()) window.restore();
      window.focus();
    }
  });
  app.on("before-quit", stopRuntime);
  app.whenReady()
    .then(async () => {
      const workspace = seedWorkspace();
      runtimeUrl = await startRuntime(workspace);
      createMainWindow();
    })
    .catch(showStartupError);
}
