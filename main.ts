// news-image-20261122 — make.fun entrypoint (Node 22, stdlib only).
//
// The entry is a single finished image that already sits next to this file.
// This program's only job is to place an exact copy of it, as entry.png,
// into the grader's output directory, so every run produces the same bytes.
//
// Local equivalent of the grader's /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(here, 'entry.png');
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

if (!existsSync(sourceImage)) {
  throw new Error(`entry image not found: ${sourceImage}`);
}

mkdirSync(outputDir, { recursive: true });
const destination = join(outputDir, 'entry.png');
copyFileSync(sourceImage, destination);
console.log(`entry.png -> ${destination}`);
