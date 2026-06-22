---
name: canvas-commons-animations
description: >-
  Create, edit, and verify programmatic animations in Canvas Commons or Motion
  Canvas — the TypeScript framework where scenes are generator functions and a
  JSX-built retained scene graph is animated by driving signal-backed
  properties. Use this whenever the user wants to build, modify, or debug an
  animation, scene, motion graphic, explainer, or visualization in this
  framework: anything mentioning Canvas Commons, Motion Canvas, makeScene2D,
  @canvas-commons/2d or @motion-canvas/2d, a .tsx "scene", tweens/signals/flow
  animation, or rendering such a scene to frames or video. Also use it when the
  user points at the canvas-commons / motion-canvas repo and asks to "animate
  X", "make an animation of Y", or capture/preview/render frames of a scene —
  even if they don't name the framework explicitly. Critically, this skill
  carries the headless frame-capture loop for visually verifying an animation,
  which type-checking and building cannot do; reach for it any time animation
  output needs to be seen, not just compiled.
---

# Canvas Commons / Motion Canvas animations

Canvas Commons is a maintained fork of Motion Canvas with an identical API;
only the package scope differs (`@canvas-commons/*` vs `@motion-canvas/*`).
Everything here applies to both.

The defining trait of this framework, and the reason it needs a skill: an
animation is **code that produces motion you cannot see by reading it**. A scene
type-checks and builds while a label sits off-screen, two boxes overlap, or the
timing is wrong. So the workflow is not "write it and ship" — it is "write it,
**render frames, and look at them**." That verification loop is the core of this
skill.

## Before touching this repo

The canvas-commons repo's `AGENTS.md` requires that contributors review the
project AI policy. Surface this link to the user once and let them decide before
contributing upstream:
https://github.com/canvas-commons/.github/blob/main/AI_POLICY.md
(For purely local work in their own fork this is informational.)

## Reference material (read as needed)

- `references/api-cheatsheet.md` — the authoring API and the gotchas that waste
  time (read this before writing any non-trivial scene).
- `references/setup-and-build.md` — fresh-checkout build order, dev server
  operation, and exactly how frame capture works.
- `references/docs/` — the framework's full prose documentation, vendored.
  Reach for a specific topic when the cheatsheet isn't enough:
  `getting-started/flow.mdx` (generators), `tweening.mdx`, `signals.mdx`,
  `positioning.mdx`, `layouts.mdx`, `code/` (code blocks), `latex.mdx`,
  `media.mdx`, `transitions.mdx`, plus `advanced/` and `components/`.
- `scripts/capture-frames.mjs` — the headless frame-capture / render tool.

## Workflow

### 1. Understand the API first

If you haven't worked in this framework recently, read
`references/api-cheatsheet.md`. The three things that catch people: JSX returns
long-lived nodes (not a virtual DOM), scenes are generators where time advances
only on `yield`, and core signals are not Preact signals. The single most
common bug is trying to `const x = yield* helper()` — `ThreadGenerator` returns
`void`, so construct nodes outside generators and pass them in.

### 2. Place and author the scene

Develop in the **template** package for the fastest loop (details and the
docs-examples alternative in `references/setup-and-build.md`):

- `packages/template/src/scenes/<name>.tsx` + a sibling `<name>.meta`
  (`{"version": 1, "timeEvents": [], "seed": <int>}`)
- register it in `packages/template/src/project.ts`

Write for an expert reader: terse, well-named, comments only where the *why*
isn't obvious. Match the style of existing scenes. Structure long scenes as
small generator helpers (`function* step(): ThreadGenerator { ... }`) called in
sequence, with a short caption/section approach if the animation is
explanatory.

### 3. Type-check and build

```bash
pnpm template:build      # tsc + vite build — the fast correctness gate
```

On a fresh checkout this needs several packages built first; see
`references/setup-and-build.md`. A green build proves it compiles — it proves
nothing about how it looks.

### 4. Render frames and LOOK at them (the step that matters)

Start the dev server backgrounded (never pipe a long-lived server through
`head`/`tail` — it gets SIGPIPE'd and dies):

```bash
pnpm template:dev > /tmp/cc-dev.log 2>&1 &
until curl -sf -o /dev/null http://localhost:9000/; do sleep 1; done
```

Then capture frames sampled across the timeline and read them:

```bash
node <skill>/scripts/capture-frames.mjs \
  --project-dir packages/template --fractions 0,0.2,0.4,0.6,0.8,1
```

It prints the captured PNG paths (and any runtime `console.error`/`pageerror`).
**Read each PNG** with the image-reading tool and check, concretely:

- Nothing important is off-screen or clipped by the view edges.
- No text overlaps a border, another label, or a shape it shouldn't.
- Colors/states are what the moment intends (e.g. the "failed" item is red).
- The timeline reads correctly — the frame at 0.5 shows the mid-point you meant.

This catches the class of defect that builds and type-checks miss. In practice
it routinely surfaces label/box collisions and off-by-a-bit positions; fix the
scene and re-capture. When iterating on one moment, capture a single fraction
(e.g. `--fractions 0.5`) to keep it fast.

### 5. Iterate

Edit the scene, re-run `template:build`, re-capture the affected fractions,
re-read. Repeat until each sampled frame is right. The dev server hot-reloads,
so you usually don't restart it between edits.

### 6. Encode to video (when asked)

```bash
node <skill>/scripts/capture-frames.mjs --project-dir packages/template \
  --all --scale 1 --encode animation.mp4
```

`--all` renders every frame at full resolution; `--encode` runs ffmpeg over the
sequence. (Manual ffmpeg and the editor's built-in exporter are covered in
`references/setup-and-build.md`.)

## Committing

If the user wants the work committed, follow the repo's Angular commit
convention (`<type>(<scope>): <subject>`, imperative, ≤50 char subject). Scene
work in `template`/`examples` is internal and does not need a changeset; runtime
changes to `core`/`2d`/etc. do. Don't push or open PRs unless asked; PRs go in
draft. The `output/` and `.cc-frames/` capture artifacts are scratch — don't
commit them (template/examples already gitignore `output/`).

## Scope note

This skill is for building animations *with* the framework and verifying them.
For changes to the framework's own runtime packages (`core`, `2d`, `editor`,
`vite-plugin`, `player`, `ffmpeg`), the repo's per-package `AGENTS.md` files and
the e2e visual-regression suite are the authority; this skill's capture loop is
still a useful way to eyeball the effect of such changes on a real scene.
