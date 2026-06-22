# Setup, build, and the frame-capture mechanism

Repo-specific operational detail for the canvas-commons monorepo. Upstream
Motion Canvas differs in package scope and script names but the capture
mechanism (driving the editor's `window.commons` debug surface) is identical.

## Where to put a scene

The fastest place to develop is the **template** package (a private dev
project):

- Scene file: `packages/template/src/scenes/<name>.tsx`
- Sibling meta: `packages/template/src/scenes/<name>.meta`
- Register it in `packages/template/src/project.ts`:

  ```ts
  import scene from './scenes/<name>?scene';
  export default makeProject({experimentalFeatures: true, scenes: [scene]});
  ```

For an animation that will live in the docs, author it in
`packages/examples/src/scenes/<name>.tsx` and register it in
`packages/examples/vite.config.ts` instead — but the template is the quickest
iteration loop.

## Building a fresh checkout

The template's `vite.config.ts` imports several sibling packages from their
*built* output, so on a fresh checkout (no `node_modules`, no `lib/`) you must
install and build them before the dev server or `template:build` will resolve:

```bash
pnpm install
pnpm core:build
pnpm 2d:build
pnpm --filter @canvas-commons/vite-plugin build
pnpm --filter @canvas-commons/ffmpeg build
pnpm --filter @canvas-commons/player build
pnpm --filter @canvas-commons/editor build
```

After that, `pnpm template:build` (runs `tsc` then `vite build`) is the
fast type-check + bundle gate for your scene. If `template:build` fails with
"Failed to resolve entry for package @canvas-commons/<x>", that package hasn't
been built yet — build it.

If you only changed scene `.tsx`/`.meta` files and the packages are already
built, `pnpm template:build` alone is enough to type-check.

## Running the dev server

```bash
pnpm template:dev      # editor at http://localhost:9000
```

**Run it backgrounded and redirect to a file** — never pipe it through `head`
or `tail`. A long-lived server piped to `head` gets SIGPIPE'd and dies the
moment `head` closes the pipe, which looks like a mysterious "server exited"
or "Execution context was destroyed" failure. Good:

```bash
pnpm template:dev > /tmp/cc-dev.log 2>&1 &     # or the harness's background mode
# then poll until ready:
until curl -sf -o /dev/null http://localhost:9000/; do sleep 1; done
```

To restart cleanly, kill whatever holds the port first:
`lsof -ti :9000 | xargs kill -9`.

## How frame capture works (the verification loop)

The editor exposes a debug surface on `window.commons`:

- `window.commons.player.playback` → `{ duration (frames), fps, currentScene }`
- `window.commons.meta.getFullRenderingSettings()` → render settings
- `window.commons.renderer.render({...settings, range, exporter})` → renders a
  time `range` (in seconds) using an exporter
- `window.commons.project.name`

The **image-sequence exporter** (`@canvas-commons/core/image-sequence`) writes
PNGs back through the dev server to disk under the *project package's*
`output/<projectName>/<sceneName>/` directory (with `groupByScene: true`). That
is why capture must know which package is running the server.

`scripts/capture-frames.mjs` automates this: it connects a headless browser to
the dev server, triggers renders for sampled timeline positions (or the whole
scene), captures any `console.error`/`pageerror`, and copies the produced PNGs
to an output dir so you can Read them. See the script header for flags.

Playwright is the browser driver. In canvas-commons it lives in
`packages/e2e/node_modules` (pnpm does not hoist it); the script discovers it by
scanning `packages/*/node_modules`. If no browser binary is installed:

```bash
pnpm --filter @canvas-commons/e2e exec playwright install chromium-headless-shell
```

## Encoding to video

After a full render (`capture-frames.mjs --all`), the sequential PNGs can be fed
straight to ffmpeg, or use the script's `--encode out.mp4`:

```bash
node capture-frames.mjs --all --scale 1 --encode animation.mp4
# equivalent manual step from the scene output dir:
ffmpeg -y -framerate <fps> -i %06d.png -c:v libx264 -pix_fmt yuv420p \
  -crf 18 -movflags +faststart animation.mp4
```

Canvas Commons also ships a built-in video exporter usable from the editor UI
(see `references/docs/getting-started/rendering/`), but the ffmpeg-from-frames
path is the most scriptable for headless work.
