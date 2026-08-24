// Build all MCP App UI bundles. Each HTML file is a separate Vite entry —
// `vite-plugin-singlefile` requires `inlineDynamicImports: true`, which
// rollup only supports with a single input per build, so we loop and
// invoke Vite's programmatic API once per UI.
import { rm } from "node:fs/promises";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { build } from "vite";

const ROOT = resolve(fileURLToPath(import.meta.url), "..");

const ENTRIES = [
  "src/DraftEmailView.html",
];

await rm(resolve(ROOT, "dist"), { recursive: true, force: true });

for (const entry of ENTRIES) {
  console.log(`\n→ Building ${entry}`);
  process.env.ENTRY = entry;
  await build({
    root: ROOT,
    configFile: resolve(ROOT, "vite.config.ts"),
    logLevel: "warn",
  });
}

console.log("\n✓ Built", ENTRIES.length, "MCP App UI bundles into dist/");