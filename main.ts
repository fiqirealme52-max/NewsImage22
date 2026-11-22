// News 22 (round 4) — one-day evidence board entrypoint.
// Copies the pre-drawn entry image to the output directory.
// Standard library only; no network.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
// Validate the source image before copying: it must exist and carry a
// genuine PNG signature (89 50 4E 47 0D 0A 1A 0A), so a truncated or
// non-PNG file can never be shipped as the entry.
let png: Buffer;
try {
  png = readFileSync(src);
} catch {
  throw new Error(`entry.png not found at ${src} — cannot build the entry`);
}
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (png.length < 8 || !png.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("entry.png is not a valid PNG (bad or missing PNG signature)");
}
// Verify the IHDR chunk: the entry must be exactly 1024×1024, the size
// this competition's image is drawn at. Width/height are the big-endian
// uint32s at bytes 16–23, right after the 8-byte signature + 8-byte chunk
// header. A wrong-size image would be a silent grading failure.
if (png.length < 24 || png.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("entry.png has no IHDR chunk — not a readable PNG image");
}
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}×${height}, expected 1024×1024`);
}
// Verify the IEND chunk: a complete PNG ends with a 12-byte IEND chunk
// (0 length, "IEND", CRC). A truncated file would lack it.
if (png.length < 12 || png.toString("ascii", png.length - 8, png.length - 4) !== "IEND") {
  throw new Error("entry.png is truncated (missing IEND chunk)");
}
copyFileSync(src, dst);
// Fail loudly if the copy did not land, so a bad run is never silent.
const bytes = statSync(dst).size;
if (bytes === 0) throw new Error("entry.png copy is empty");
console.log(`wrote ${dst} (${width}×${height}, ${bytes} bytes) — News 22 round 4, 35 stories`);
