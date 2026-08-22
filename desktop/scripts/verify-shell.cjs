"use strict";

const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const packageJson = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
const main = fs.readFileSync(path.join(root, "main.cjs"), "utf8");
const readme = fs.readFileSync(path.join(root, "README.md"), "utf8");
const failures = [];

function assert(condition, message) {
  if (!condition) failures.push(message);
}
function includes(source, value, message) {
  assert(source.includes(value), message);
}

assert(packageJson.main === "main.cjs", "package main must be main.cjs");
assert(packageJson.build?.appId === "com.jenninexus.pdfdesigner", "appId must be com.jenninexus.pdfdesigner");
assert(packageJson.devDependencies?.electron === "43.4.1", "Electron must be pinned to 43.4.1");
assert(packageJson.devDependencies?.["electron-builder"] === "26.15.3", "electron-builder must be pinned to 26.15.3");
assert(packageJson.build?.artifactName === "PDF-Designer-Setup-${version}.exe", "NSIS artifact name is incorrect");
assert(packageJson.build?.win?.target?.[0]?.target === "nsis", "Windows target must be NSIS");
assert(packageJson.build?.win?.target?.[0]?.arch?.join(",") === "x64", "NSIS target must be x64 only");
assert(packageJson.build?.nsis?.oneClick === false, "installer must be assisted (oneClick false)");
assert(packageJson.build?.nsis?.perMachine === false, "installer must be per-user");
assert(packageJson.build?.nsis?.allowToChangeInstallationDirectory === true, "installer must permit changing install directory");
assert(packageJson.build?.nsis?.createDesktopShortcut === true, "installer must create a desktop shortcut");
assert(packageJson.build?.nsis?.createStartMenuShortcut === true, "installer must create a Start Menu shortcut");
includes(packageJson.scripts?.dist || "", "--publish never", "dist must explicitly disable publishing");
includes(main, "app.requestSingleInstanceLock()", "single-instance lock is required");
includes(main, '"--port", "0", "--no-open", "--ready-file"', "runtime launch arguments are incomplete");
includes(main, 'packagedResource("runtime", "pdf-designer-runtime", "pdf-designer-runtime.exe")', "shell must launch only the bundled runtime executable");
assert(packageJson.build?.extraResources?.some((entry) => entry.from === "workspace-seed" && entry.to === "workspace-seed"), "workspace seed must be packaged as a resource");
includes(main, "/^http:\\/\\/127\\.0\\.0\\.1:([1-9][0-9]{0,4})\\/$/", "ready URL must require exact loopback URL form");
includes(main, "STARTUP_TIMEOUT_MS = 30_000", "runtime startup must be bounded");
includes(main, "contextIsolation: true", "context isolation must be enabled");
includes(main, "nodeIntegration: false", "Node integration must be disabled");
includes(main, "sandbox: true", "renderer sandbox must be enabled");
includes(main, "setWindowOpenHandler(() => ({ action: \"deny\" }))", "window.open must be denied");
includes(main, "will-navigate", "navigation must be restricted");
includes(main, 'candidate.hostname === "127.0.0.1"', "navigation must stay on loopback");
includes(main, "execFile(\"taskkill\"", "only the spawned runtime PID must be stopped on quit");
assert(!main.includes("autoUpdater"), "desktop shell must not include an auto-updater");
assert(!main.includes("https://"), "desktop shell must not load remote URLs");
includes(readme, "SmartScreen", "README must explain unsigned Windows SmartScreen behavior");
includes(readme, "no auto-update", "README must state the no-auto-update contract");

if (failures.length) {
  console.error("PDF Designer desktop-shell verification failed:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}
console.log("PDF Designer desktop-shell static verification passed.");
