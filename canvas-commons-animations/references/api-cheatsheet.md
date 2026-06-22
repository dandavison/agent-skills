# Canvas Commons / Motion Canvas authoring cheatsheet

Canvas Commons is a maintained fork of Motion Canvas; the API is the same. Only
the package scope differs: `@canvas-commons/2d` and `@canvas-commons/core` here,
`@motion-canvas/2d` and `@motion-canvas/core` upstream. Everything below applies
to both.

This is a quick reference for the things that actually trip you up. For
conceptual depth, read the vendored prose docs under `references/docs/`
(start with `getting-started/flow.mdx`, `tweening.mdx`, `signals.mdx`,
`positioning.mdx`, `layouts.mdx`).

## The mental model (three things that look familiar and aren't)

- **JSX builds a retained scene graph, not a virtual DOM.** A `<Rect>` returns a
  long-lived `Node` you keep a reference to and mutate over time. There is no
  reconciler, no re-render, no diff. You construct nodes once, then animate them
  by driving their signal-backed properties.
- **A scene is a generator function.** `yield` = "this frame is ready, show it";
  `yield*` delegates to another animation generator. Time only advances when you
  yield. Plain code between yields runs in zero scene-time.
- **`@canvas-commons/core` signals are not `@preact/signals`.** The editor UI
  uses Preact signals; animation state uses core signals (`createSignal`,
  `createComputed`). Same surface syntax, unrelated implementations. Never mix.

## Scene skeleton

```tsx
import {makeScene2D, Rect, Txt} from '@canvas-commons/2d';
import {createRef, all, waitFor, createSignal} from '@canvas-commons/core';

export default makeScene2D(function* (view) {
  view.fill('#101317'); // background

  const box = createRef<Rect>();
  view.add(<Rect ref={box} size={120} fill={'#4a90d9'} />);

  yield* box().position.x(300, 1);   // animate x to 300 over 1s
  yield* waitFor(0.5);
});
```

Two equivalent construction styles — use whichever is cleaner for the case:

```tsx
// JSX + ref (good for nested trees authored declaratively)
const box = createRef<Rect>();
view.add(<Rect ref={box} size={120} />);
box().fill('red');

// Direct constructor (good for programmatic creation in loops)
const box = new Rect({size: 120});
view.add(box);
box.fill('red');
```

## Animating properties (tweens)

Every animatable property is callable:

```tsx
node.position.x(value, duration, easing?)   // tween to value over duration
node.opacity(1, 0.3)
node.fill('#ff0000', 0.4)
node.scale(1.2, 0.2).to(1, 0.3)             // CHAIN tweens with .to()
node.rotation(90, 1, easeInOutCubic)        // optional easing fn
```

- `node.prop()` (no args) reads the current value.
- `node.prop(value)` (no duration) sets instantly.
- `node.prop(value, duration)` returns a tween you `yield*`.
- `.to(value, duration)` chains another leg onto a tween.

## Flow control

```tsx
yield* all(a, b, c);          // run tweens in parallel, finish together
yield* sequence(0.2, a, b);   // start each 0.2s after the previous (stagger)
yield* chain(a, b, c);        // strictly one after another
yield* waitFor(seconds);
yield* waitUntil('label');    // time-event marker (see time-events.mdx)
yield* loop(5, i => ...);     // repeat
```

Common easings from `@canvas-commons/core`: `linear`, `easeInOutCubic`,
`easeInExpo`, `easeOutBack`, etc.

## Signals (reactive values, incl. live-updating text)

```tsx
const count = createSignal(0);
const label = createComputed(() => `n = ${count()}`);

// Text that re-renders whenever the signal changes:
view.add(<Txt text={() => `admitted ${count()}`} />);

count(5);              // set
count(count() + 1);    // increment
yield* count(100, 2);  // tween a signal numerically over 2s
```

Passing a function as a prop makes it reactive — the node tracks the signals
read inside and updates automatically.

## Coordinates and layout

- The view is centered at the origin. **+x is right, +y is DOWN.**
- Default scene size is 1920×1080, so without scaling x ≈ [-960, 960],
  y ≈ [-540, 540]. (Capture/preview may downscale, but coordinates are unscaled.)
- A child's `position` is relative to its parent. `node.absolutePosition()` and
  the `.relativeTo()` / `.view()` / `.local()` variants convert between frames
  (see `positioning.mdx`).
- For automatic stacking/rows, use `<Layout>` / flex props rather than manual
  coordinates (see `layouts.mdx`).
- `node.reparent(newParent)` moves a node and preserves its absolute transform —
  the standard way to "hand off" a node from one container to another mid-scene.

## Common nodes

`Rect`, `Circle`, `Txt`, `Line`, `Node` (transform-only group), `Layout`,
`Img`, `Path`, `Spline`, `Code` (syntax-highlighted). `Node` is useful as an
invisible group you position/animate as a unit (e.g. a label + marker that move
together).

## Gotchas that waste time

- **`ThreadGenerator` returns `void`.** You cannot do
  `const x = yield* myGen()` to get a value out of an animation helper. If a
  helper needs to hand back a node, construct the node *outside* and pass it in,
  or return it from a plain (non-generator) function called before the
  `yield*`. This is the single most common authoring mistake.
- **Null assertions (`!`) and `any` are disallowed** by repo lint. Type refs as
  `createRef<Rect>()`; guard instead of asserting.
- **Each scene file needs a sibling `.meta` file** and must be registered in the
  project (`src/project.ts`). A minimal meta is
  `{"version": 1, "timeEvents": [], "seed": <int>}`.
- **Reactive props need a function, not a value.** `text={`n ${count()}`}` is
  evaluated once; `text={() => `n ${count()}`}` stays live.
- **Don't animate the same property in two parallel tweens** — the last writer
  wins and the motion looks broken. Split into sequential legs or animate
  different properties.
- **Text and box collisions are invisible to the type-checker.** Only frame
  capture (below) catches a label overlapping a border or a node off-screen.
