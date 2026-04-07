# D2 Layout Engines

Source: https://d2lang.com/tour/layouts

## Available Engines

1. **dagre** (default, bundled): Fast directed graph layout. Layered/hierarchical. Based on Graphviz DOT.
2. **elk** (bundled): Eclipse Layout Kernel. More mature, good for directed graphs.
3. **tala** (commercial): Purpose-built for software architecture diagrams. Most features.

## Setting the Engine

```bash
d2 --layout=elk input.d2 output.svg
# or
D2_LAYOUT=elk d2 input.d2 output.svg
```

List engines: `d2 layout`
Engine options: `d2 layout dagre`

## Direction

```d2
direction: right
```

Values: `up`, `down`, `right`, `left`

Only TALA supports per-container direction. Others are global only.

## Feature Matrix

| Feature | dagre | elk | tala |
|---------|-------|-----|------|
| `near` object refs | no | no | yes |
| Container `width`/`height` | no | yes | adding |
| Position locking (`top`/`left`) | no | no | yes |
| Ancestor-to-descendant connections | no | yes | yes |
| Per-container `direction` | no | no | yes |
