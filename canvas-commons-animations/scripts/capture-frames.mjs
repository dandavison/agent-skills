#!/usr/bin/env node
// Headless frame capture for a running Canvas Commons / Motion Canvas editor.
//
// Drives the editor dev server with a headless browser, triggers the
// image-sequence renderer for chosen points in the timeline, then collects the
// produced PNGs so an agent can Read them and visually inspect the animation.
// This is the verification step: it catches runtime errors, off-screen nodes,
// text/box collisions, and timing mistakes that a type-check and build cannot.
//
// Prereqs:
//   1. The editor dev server is running (e.g. `pnpm template:dev`, default
//      http://localhost:9000). The frames are written by that server into the
//      *project package's* output/ dir, so run this from (or pass --project-dir
//      pointing at) the package whose dev server is running.
//   2. A browser binary is available to Playwright. If not, install one:
//        pnpm --filter <e2e-pkg> exec playwright install chromium-headless-shell
//
// Usage:
//   node capture-frames.mjs --project-dir packages/template
//   node capture-frames.mjs --fractions 0,0.3,0.6,0.9,1
//   node capture-frames.mjs --all --scale 1 --encode out.mp4   # full render + mp4
//
// Flags:
//   --url <url>            editor dev server (default http://localhost:9000)
//   --project-dir <dir>    package running the dev server (default cwd) — its
//                          output/ dir is where rendered PNGs land
//   --out <dir>            collect captured frames here (default ./.cc-frames)
//   --fractions a,b,c      timeline positions in [0,1] to sample
//                          (default 0,0.25,0.5,0.75,1)
//   --all                  render every frame instead of sampling
//   --scale <n>            resolutionScale: 0.5 fast preview, 1 full (default 0.5)
//   --encode <path.mp4>    after --all, encode the sequence to mp4 via ffmpeg
//   --timeout <ms>         per-render timeout (default 120000)

import {spawnSync} from 'node:child_process';
import {existsSync, mkdirSync, readdirSync, rmSync, copyFileSync, statSync} from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const args = parseArgs(process.argv.slice(2));
const url = args.url ?? 'http://localhost:9000';
const projectDir = path.resolve(args['project-dir'] ?? process.cwd());
const outDir = path.resolve(args.out ?? '.cc-frames');
const scale = Number(args.scale ?? 0.5);
const timeout = Number(args.timeout ?? 120000);
const renderAll = 'all' in args;
const fractions = (args.fractions ?? '0,0.25,0.5,0.75,1')
  .split(',')
  .map(Number)
  .filter(n => !Number.isNaN(n));

const outputRoot = path.join(projectDir, 'output');

const chromium = await loadChromium(projectDir);
const browser = await chromium.launch();
const page = await browser.newPage();
const problems = [];
page.on('console', m => {
  if (m.type() === 'error') problems.push(`console.error: ${m.text()}`);
});
page.on('pageerror', e => problems.push(`pageerror: ${e.message}`));

try {
  await page.goto(url);
  await page.waitForSelector('main');
  await page.waitForFunction(
    () => !!window.commons && window.commons.player.playback.duration > 0,
    undefined,
    {timeout: 30000},
  );

  const info = await page.evaluate(() => ({
    frames: window.commons.player.playback.duration,
    fps: window.commons.player.playback.fps,
    name: window.commons.project.name,
  }));
  const seconds = info.frames / info.fps;
  console.log(
    `project=${info.name} duration=${seconds.toFixed(2)}s fps=${info.fps}`,
  );

  // Start clean so collected frames are exactly this run's output.
  rmSync(outputRoot, {recursive: true, force: true});
  rmSync(outDir, {recursive: true, force: true});
  mkdirSync(outDir, {recursive: true});
  const collected = [];

  if (renderAll) {
    await renderRange(0, seconds);
    console.log('full render complete');
    // Keep sequential names so ffmpeg can consume them directly.
    for (const src of collectPngs(outputRoot)) {
      const dest = path.join(outDir, path.basename(src));
      copyFileSync(src, dest);
      collected.push(dest);
    }
  } else {
    // The renderer emits the requested frame plus a boundary frame for a narrow
    // range, so collect per-sample and keep just the first new PNG.
    const seen = new Set();
    for (const f of fractions) {
      const frame = Math.min(
        Math.max(0, Math.round(Math.min(f, 1) * (info.frames - 1))),
        info.frames - 1,
      );
      await renderRange(frame / info.fps, (frame + 0.999) / info.fps);
      const fresh = collectPngs(outputRoot).filter(p => !seen.has(p));
      fresh.forEach(p => seen.add(p));
      if (fresh.length === 0) {
        console.log(`fraction ${f}: no frame produced (skipped)`);
        continue;
      }
      const dest = path.join(
        outDir,
        `frame-${String(collected.length + 1).padStart(3, '0')}.png`,
      );
      copyFileSync(fresh[0], dest);
      collected.push(dest);
      console.log(`rendered frame ${frame} (t=${(frame / info.fps).toFixed(2)}s, fraction ${f})`);
    }
  }

  if (collected.length === 0) {
    throw new Error(
      `No frames found under ${outputRoot}. Is --project-dir the package ` +
        `running the dev server?`,
    );
  }

  console.log(`\ncaptured ${collected.length} frame(s) to ${outDir}:`);
  for (const f of collected) console.log('  ' + f);

  console.log(
    problems.length ? `\nRUNTIME PROBLEMS:\n  ${problems.join('\n  ')}` : '\nno runtime errors',
  );

  if (renderAll && args.encode) {
    encode(collected, info.fps, path.resolve(args.encode));
  }
} finally {
  await browser.close();
}

