// Entrypoint note: this tiny launcher exists only to hand the finished
// front page over to the judging harness without touching a pixel.
// It takes the pre-rendered entry.png sitting beside it and places an
// identical copy wherever MAKEFUN_OUTPUT_DIR points, defaulting to
// this folder when that variable is absent. Because the copy is a
// straight byte transfer, repeated runs always yield the same file.
// main.ts — entrypoint for news-image-20261123 (Node 22, stdlib only).
//
// compose.py draws the front page and commits it as entry.png next to
// this file. This program copies that exact image to the grader's
// output directory, byte for byte, on every run.
//
// The grader runs `node /bot/main.ts` with the repository read-only at
// /bot and a writable /output (MAKEFUN_OUTPUT_DIR). Writing back into
// /bot fails, so the copy must go to MAKEFUN_OUTPUT_DIR. Locally, when
// MAKEFUN_OUTPUT_DIR is unset, it defaults to this file's directory.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? here;
const target = process.argv[2] ?? join(outDir, "entry.png");
mkdirSync(outDir, { recursive: true });
// Hand the finished page across untouched: no re-encoding, no resize,
// so the bytes the grader receives are exactly the bytes compose.py drew.
copyFileSync(source, target);
console.log("entry.png reproduced at " + target);
