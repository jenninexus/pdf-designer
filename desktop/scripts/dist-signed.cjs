"use strict";

// Signed NSIS release. Fails closed unless Azure Trusted Signing names and
// Entra credentials are present. Never writes secrets. The unsigned 0.1.0
// artifact must not be treated as this path succeeding.
const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const root = path.resolve(__dirname, "..");
const repoRoot = path.resolve(root, "..");
const localConfig = path.join(root, "azure-trusted-signing.json");
const exampleConfig = path.join(root, "azure-trusted-signing.example.json");

function fail(message) {
  console.error(message);
  process.exit(1);
}

if (!fs.existsSync(localConfig)) {
  fail(
    "Missing desktop/azure-trusted-signing.json. Copy " +
      path.basename(exampleConfig) +
      " and fill the Azure account names. Entra secrets stay in AZURE_* env vars, never git."
  );
}

const azure = JSON.parse(fs.readFileSync(localConfig, "utf8"));
for (const key of ["publisherName", "endpoint", "codeSigningAccountName", "certificateProfileName"]) {
  const value = azure[key];
  if (!value || String(value).includes("REPLACE_WITH")) {
    fail(`desktop/azure-trusted-signing.json field "${key}" is missing or still a placeholder.`);
  }
}

for (const name of ["AZURE_TENANT_ID", "AZURE_CLIENT_ID"]) {
  if (!process.env[name]) {
    fail(`Signed dist requires ${name} in the environment (sys-admin / user env). Never commit it.`);
  }
}
if (!process.env.AZURE_CLIENT_SECRET && !process.env.AZURE_CLIENT_CERTIFICATE_PATH) {
  fail("Signed dist requires AZURE_CLIENT_SECRET or AZURE_CLIENT_CERTIFICATE_PATH.");
}

const pkg = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
const config = {
  ...pkg.build,
  win: {
    ...pkg.build.win,
    azureSignOptions: {
      publisherName: azure.publisherName,
      endpoint: azure.endpoint,
      codeSigningAccountName: azure.codeSigningAccountName,
      certificateProfileName: azure.certificateProfileName,
      fileDigest: azure.fileDigest || "SHA256",
      timestampRfc3161: azure.timestampRfc3161 || "http://timestamp.acs.microsoft.com",
      timestampDigest: azure.timestampDigest || "SHA256"
    }
  }
};

const tmpDir = path.join(root, ".runtime-build");
fs.mkdirSync(tmpDir, { recursive: true });
const tmp = path.join(tmpDir, "electron-builder.signed.json");
fs.writeFileSync(tmp, JSON.stringify(config, null, 2));

const env = { ...process.env };
delete env.CSC_IDENTITY_AUTO_DISCOVERY;

const bin = path.join(
  root,
  "node_modules",
  ".bin",
  process.platform === "win32" ? "electron-builder.cmd" : "electron-builder"
);
const built = spawnSync(bin, ["--config", tmp, "--win", "nsis", "--x64", "--publish", "never"], {
  cwd: root,
  stdio: "inherit",
  env,
  shell: process.platform === "win32"
});
if ((built.status ?? 1) !== 0) process.exit(built.status ?? 1);

const installer = path.join(root, "dist", `PDF-Designer-Setup-${pkg.version}.exe`);
const verify = path.join(repoRoot, "scripts", "verify-authenticode.ps1");
const checked = spawnSync(
  "pwsh",
  ["-NoProfile", "-File", verify, "-InstallerPath", installer, "-RequireSigned", "-ExpectedPublisher", azure.publisherName],
  { cwd: repoRoot, stdio: "inherit" }
);
process.exit(checked.status ?? 1);
