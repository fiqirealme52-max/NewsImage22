// News 22 (revision round 3) — one-day evidence board entrypoint.
// Copies the pre-drawn entry image to the output directory.
// Standard library only; no network.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
// Fail loudly if the copy did not land, so a bad run is never silent.
import { statSync } from "node:fs";
const bytes = statSync(dst).size;
if (bytes === 0) throw new Error("entry.png copy is empty");
console.log(`wrote ${dst} (${bytes} bytes) — News 22 revision round 3, 35 stories`);
