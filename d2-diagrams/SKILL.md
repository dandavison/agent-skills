---
name: d2-diagrams
description: >
  Create d2 diagrams — architecture, flowcharts, sequence diagrams, ER diagrams, UML class
  diagrams, grid layouts, and multi-board compositions. Use this skill when the user
  explicitly mentions d2: "create a d2 diagram", "write a .d2 file", "make this in d2",
  "d2 sequence diagram", etc. Also use when editing or fixing existing .d2 files.
  Do NOT use for code-path diagrams (use code-path-diagram skill instead).
---

# D2 Diagrams

Create d2 diagrams for any purpose: system architecture, data flow, sequence interactions,
database schemas, class hierarchies, grid layouts, and multi-board compositions.

## When to use

The user wants a visual diagram and either explicitly asks for d2 or asks for a diagram
type that d2 handles well. Examples:
- "Create an architecture diagram showing how the services connect"
- "Draw a sequence diagram of the auth flow"
- "Make an ER diagram for these database tables"
- "Lay out a grid showing all 12 microservices"
- "Diagram the deployment pipeline with different scenarios"
- "I need a class diagram for this data model"

## Process

### 1. Understand what the user wants

Determine:
- **Diagram type** — which d2 feature to use (see diagram type guide below)
- **Content** — what entities, relationships, and labels to include
- **Output path** — where to write the file (default: working directory or `.task/`)

If the request is clear, skip straight to reading docs and writing.

### 2. Read the relevant docs

The `docs/` subdirectory (relative to this skill file) contains comprehensive d2 reference
documentation. Read only what you need for the diagram at hand:

| Diagram type | Read these docs |
|-------------|----------------|
| Architecture / flowchart / general | `shapes.md`, `containers.md`, `connections.md` |
| Sequence diagram | `sequence-diagrams.md`, `connections.md` |
| Grid / dashboard layout | `grid-diagrams.md` |
| ER / database schema | `sql-tables.md`, `connections.md` |
| UML class diagram | `uml-classes.md`, `connections.md` |
| Multi-board (scenarios/steps) | `composition.md` |
| Any diagram needing styling | `style.md`, `themes.md`, `icons.md` |
| Positioning / layout control | `layouts.md`, `positioning.md` |
| Reusable styles | `classes-reuse.md`, `vars.md`, `globs.md` |
| Text / labels / code blocks | `text.md` |
| Tooltips / links | `interactive.md` |
| CLI flags / rendering | `cli.md` |

Always read the docs before writing d2 — they contain the exact syntax and valid values.
Don't rely on memory for d2 specifics; the docs are the source of truth.

### 3. Write the d2 file

#### Diagram type guide

**Standard graphs** (architecture, flowcharts, call graphs, data flow):
```d2
direction: right

client: Client
server: Backend Server {
  api: API Gateway
  auth: Auth Service
  db: Database {
    shape: cylinder
  }
}
client -> server.api: HTTPS
server.api -> server.auth: validate
server.api -> server.db: query
```

**Sequence diagrams** — set `shape: sequence_diagram` on a container. Order of declarations
controls visual order. All actors share scope within the sequence container:
```d2
auth_flow: {
  shape: sequence_diagram
  client
  api
  auth
  db

  client -> api: POST /login
  api -> auth: validate credentials
  auth -> db: lookup user
  db -> auth: user record
  auth -> api: JWT token
  api -> client: 200 OK + token
}
```

**Grid diagrams** — use `grid-rows` and/or `grid-columns` for matrix layouts:
```d2
services: {
  grid-columns: 3
  grid-gap: 20
  svc_a: Service A
  svc_b: Service B
  svc_c: Service C
  svc_d: Service D
  svc_e: Service E
  svc_f: Service F
}
```

**SQL table diagrams** — use `shape: sql_table` with typed columns and constraints:
```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  email: varchar {constraint: unique}
  name: varchar
}
posts: {
  shape: sql_table
  id: int {constraint: primary_key}
  user_id: int {constraint: foreign_key}
  title: varchar
  body: text
}
posts.user_id -> users.id
```

**UML class diagrams** — use `shape: class` with visibility prefixes (`+`/`-`/`#`):
```d2
Animal: {
  shape: class
  +name: string
  #age: int
  +speak(): string
}
Dog: {
  shape: class
  +breed: string
  +speak(): string
}
Dog -> Animal: inherits
```

**Multi-board compositions** — use `layers` (independent), `scenarios` (inherit from base),
or `steps` (inherit from previous step):
```d2
server -> db: query

scenarios: {
  healthy: {
    db -> server: result
    server -> client: 200
  }
  failure: {
    db -> server: timeout {
      style.stroke: red
      style.stroke-dash: 5
    }
    server -> client: 503
  }
}
```

#### Styling guidelines

Apply styling intentionally to convey meaning — color-code categories of nodes, use dashed
lines for optional/error paths, use `animated: true` for active flows. If the diagram has
a color scheme, add a legend:

```d2
legend: {
  direction: right
  service: Service {style.fill: "#b8e6b8"}
  database: Database {style.fill: "#f5a0a0"}
  external: External {style.fill: "#f5d6a0"}
}
```

For consistent styling across many nodes, use classes:
```d2
classes: {
  db: {
    style.fill: "#f5a0a0"
    style.stroke: "#a01010"
    style.stroke-width: 2
  }
}
primary_db.class: db
replica_db.class: db
```

#### Source organization

Use comment headers for sections in larger diagrams:
```d2
# ================================================================
# SECTION NAME
# ================================================================
```

### 4. Verify and render

Check if d2 is installed:
```bash
which d2
```

If available, compile and render:
```bash
d2 <output>.d2 <output>.svg
```

Fix any compilation errors before presenting. Common errors:
- Referencing a shape key that doesn't exist (typo or case mismatch)
- Invalid shape type name
- Syntax errors in nested blocks (mismatched braces)

### 5. Present

Give the user the SVG path to view and the d2 source path for future edits.
If d2 is not installed, give the source path and suggest `brew install d2`.

## Gotchas

These are easy mistakes to make with d2 — be aware of them:

- **Keys are case-insensitive**: `PostgreSQL` and `postgresql` reference the same shape
- **Connections reference keys, not labels**: if `pg: PostgreSQL`, connect with `pg ->` not `PostgreSQL ->`
- **Sequence diagram ordering matters**: declaration order = visual order (unlike other d2 diagrams)
- **Repeated connections create additional edges**: `a -> b` twice means two separate arrows
- **`near` positioning** only works reliably with the TALA layout engine
- **SQL reserved words** in sql_table columns must be quoted: `"select": varchar`
- **URL fragments** (`#`) in links are treated as comments if unquoted — always quote URLs with `#`
- **Sequence diagram scope**: actors referenced inside groups refer to top-level actors (shared scope)
- **Grid fill order**: when both `grid-rows` and `grid-columns` are set, whichever keyword appears first determines the dominant fill direction
