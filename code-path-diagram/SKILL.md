---
name: code-path-diagram
description: >
  Generate d2 diagrams that visualize code path mechanics — call flows, cache interactions,
  persistence boundaries, decorator chains, branching logic, and error paths. Use this skill
  whenever the user asks to diagram, visualize, or map out how code paths work, how requests
  flow through a system, what happens during a specific operation, or how components interact
  at the code level. Also use when the user says things like "trace the execution path",
  "show me how X works as a diagram", "create a call graph", "map the code flow", or
  "I want a visual of the code path for Y". This produces .d2 diagram source files that
  render with the d2 CLI.
---

# Code Path Diagram

Generate a d2 diagram that explains how a specific area of code works by tracing execution
paths, showing decision points, and highlighting architectural boundaries (cache vs persistence,
decorators/wrappers, error paths).

## When to use

The user describes an area of codebase mechanics they want visualized. Examples:
- "Diagram the StartActivity execution path"
- "Show me how the workflow cache handles lookups"
- "Map out the persistence write path for creating executions"
- "Trace what happens when a Poll request comes in"

## Process

### 1. Clarify scope

Ask the user:
- Which code path or operation to diagram
- Whether to include specific variants (e.g., cache hit vs miss, error paths, decorator chains)
- Where to write the output (default: `.task/` in the current repo)

If the user's request is already specific enough, skip straight to research.

### 2. Research the code paths

Trace the execution by reading source files. Follow function calls from the entry point
downward. At each step, note:

- **Function name and location** (file:line)
- **What the function does** in one phrase
- **Decision points** — conditionals that branch the path (cache hit/miss, error/success, config flags)
- **Boundary crossings** — transitions between architectural layers (in-memory to persistence,
  Go code to SQL, application to external storage)
- **Decorator/wrapper chains** — if the call passes through middleware, rate limiters, metrics
  wrappers, or other decorators, trace the full chain

Build a mental model of the flow before writing any d2. Identify which nodes belong to which
category (see color scheme below).

### 3. Write the d2 diagram

Read the two reference examples before writing:
- `references/example-oss.d2` — a clean single-codebase diagram
- `references/example-cloud.d2` — same paths but showing a decorator/wrapper layer

These are the gold standard. Study their structure, then produce output of equivalent quality.

#### Structure

```
direction: down

# Legend at top (horizontal)
legend: { ... }

# Entry points / handler operations (grouped)
handler: { ... }

# Divergent paths (labeled sections)
# Each major path gets its own section with a comment header

# Nodes and edges, organized by path
```

#### Color scheme

Use these colors consistently. Include a legend at the top of every diagram showing which
colors are used (only include colors that appear in the diagram).

| Category | Fill | Stroke | When to use |
|----------|------|--------|-------------|
| In-memory / cache | `#ffe066` | `#8a6d00` | LRU lookups, cache keys, MutableState in memory |
| Persistence / DB | `#f5a0a0` | `#a01010` | SQL queries, DB reads/writes, persistence store calls |
| External storage | `#f5d6a0` | `#a06010` | S3, blob storage, tiered storage |
| Decorator / wrapper | `#b8d4f0` | `#1a5276` | Middleware chains, rate limiters, metrics wrappers |
| Entry point (primary) | `#b8e6b8` | `#1a6b1a` | The main operation being diagrammed |
| Entry point (secondary) | `#c8b8e8` | `#4a2d8a` | Related operations shown for context |
| Neutral / logic | `#ffffff` | (default) | Regular function calls, branching logic |

All colored nodes should set `style.stroke-width: 3` (for cache/persistence/storage/decorator)
or `style.stroke-width: 2` (for entry points).

#### Node design

Each node label should contain enough context to understand it without opening the source:

```
node_id: "functionName\nfile.go:123\nBrief description of what happens" {
  style.fill: "#ffe066"
  style.stroke: "#8a6d00"
  style.stroke-width: 3
  link: "https://github.com/org/repo/blob/commit/path/to/file.go#L123"
}
```

For cache keys or other structural data, use italic:
```
cache_key: "Cache Key:\n{field1, field2, field3}" {
  style.fill: "#ffe066"
  style.stroke: "#8a6d00"
  style.stroke-width: 3
  style.italic: true
}
```

#### Edge design

- **Normal flow**: no special styling
- **Colored boundary crossings**: match the stroke color of the target category
  ```
  node_a -> node_b: "description" {
    style.stroke: "#a01010"
    style.stroke-width: 3
  }
  ```
- **Conditional / error paths**: dashed lines
  ```
  node_a -> node_b: "error case" {
    style.stroke-dash: 5
    style.stroke-width: 3
  }
  ```
- **Cache hit/miss**: use colored edges matching the cache color for hits,
  persistence color for misses

#### Source links

Every node that references a function must include a `link:` with a line number. Links must
be **GitHub permalink URLs using an explicit commit SHA** — never use branch names like `main`
or `master` in URLs, because those are moving targets and the diagram becomes inaccurate as
soon as the branch advances.

Determine the GitHub remote URL and the SHA to link to:
```bash
git remote get-url origin
```

The user may not have `main` checked out. Ask them which SHA they want the links to point at
if it's not obvious. Typically this is the HEAD of `main` or `master` on the remote, since
the diagram is meant to be useful to anyone reading it. Get the SHA:
```bash
git rev-parse --short origin/main   # or origin/master
```

Construct links as:
```
https://github.com/org/repo/blob/<sha>/path/to/file.go#L123
```

For line ranges:
```
https://github.com/org/repo/blob/<sha>/path/to/file.go#L108-L124
```

Every link must include `#L<number>` (or `#L<start>-L<end>` for ranges). A link without a
line number is useless — the reader would have to search the file to find the relevant code.

#### d2 source organization

Use comment headers to organize sections:
```
# ================================================================
# SECTION NAME
# ================================================================
```

And sub-sections:
```
# ----------------------------------------------------------------
# Sub-section name
# ----------------------------------------------------------------
```

### 4. Verify and render

Compile the diagram and render it to SVG. Check if `d2` is installed first:

```bash
which d2
```

If d2 is available, render the SVG alongside the d2 source:

```bash
d2 <output-file>.d2 <output-file>.svg
```

Fix any d2 compilation errors before presenting to the user.

### 5. Present

Give the user the path to the rendered SVG file — this is what they want to click on
and view. Also mention the d2 source path for future edits. If d2 is not installed,
give the d2 source path and tell them to install d2 (`brew install d2`) to render it.

## Common patterns

### Showing cache hit vs miss

Create separate nodes for the hit and miss outcomes, with colored edges:

```
cache_lookup -> hit_result: "cache hit" {
  style.stroke: "#8a6d00"   # cache color
  style.stroke-width: 3
}
cache_lookup -> miss_path: "cache miss" {
  style.stroke: "#a01010"   # persistence color
  style.stroke-width: 3
}
```

### Showing decorator chains

When calls pass through a chain of wrappers, show the chain as a single labeled node
with the chain described in the label or on the edge:

```
wrapper_node: "Cloud ExecutionManager decorator chain\n(saas-temporal)\n\nMethod X is NOT overridden\n— passes straight through" {
  style.fill: "#b8d4f0"
  style.stroke: "#1a5276"
  style.stroke-width: 3
}
source -> wrapper_node
wrapper_node -> target: "rate limiter\n-> metrics\n-> retry\n-> OSS impl"
```

### Invisible ordering edges

To control layout without visible connections:
```
legend -> handler: {
  style.opacity: 0
}
```
