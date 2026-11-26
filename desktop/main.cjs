"use strict";

// This is intentionally only application chrome.  Rendering remains in the
// bundled local Python runtime, where PDF Designer already uses Playwright.
const { app, BrowserWindow, screen, shell } = require("electron");
const { spawn, execFile } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const STARTUP_TIMEOUT_MS = 30_000;
const SUPPORT_LINKS = new Set([
  "https://www.patreon.com/c/JenniNexus",
  "https://paypal.me/jenninexus",
  "https://discord.gg/KYPh7Cp",
  "https://x.com/JenniNexus"
]);
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
  // Reuse the last successful loopback origin so Chromium keeps Hub settings
  // across relaunches and updates. The runtime falls back if the port is busy.
  const previousUrl = readReadyUrl(readyFile);
  const preferredPort = previousUrl ? new URL(previousUrl).port : null;
  fs.rmSync(readyFile, { force: true });
  const args = ["--port", "0", "--no-open", "--ready-file", readyFile];
  if (preferredPort) args.push("--preferred-port", preferredPort);
  args.push(workspace);

  runtimeChild = spawn(
    runtime,
    args,
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

function windowBounds(preferredWidth, preferredHeight) {
  const { x, y, width, height } = screen.getDisplayNearestPoint(screen.getCursorScreenPoint()).workArea;
  const windowWidth = Math.min(preferredWidth, width);
  const windowHeight = Math.min(preferredHeight, height);
  return {
    x: x + Math.floor((width - windowWidth) / 2),
    y: y + Math.floor((height - windowHeight) / 2),
    width: windowWidth,
    height: windowHeight,
  };
}

function createMainWindow() {
  const bounds = windowBounds(1360, 900);
  const window = new BrowserWindow({
    ...bounds,
    minWidth: Math.min(640, bounds.width),
    minHeight: Math.min(400, bounds.height),
    show: false,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });
  window.removeMenu();
  window.webContents.setWindowOpenHandler(({ url }) => {
    if (SUPPORT_LINKS.has(url)) {
      shell.openExternal(url).catch(error => console.error("Support link failed:", error));
    }
    if (isAllowedRuntimeUrl(url) && new URL(url).pathname.toLowerCase().endsWith(".pdf")) {
      return { action: "allow" };
    }
    return { action: "deny" };
  });
  window.webContents.on("did-create-window", child => {
    child.webContents.setWindowOpenHandler(() => ({ action: "deny" }));
    child.webContents.on("will-navigate", event => event.preventDefault());
  });
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
    ...windowBounds(720, 460),
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
