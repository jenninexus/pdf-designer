"use strict";

// Default NSIS dist stays unsigned on purpose. A cert sitting in the Windows
// store must not silently Authenticode-sign a packaging artifact.
const { spawnSync } = require("node:child_process");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
process.env.CSC_IDENTITY_AUTO_DISCOVERY = process.env.CSC_IDENTITY_AUTO_DISCOVERY || "false";

const bin = path.join(
  root,
  "node_modules",
  ".bin",
  process.platform === "win32" ? "electron-builder.cmd" : "electron-builder"
);

const result = spawnSync(bin, ["--win", "nsis", "--x64", "--publish", "never"], {
  cwd: root,
  stdio: "inherit",
  env: process.env,
  shell: process.platform === "win32"
});

process.exit(result.status ?? 1);
