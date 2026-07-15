#!/usr/bin/env node
/**
 * wcag-resume-palettes — contrast spot-check for pdf-designer resume presets.
 * Adapted from syna-theme-kit/scripts/wcag-check.mjs (same WCAG math).
 *
 * Usage (from pdf-designer root):
 *   node scripts/wcag-resume-palettes.mjs
 *   node scripts/wcag-resume-palettes.mjs --strict
 */
import { readFileSync, readdirSync, existsSync } from "fs";
import { resolve, dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const STRICT = process.argv.includes("--strict");

function hexToRgb(hex) {
  const h = hex.replace("#", "");
  const full = h.length === 3 ? h.split("").map((c) => c + c).join("") : h;
  return [parseInt(full.slice(0, 2), 16), parseInt(full.slice(2, 4), 16), parseInt(full.slice(4, 6), 16)];
}
function relLum([r, g, b]) {
  const f = (v) => {
    const s = v / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}
function contrast(a, b) {
  const L1 = relLum(hexToRgb(a));
  const L2 = relLum(hexToRgb(b));
  const hi = Math.max(L1, L2);
  const lo = Math.min(L1, L2);
  return (hi + 0.05) / (lo + 0.05);
}

function loadTokenMaps() {
  const maps = [];
  const files = [
    join(ROOT, "themes", "default-resume.json"),
    ...readdirSync(join(ROOT, "themes", "presets"))
      .filter((n) => n.endsWith(".json"))
      .map((n) => join(ROOT, "themes", "presets", n)),
  ];
  for (const f of files) {
    if (!existsSync(f)) continue;
    const data = JSON.parse(readFileSync(f, "utf8"));
    const name = data._meta?.name || f.split(/[/\\]/).pop();
    if (data.tokens?.dark && data.tokens?.light) {
      maps.push({ name, dark: data.tokens.dark, light: data.tokens.light });
    } else if (data.dark?.accents && data.light?.accents) {
      maps.push({
        name,
        dark: {
          "--bg": data.dark.backgrounds?.body,
          "--text": (data.dark.text?.primary || "").startsWith("#")
            ? data.dark.text.primary
            : "#f0f2f6",
          "--primary": data.dark.accents.primary,
        },
        light: {
          "--bg": data.light.backgrounds?.body,
          "--text": data.light.text?.primary,
          "--primary": data.light.accents.primary,
        },
      });
    }
  }
  return maps;
}

function solidHex(v) {
  if (!v || typeof v !== "string") return null;
  if (v.startsWith("#") && (v.length === 7 || v.length === 4)) return v;
  return null; // skip rgba for this spot-check
}

let fails = 0;
for (const m of loadTokenMaps()) {
  for (const mode of ["dark", "light"]) {
    const t = m[mode];
    const bg = solidHex(t["--bg"]);
    const text = solidHex(t["--text"]);
    const primary = solidHex(t["--primary"]);
    if (bg && text) {
      const r = contrast(text, bg);
      const ok = r >= 4.5;
      if (!ok) fails++;
      console.log(`${ok ? "PASS" : "FAIL"} ${m.name} ${mode} text/bg ${r.toFixed(2)}:1`);
    }
    if (bg && primary) {
      const r = contrast(primary, bg);
      const ok = r >= 3.0; // large-text / UI accent floor
      if (!ok) fails++;
      console.log(`${ok ? "PASS" : "FAIL"} ${m.name} ${mode} primary/bg ${r.toFixed(2)}:1 (UI≥3)`);
    }
  }
}
console.log(fails ? `\n${fails} contrast warnings` : "\nAll checked pairs OK");
if (STRICT && fails) process.exit(1);
