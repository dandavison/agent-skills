# Vendored Canvas Commons / Motion Canvas documentation

The framework's prose docs, copied verbatim (the API is identical between the
two projects). These are `.mdx` written for the Docusaurus site, so they contain
import lines and `<Tabs>`/`<TabItem>`/`<ApiSnippet>` components — ignore that
scaffolding and read the prose and code blocks.

Most useful for authoring, in rough priority order:

- `getting-started/flow.mdx` — generators, `yield` / `yield*`, the core model.
- `getting-started/tweening.mdx` — animating properties, easing, `.to()` chains.
- `getting-started/signals.mdx` — reactive values and computed signals.
- `getting-started/positioning.mdx` — coordinate frames and conversions.
- `getting-started/layouts.mdx` — flex layout for automatic arrangement.
- `getting-started/references.mdx` — `createRef`, `makeRef`, refs in loops.
- `getting-started/transitions.mdx` — scene transitions.
- `getting-started/time-events.mdx` — `waitUntil` labels and the timeline.
- `getting-started/media.mdx`, `effects.mdx`, `presentation.mdx`,
  `rendering/` — assets, generators-as-effects, presenting, exporting.
- `components/` — `code/` (syntax-highlighted code blocks), `latex.mdx`,
  `path.mdx`, `spline.mdx`, `bezier.mdx`, `custom-components.mdx`.
- `advanced/` — filters/effects, shaders, plugins, random, project variables.
- `migration/` — version migration notes.

For the condensed, gotcha-focused version, see `../api-cheatsheet.md` first.