async function renderRange(start, end) {
  await page.evaluate(
    async ({start, end, scale}) => {
      const settings = window.commons.meta.getFullRenderingSettings();
      await window.commons.renderer.render({
        ...settings,
        name: window.commons.project.name,
        resolutionScale: scale,
        range: [start, end],
        exporter: {
          name: '@canvas-commons/core/image-sequence',
          options: {fileType: 'image/png', quality: 100, groupByScene: true},
        },
      });
    },
    {start, end, scale},
  );
  await page.waitForTimeout(150); // let the server flush PNGs to disk
}

function collectPngs(root) {
  if (!existsSync(root)) return [];
  const found = [];
  const walk = dir => {
    for (const entry of readdirSync(dir, {withFileTypes: true})) {
      const p = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(p);
      else if (entry.name.endsWith('.png')) found.push(p);
    }
  };
  walk(root);
  return found.sort();
}

function encode(frames, fps, outPath) {
  const dir = path.dirname(frames[0]);
  const r = spawnSync(
    'ffmpeg',
    ['-y', '-framerate', String(fps), '-pattern_type', 'glob', '-i',
     path.join(dir, '*.png'),
     '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
     '-movflags', '+faststart', outPath],
    {stdio: 'inherit'},
  );
  if (r.status === 0) console.log(`\nencoded ${outPath} (${statSizeMB(outPath)} MB)`);
  else console.log('\nffmpeg failed; is ffmpeg installed?');
}

function statSizeMB(p) {
  return (statSync(p).size / 1e6).toFixed(1);
}

async function loadChromium(startDir) {
  try {
    return (await import('playwright')).chromium;
  } catch {
    /* fall through to discovery */
  }
  // Walk up from startDir. At each ancestor check node_modules/playwright and,
  // because pnpm does not hoist, every packages/<pkg>/node_modules/playwright
  // (canvas-commons keeps it in the e2e package).
  let dir = startDir;
  for (let i = 0; i < 8; i++) {
    const candidates = [path.join(dir, 'node_modules/playwright')];
    const pkgsDir = path.join(dir, 'packages');
    if (existsSync(pkgsDir)) {
      for (const entry of readdirSync(pkgsDir, {withFileTypes: true})) {
        if (entry.isDirectory()) {
          candidates.push(path.join(pkgsDir, entry.name, 'node_modules/playwright'));
        }
      }
    }
    for (const c of candidates) {
      const entry = path.join(c, 'index.mjs');
      if (existsSync(entry)) return (await import(pathToFileURL(entry).href)).chromium;
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  throw new Error(
    'Playwright not found. Install it, e.g.:\n' +
      '  pnpm --filter @canvas-commons/e2e exec playwright install chromium-headless-shell\n' +
      'or `npm i -D playwright && npx playwright install chromium-headless-shell`,\n' +
      'then re-run. You can also pass its dir via the node_modules resolution path.',
  );
}

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) continue;
    const key = a.slice(2);
    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) out[key] = true;
    else {
      out[key] = next;
      i++;
    }
  }
  return out;
}
