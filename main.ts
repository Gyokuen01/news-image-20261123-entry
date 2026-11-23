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
copyFileSync(source, target);
console.log("entry.png reproduced at " + target);
