---
name: d2
description: |
  The D2 diagram language: language reference, examples, and CLI documentation,
  generated from the D2 source and docs repositories vendored in this skill.
  Diagrams are rendered with the TALA layout engine.
---


# D2

Render with TALA, D2's layout engine for software architecture diagrams; use another
engine only when asked:

```sh
d2 --layout=tala in.d2 out.svg
d2 validate in.d2
d2 fmt in.d2
```

Two things below are stale: `d2 --help` and the tour present `dagre` as the default,
and `tour/tala.md` calls TALA proprietary, paid, and a separate install. As of v0.9.0
TALA is bundled with `d2` and open source.


## Diagramming an application built on Temporal

Use these conventions for any diagram of a system built on Temporal. They exist to keep apart the
two things readers conflate: server-side state, and the user code that acts on it.

| Element | Meaning |
|---|---|
| A **Temporal** box | Exactly one namespace; label it `Temporal — <namespace>`. Two namespaces are two boxes, since that is a separate Frontend to talk to and in general a separate cell. |
| A box **inside** a Temporal box | One execution — workflow, activity, Nexus operation, schedule. Server-side state, never code. |
| A **dashed container** | One worker or client process, holding the user code that corresponds to those executions. Label it with something the reader could run. |
| A **solid** arrow | A request, drawn sender → receiver. |
| A **dashed** arrow | A response to a request the other side already made. |

Everything a worker receives arrives on a long poll it already has open, so **every task arrow is
dashed and points from Temporal to the worker**. Do not draw the poll itself: it is noise, and
drawing it makes the task look like an unsolicited push.

Further rules that make these diagrams readable:

- `direction: right`. These flows are wide, not tall.
- Number the steps in arrow labels, following one happy path. Order is otherwise unrecoverable
  from a box diagram, and a reader who cannot find the entry point reads nothing.
- Suffix a number with a letter (`6a`, `6b`) for steps that are concurrent, or alternatives, at the
  same point in the path; say which in the prose. Give a long-lived arrow — a subscription held open
  across the whole flow — the number of the step that opens it, and say it stays open.
- Label every arrow that crosses a process or namespace boundary with the actual API —
  `UpdateWorkflowExecution`, `Nexus StartOperation (HTTP)`, `RespondActivityTaskCompleted`. The API
  name is the most informative label available; never write "calls".
- Draw executions, not services. Frontend/History/Matching deserve a box only when they are the
  subject; in an application diagram they are where the reader stops seeing the application.
- One diagram per question. A topology diagram and a one-request sequence diagram over the same
  system are two diagrams.
- Put a `note` near the bottom for anything true of the whole diagram, including whether what is
  drawn actually exists yet.
- When you're done, verify arrow numbering, and verify the rendered output visually, checking for
  example that it is visually clear to which arrow each arrow label refers.

Worked example — a workflow calling a Nexus operation another namespace backs with an activity:

```d2
direction: right

cw: Caller worker — your code {
  style.stroke-dash: 3
  wfcode: Workflow code
}

t1: Temporal — caller namespace {
  wf: Workflow execution\n(NexusOperation component in its tree)
}

t2: Temporal — handler namespace {
  saa: Activity execution
}

hw: Handler worker — their code {
  style.stroke-dash: 3
  handler: Nexus operation handler
  act: Activity code
}

api: External API

cw.wfcode -> t1.wf: 1. RespondWorkflowTaskCompleted\n(ScheduleNexusOperation)
t1.wf -> t2: 2. Nexus StartOperation (HTTP)
t2 -> hw.handler: 3. Nexus task {style.stroke-dash: 3}
hw.handler -> t2.saa: 4. StartActivityExecution
t2 -> hw.act: 5. activity task {style.stroke-dash: 3}
hw.act -> api: 6. HTTP call
api -> hw.act: 7. response {style.stroke-dash: 3}
hw.act -> t2.saa: 8. RespondActivityTaskCompleted
t2.saa -> t1.wf: 9. Nexus completion callback (HTTP)
```


## Sources

Everything below is upstream material, assembled by `/Users/dan/src/devenv/skills/d2/generate-skill`
(regenerate with `make d2`) from:

- `/Users/dan/src/devenv/skills/d2/d2` — D2 source, v0.9.0-3-g65a01bdee
- `/Users/dan/src/devenv/skills/d2/d2-docs` — D2 language docs, 6a8db79
- `d2` on PATH — v0.9.0

Upstream material that is not inlined here is listed at the end.


## CLI

### `d2 --help`

```
d2 v0.9.0
Usage:
  d2 [--watch=false] [--theme=0] file.d2 [file.svg | file.png | file.pdf | file.pptx | file.gif | file.txt]
  d2 layout [name]
  d2 fmt file.d2 ...
  d2 play [--theme=0] [--sketch] file.d2
  d2 validate file.d2

d2 compiles and renders file.d2 to file.svg | file.png | file.pdf | file.pptx | file.gif | file.txt
It defaults to file.svg if an output path is not provided.

Use - to have d2 read from stdin or write to stdout.

PNG exports support up to 32768 pixels per dimension, subject to rendering resource limits.

See man d2 for more detailed docs.

Flags:
  -w, --watch                       $D2_WATCH               watch for changes to input and live reload. Use $HOST and $PORT to specify the listening address.
                                                            (default localhost:0, which will open on a randomly available local port). (default false)
  -h, --host string                 $HOST                   host listening address when used with watch (default "localhost")
  -p, --port string                 $PORT                   port listening address when used with watch (default "0")
  -b, --bundle                      $D2_BUNDLE              when outputting SVG, bundle all assets and layers into the output file (default true)
      --force-appendix              $D2_FORCE_APPENDIX      an appendix for tooltips and links is added to PNG exports since they are not interactive. --force-appendix adds an appendix to SVG exports as well (default false)
  -d, --debug                       $DEBUG                  print debug logs. (default false)
      --img-cache                   $IMG_CACHE              in watch mode, images used in icons are cached for subsequent compilations. This should be disabled if images might change. (default true)
  -l, --layout string               $D2_LAYOUT              the layout engine used (default "dagre")
  -t, --theme int                   $D2_THEME               the diagram theme ID (default 0)
      --dark-theme int              $D2_DARK_THEME          the theme to use when the viewer's browser is in dark mode. When left unset -theme is used for both light and dark mode. Be aware that explicit styles set in D2 code will still be applied and this may produce unexpected results. We plan on resolving this by making style maps in D2 light/dark mode specific. See https://github.com/d2lang/d2/issues/831. (default -1)
      --pad int                     $D2_PAD                 pixels padded around the rendered diagram (default 100)
      --animate-interval int        $D2_ANIMATE_INTERVAL    if given, multiple boards are packaged as 1 SVG which transitions through each board at the interval (in milliseconds). Can only be used with SVG or GIF exports. For GIF exports, defaults to 1000ms if not specified. (default 0)
      --timeout int                 $D2_TIMEOUT             the maximum number of seconds that D2 runs for before timing out and exiting. When rendering a large diagram, it is recommended to increase this value (default 120)
  -v, --version                                             get the version (default false)
  -s, --sketch                      $D2_SKETCH              render the diagram to look like it was sketched by hand (default false)
      --stdout-format string                                output format when writing to stdout (svg, png, ascii, txt, pdf, pptx, gif). Usage: d2 input.d2 --stdout-format png - > output.png (default "")
      --browser string              $BROWSER                browser executable that watch opens. Setting to 0 opens no browser. (default "")
  -c, --center                      $D2_CENTER              center the SVG in the containing viewbox, such as your browser screen (default false)
      --scale float                 $SCALE                  scale the output. E.g., 0.5 to halve the default size. Default -1 means that SVG's will fit to screen and all others will use their default render size. Setting to 1 turns off SVG fitting to screen. (default -1)
      --target string                                       target board to render. Pass an empty string to target root board. If target ends with '*', it will be rendered with all of its scenarios, steps, and layers. Otherwise, only the target board will be rendered. E.g. --target='' to render root board only or --target='layers.x.*' to render layer 'x' with all of its children. (default "*")
      --font-regular string         $D2_FONT_REGULAR        path to .ttf file to use for the regular font. If none provided, Source Sans Pro Regular is used. (default "")
      --font-italic string          $D2_FONT_ITALIC         path to .ttf file to use for the italic font. If none provided, Source Sans Pro Regular-Italic is used. (default "")
      --font-bold string            $D2_FONT_BOLD           path to .ttf file to use for the bold font. If none provided, Source Sans Pro Bold is used. (default "")
      --font-semibold string        $D2_FONT_SEMIBOLD       path to .ttf file to use for the semibold font. If none provided, Source Sans Pro Semibold is used. (default "")
      --font-mono string            $D2_FONT_MONO           path to .ttf file to use for the monospace font. If none provided, Source Code Pro Regular is used. (default "")
      --font-mono-bold string       $D2_FONT_MONO_BOLD      path to .ttf file to use for the monospace bold font. If none provided, Source Code Pro Bold is used. (default "")
      --font-mono-italic string     $D2_FONT_MONO_ITALIC    path to .ttf file to use for the monospace italic font. If none provided, Source Code Pro Italic is used. (default "")
      --font-mono-semibold string   $D2_FONT_MONO_SEMIBOLD  path to .ttf file to use for the monospace semibold font. If none provided, Source Code Pro Semibold is used. (default "")
      --check                       $D2_CHECK               check that the specified files are formatted correctly. (default false)
      --no-xml-tag                  $D2_NO_XML_TAG          omit XML tag (<?xml ...?>) from output SVG files. Useful when generating SVGs for direct HTML embedding (default false)
      --salt string                                         Add a salt value to ensure the output uses unique IDs. This is useful when generating multiple identical diagrams to be included in the same HTML doc, so that duplicate IDs do not cause invalid HTML. The salt value is a string that will be appended to IDs in the output. (default "")
      --omit-version                $OMIT_VERSION           omit D2 version from generated image (default false)
      --ascii-mode string           $D2_ASCII_MODE          ASCII rendering mode for text outputs. Options: 'standard' (basic ASCII chars) or 'extended' (Unicode chars) (default "extended")


Subcommands:
  d2 layout - Lists available layout engine options with short help
  d2 layout [name] - Display long help for a particular layout engine, including its configuration options
  d2 themes - Lists available themes
  d2 fmt file.d2 ... - Format passed files
	d2 play file.d2 - Opens the file in playground, an online web viewer (https://play.d2lang.com)
  d2 validate file.d2  - Validates file.d2

See more docs and the source code at https://github.com/d2lang/d2.
Hosted icons at https://icons.d2lang.com.
Playground runner at https://play.d2lang.com.
```

### `d2 layout`

```
Available layout engines found:

dagre (bundled) - The directed graph layout library Dagre
elk (bundled) - Eclipse Layout Kernel (ELK) with the Layered algorithm.
tala (bundled) - TALA is D2's native layout and edge-routing engine.

Usage:
  To use a particular layout engine, set the environment variable D2_LAYOUT=[name] or flag --layout=[name].

Example:
  D2_LAYOUT=dagre d2 in.d2 out.svg

Subcommands:
  d2 layout [layout name] - Display long help for a particular layout engine, including its configuration options

See more docs at https://d2lang.com/tour/layouts
```

### `d2 layout tala`

```
tala (bundled):

TALA is D2's native layout and edge-routing engine for software architecture diagrams.

Diagram data under tala-seeds takes precedence over the command-line flag.

Flags:
      --tala-seeds int64Slice     random seeds for deterministic TALA layout attempts; the best complete result is selected. (default [1,2,3])
```

### `d2 themes`

```
Available themes:
Light:
- Neutral Default: 0
- Neutral Grey: 1
- Flagship Terrastruct: 3
- Cool Classics: 4
- Mixed Berry Blue: 5
- Grape Soda: 6
- Aubergine: 7
- Colorblind Clear: 8
- Vanilla Nitro Cola: 100
- Orange Creamsicle: 101
- Shirley Temple: 102
- Earth Tones: 103
- Everglade Green: 104
- Buttered Toast: 105
- Terminal: 300
- Terminal Grayscale: 301
- Origami: 302
- C4: 303
Dark:
- Dark Mauve: 200
- Dark Flagship Terrastruct: 201
```


## Vocabulary

Exhaustive lists, extracted from `d2ast/keywords.go`, `d2target/d2target.go`, and `d2lsp/completion.go` in the D2 source.

- Keywords: `class`, `constraint`, `direction`, `grid-columns`, `grid-gap`, `grid-rows`, `height`, `horizontal-gap`, `icon`, `label`, `left`, `link`, `near`, `shape`, `tooltip`, `top`, `vars`, `vertical-gap`, `width`
- Keywords that only hold a map: `style`
- Keywords that hold a value or a map: `classes`, `constraint`, `icon`, `label`, `source-arrowhead`, `target-arrowhead`, `tooltip`
- Keywords that create a new board: `layers`, `scenarios`, `steps`
- `style.*` keywords: `3d`, `animated`, `bold`, `border-radius`, `double-border`, `fill`, `fill-pattern`, `filled`, `font`, `font-color`, `font-size`, `italic`, `multiple`, `opacity`, `shadow`, `stroke`, `stroke-dash`, `stroke-width`, `text-transform`, `underline`
- `shape` values: `rectangle`, `square`, `page`, `parallelogram`, `document`, `cylinder`, `queue`, `package`, `step`, `callout`, `stored_data`, `person`, `c4-person`, `diamond`, `oval`, `circle`, `hexagon`, `cloud`, `text`, `code`, `class`, `sql_table`, `image`, `sequence_diagram`, `hierarchy`
- `*-arrowhead.shape` values: `arrow`, `box`, `cf-many`, `cf-many-required`, `cf-one`, `cf-one-required`, `circle`, `cross`, `diamond`, `none`, `triangle`
- `near` constants: `top-left`, `top-center`, `top-right`, `center-left`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`
- `label.near` and `icon.near` positions: `top-left`, `top-center`, `top-right`, `center-left`, `center-center`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`, `outside-top-left`, `outside-top-center`, `outside-top-right`, `outside-left-top`, `outside-left-center`, `outside-left-bottom`, `outside-right-top`, `outside-right-center`, `outside-right-bottom`, `outside-bottom-left`, `outside-bottom-center`, `outside-bottom-right`, `border-top-left`, `border-top-center`, `border-top-right`, `border-left-top`, `border-left-center`, `border-left-bottom`, `border-right-top`, `border-right-center`, `border-right-bottom`, `border-bottom-left`, `border-bottom-center`, `border-bottom-right`
- `tooltip.near` positions: `top-left`, `top-center`, `top-right`, `center-left`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`
- `style.fill-pattern` values: `none`, `dots`, `lines`, `grain`, `paper`
- `style.text-transform` values: `none`, `uppercase`, `lowercase`, `capitalize`

### Value ranges

- `opacity`: number between 0.0 and 1.0, e.g. 0.4
- `stroke-width`: number between 0 and 15, e.g. 2
- `font-size`: number between 8 and 100, e.g. 14
- `stroke-dash`: number between 0 and 10, e.g. 5
- `border-radius`: number greater than or equal to 0, e.g. 4
- `font-color`, `stroke`, `fill`: color name or hex code, e.g. blue, #ff0000
- `width`, `height`, `top`, `left`: pixels, e.g. 400


## Language tour

### Hello World — `docs/tour/hello-world.md`

```d2
x -> y: hello world
```

This declares a connection between two shapes, `x` and `y`, with the label, `hello world`.

### Shapes — `docs/tour/shapes.md`

#### Basics

You can declare shapes like so:

```d2
imAShape
im_a_shape
im a shape
i'm a shape
# notice that one-hyphen is not a connection
# whereas, `a--shape` would be a connection
a-shape
```

You can also use semicolons to define multiple shapes on the same line:

```d2
SQLite; Cassandra
```

By default, a shape's label is the same as the shape's key. But if you want it to be different, assign a new label like so:

```d2
pg: PostgreSQL
```

By default, a shape's type is `rectangle`. To specify otherwise, provide the field `shape`:

```d2
Cloud: my cloud
Cloud.shape: cloud
```

#### Example

```d2
pg: PostgreSQL
Cloud: my cloud
Cloud.shape: cloud
SQLite
Cassandra
```

Keys are case-insensitive, so `postgresql` and `postgreSQL` will reference the same shape.

There are other values that `shape` can take, but they're special types that are covered
in the next section.

#### 1:1 Ratio shapes

Some shapes maintain a 1:1 aspect ratio, meaning their width and height are always equal.

- `circle`
- `square`

For these shapes, if you have a long label that make the shape wider, D2 will also make
the shape taller to maintain the 1:1 ratio.

If you manually set `width` and `height` on a 1:1 ratio shape, both dimensions will be set
to the larger of the two values to maintain the aspect ratio.

### Connections — `docs/tour/connections.md`

Connections define relationships between shapes.

#### Basics

Hyphens/arrows in between shapes define a connection.

```d2
Write Replica Canada <-> Write Replica Australia

Read Replica <- Master
Write Replica -> Master

Read Replica 1 -- Read Replica 2
```

If you reference an undeclared shape in a connection, it's created (as shown in the [hello
world](hello-world.md) example).

There are 4 valid ways to define a connection:

- `--`
- `->`
- `<-`
- `<->`

##### Connection labels

```d2
Read Replica 1 -- Read Replica 2: Kept in sync
```

##### Connections must reference a shape's key, not its label.

```d2
be: Backend
fe: Frontend

# This would create new shapes
Backend -> Frontend

# This would define a connection over existing labels
be -> fe
```

#### Example

```d2
Write Replica Canada <-> Write Replica Australia

Read Replica <- Master

x -- y

super long shape id here -> super long shape id even longer here
```

#### Repeated connections

Repeated connections do not override existing connections. They declare new ones.

```d2
Database -> S3: backup
Database -> S3
Database -> S3: backup
```

#### Connection chaining

For readability, it may look more natural to define multiple connection in a single line.

```d2
# The label applies to each connection in the chain.
High Mem Instance -> EC2 <- High CPU Instance: Hosted By
```

#### Cycles are okay

```d2
Stage One -> Stage Two -> Stage Three -> Stage Four
Stage Four -> Stage One: repeat
```

#### Arrowheads

To override the default arrowhead shape or give a label next to arrowheads, define a special shape on connections named `source-arrowhead` and/or `target-arrowhead`.

```d2
a: The best way to avoid responsibility is to say, "I've got responsibilities"
b: Whether weary or unweary, O man, do not rest
c: I still maintain the point that designing a monolithic kernel in 1991 is a

a -> b: To err is human, to moo bovine {
  source-arrowhead: 1
  target-arrowhead: * {
    shape: diamond
  }
}

b <-> c: "Reality is just a crutch for people who can't handle science fiction" {
  source-arrowhead.label: 1
  target-arrowhead: * {
    shape: diamond
    style.filled: true
  }
}

d: A black cat crossing your path signifies that the animal is going somewhere

d -> a -> c
```

- `triangle` (default)
  - Can be further styled as `style.filled: false`.
- `arrow` (like triangle but pointier)
- `diamond`
  - Can be further styled as `style.filled: true`.
- `circle`
  - Can be further styled as `style.filled: true`.
- `box`
  - Can be further styled as `style.filled: true`.
- `cf-one`, `cf-one-required` (cf stands for crows foot)
- `cf-many`, `cf-many-required`
- `cross`

It's recommended the arrowhead labels be kept short. They do not go through
autolayout for optimal positioning like regular labels do, so long arrowhead labels are
more likely to collide with surrounding objects.

If the connection does not have an endpoint, arrowheads won't do anything.

For example, the following will do nothing, because there is no source arrowhead.

```d2
x -> y: {
  source-arrowhead.shape: diamond
}
```

#### Referencing connections

You can reference a connection by specifying the original ID followed by its index.

```d2
x -> y: hi
x -> y: hello

(x -> y)[0].style.stroke: red
(x -> y)[1].style.stroke: blue
```

### Containers — `docs/tour/containers.md`

```d2
server
# Declares a shape inside of another shape
server.process

# Can declare the container and child in same line
im a parent.im a child

# Since connections can also declare keys, this works too
apartment.Bedroom.Bathroom -> office.Spare Room.Bathroom: Portal
```

#### Nested syntax

You can avoid repeating containers by creating nested maps.

```d2
clouds: {
  aws: {
    load_balancer -> api
    api -> db
  }
  gcloud: {
    auth -> db
  }

  gcloud -> aws
}
```

#### Container labels

There are two ways define container labels.

##### 1. Shorthand container labels

```d2-incomplete
gcloud: Google Cloud {
  ...
}
```

##### 2. Reserved keyword `label`

```d2-incomplete
gcloud: {
  label: Google Cloud
  ...
}
```

#### Example

```d2
clouds: {
  aws: AWS {
    load_balancer -> api
    api -> db
  }
  gcloud: Google Cloud {
    auth -> db
  }

  gcloud -> aws
}

users -> clouds.aws.load_balancer
users -> clouds.gcloud.auth

ci.deploys -> clouds
```

#### Reference parent

Sometimes you want to reference something outside of the container from within. The
underscore (`_`) refers to parent.

```d2
christmas: {
  presents
}
birthdays: {
  presents
  _.christmas.presents -> presents: regift
  _.christmas.style.fill: "#ACE1AF"
}
```

### Text — `docs/tour/text.md`

#### Standalone text is Markdown

```d2
explanation: |md
  # I can do headers
  - lists
  - lists

  And other normal markdown stuff
|
```

#### Markdown label

If you want to set a Markdown label on a shape, you must explicitly declare the shape.

```d2
explanation: |md
  # I can do headers
  - lists
  - lists

  And other normal markdown stuff
|
# Explicitly declare, even though the default shape is rectangle
explanation.shape: rectangle
```

#### Most languages are supported

D2 most likely supports any language you want to use, including non-Latin ones like
Chinese, Japanese, Korean, even emojis!

#### LaTeX

You can use `latex` or `tex` to specify a LaTeX language block.

```d2
plankton -> formula: will steal
formula: |latex
  \lim_{h \rightarrow 0 } \frac{f(x+h)-f(x)}{h}
|
```

A few things to note about LaTeX blocks:

- LaTeX blocks do not respect `font-size` styling. Instead, you must style these inside
  the Latex script itself with commands:
  - `\tiny{ }`
  - `\small{ }`
  - `\normal{ }`
  - `\large{ }`
  - `\huge{ }`
- Under the hood, this is using [MathJax](https://www.mathjax.org/). It is not full LaTeX
  (full LaTeX includes a document layout engine). D2's LaTeX blocks are meant to display
  mathematical notation, but not support the format of existing LaTeX documents. See
  [here](https://docs.mathjax.org/en/latest/input/tex/macros/index.html) for a list of all
  supported commands.

D2 runs on the latest version of MathJax, which has a lot of nice things but unfortunately
does not have linebreaks. You can kind of get around this with the `displaylines` command.
See below.

#### Code

Change `md` to a programming language for code blocks

```d2
explanation: |go
  awsSession := From(c.Request.Context())
  client := s3.New(awsSession)

  ctx, cancelFn := context.WithTimeout(c.Request.Context(), AWS_TIMEOUT)
  defer cancelFn()
|
```

See the [Chroma library](https://github.com/alecthomas/chroma?tab=readme-ov-file#supported-languages) for a full list of supported languages.

D2 also provides convenient short aliases:
- `md` → `markdown`
- `tex` → `latex`
- `js` → `javascript`
- `go` → `golang`
- `py` → `python`
- `rb` → `ruby`
- `ts` → `typescript`

If a language isn't recognized, D2 will fall back to plain text rendering without syntax highlighting.

#### Advanced: Non-Markdown text

In some cases, you may want non-Markdown text. Maybe you just don't like Markdown, or the
GitHub-styling of Markdown that D2 uses, or you want to quickly change a shape to text.
Just set `shape: text`.

```d2
title: A winning strategy {
  shape: text
  near: top-center
  style: {
    font-size: 55
    italic: true
  }
}

poll the people -> results
results -> unfavorable -> poll the people
results -> favorable -> will of the people
```

#### Advanced: Block strings

What if you're writing Typescript where the pipe symbol `|` is commonly used? Just add
another pipe, `||`.

```d2
my_code: ||ts
  declare function getSmallPet(): Fish | Bird;
||
```

Actually, Typescript uses `||` too, so that won't work. Let's keep going.

```d2
my_code: |||ts
  declare function getSmallPet(): Fish | Bird;
  const works = (a > 1) || (b < 2)
|||
```

There's probably some language or scenario where the triple pipe is used too. D2 actually
allows you to use any special symbols (not alphanumeric, space, or `_`) after the first pipe:

```d2
# Much cleaner!
my_code: |`ts
  declare function getSmallPet(): Fish | Bird;
  const works = (a > 1) || (b < 2)
`|
```

#### Advanced: LaTeX plugins

D2 includes the following LaTeX plugins:

```d2
grid-columns: 3
grid-gap: 100

*.style.fill: transparent
*.style.stroke: black

amscd plugin: {
  ex: |tex
    \begin{CD} B @>{\text{very long label}}>> C S^{{\mathcal{W}}_\Lambda}\otimes T @>j>> T\\ @VVV V \end{CD}
  |
}

braket plugin: {
  ex: |tex
    \bra{a}\ket{b}
  |
}

cancel plugin: {
  ex: |tex
    \cancel{Culture + 5}
  |
}

color plugin: {
  ex: |tex
    \textcolor{red}{y} = \textcolor{green}{\sin} x
  |
}

gensymb plugin: {
  ex: |tex
    \lambda = 10.6\,\micro\mathrm{m}
  |
}

mhchem plugin: {
  ex: |tex
    \ce{SO4^2- + Ba^2+ -> BaSO4 v}
  |
}

physics plugin: {
  ex: |tex
    \var{F[g(x)]}
    \dd(\cos\theta)
  |
}

multilines: {
  ex: |tex
    \displaylines{x = a + b \\ y = b + c}
    \sum_{k=1}^{n} h_{k} \int_{0}^{1} \bigl(\partial_{k} f(x_{k-1}+t h_{k} e_{k}) -\partial_{k} f(a)\bigr) \,dt
  |
}

asm: {
  ex: |latex
    \min_{ \mathclap{\substack{ x \in \mathbb{R}^n \ x \geq 0 \ Ax \leq b }}} c^T x
  |
}
```

### Icons — `docs/tour/icons.md`

We host a collection of icons commonly found in software architecture diagrams for free to
help you get started: [https://icons.d2lang.com](https://icons.d2lang.com).

Icons and images are an essential part of production-ready diagrams.

You can use any URL as value.

```d2
deploy: {
  icon: https://icons.d2lang.com/aws%2FDeveloper%20Tools%2FAWS-CodeDeploy.svg
}

backup: {
  icon: https://icons.d2lang.com/aws%2FStorage%2FAWS-Backup.svg
}

deploy -> backup: {
  icon: https://icons.d2lang.com/infra%2F002-backup.svg
}
```

Using the D2 CLI locally? You can specify local images like `icon: ./my_cat.png`.

Icon placement is automatic. Considerations vary depending on layout engine, but things
like coexistence with a label and whether it's a container generally affect where the icon
is placed to not obstruct. Notice how the following diagram has container icons in the
top-left and non-container icons in the center.

```d2
vpc: VPC 1 10.1.0.0./16 {
  icon: https://icons.d2lang.com/aws%2F_Group%20Icons%2FVirtual-private-cloud-VPC_light-bg.svg
  style: {
    stroke: green
    font-color: green
    fill: white
  }
  az: Availability Zone A {
    style: {
      stroke: blue
      font-color: blue
      stroke-dash: 3
      fill: white
    }
    firewall: Firewall Subnet A {
      icon: https://icons.d2lang.com/aws%2FNetworking%20&%20Content%20Delivery%2FAmazon-Route-53_Hosted-Zone_light-bg.svg
      style: {
        stroke: purple
        font-color: purple
        fill: "#e1d5e7"
      }
      ec2: EC2 Instance {
        icon: https://icons.d2lang.com/aws%2FCompute%2F_Instance%2FAmazon-EC2_C4-Instance_light-bg.svg
      }
    }
  }
}
```

Icons can be positioned with the `near` keyword [introduced later](/tour/positions/#label-and-icon-positioning).

#### Add `shape: image` for standalone icon shapes

```d2
direction: right
server: {
  shape: image
  icon: https://icons.d2lang.com/tech/022-server.svg
}

github: {
  shape: image
  icon: https://icons.d2lang.com/dev/github.svg
}

server -> github
```

### SQL Tables — `docs/tour/sql-tables.md`

#### Basics

You can easily diagram entity-relationship diagrams (ERDs) in D2 by using the `sql_table` shape. Here's a minimal example:

```d2
my_table: {
  shape: sql_table
  # This is defined using the shorthand syntax for labels discussed in the containers section.
  # But here it's for the type of a constraint.
  # The id field becomes a map that looks like {type: int; constraint: primary_key}
  id: int {constraint: primary_key}
  last_updated: timestamp with time zone
}
```

Each key of a SQL Table shape defines a row. The primary value (the thing after the colon)
of each row defines its type.

The constraint value of each row defines its SQL constraint. D2 will recognize and
shorten:

| constraint  | short |
| ----------- | ----- |
| primary_key | PK    |
| foreign_key | FK    |
| unique      | UNQ   |

But you can set any constraint you'd like. It just won't be shortened if unrecognized.

You can also specify multiple constraints with an array.

```d2
x: int { constraint: [primary_key; unique] }
```

If you'd like to use a reserved keyword, wrap it in quotes.

```d2
my_table: {
  shape: sql_table
  "label": string
}
```

#### Foreign Keys

Here's an example of how you'd define a foreign key connection between two tables:

```d2
objects: {
  shape: sql_table
  id: int {constraint: primary_key}
  disk: int {constraint: foreign_key}

  json: jsonb {constraint: unique}
  last_updated: timestamp with time zone
}

disks: {
  shape: sql_table
  id: int {constraint: primary_key}
}

objects.disk -> disks.id
```

When rendered with the [TALA layout engine](/tour/tala/) or [ELK layout engine](/tour/elk/),
connections point to the exact row.

#### Example

Like all other shapes, you can nest `sql_tables` into containers and define edges
to them from other shapes. Here's an example:

```d2
cloud: {
  disks: {
    shape: sql_table
    id: int {constraint: primary_key}
  }
  blocks: {
    shape: sql_table
    id: int {constraint: primary_key}
    disk: int {constraint: foreign_key}
    blob: blob
  }
  blocks.disk -> disks.id

  AWS S3 Vancouver -> disks
}
```

### UML Classes — `docs/tour/uml-classes.md`

#### Basics

D2 fully supports UML Class diagrams. Here's a minimal example:

```d2
MyClass: {
  shape: class

  field: "[]string"
  method(a uint64): (x, y int)
}
```

Each key of a `class` shape defines either a field or a method.

The value of a field key is its type.

Any key that contains `(` is a method, whose value is the return type.

A method key without a value has a return type of void.

If you'd like to use a reserved keyword, wrap it in quotes.

```d2
my_class: {
  shape: class
  "label": string
}
```

#### Visibilities

You can also use UML-style prefixes to indicate field/method visibility.

| visibility prefix | meaning   |
| ----------------- | --------- |
| none              | public    |
| +                 | public    |
| -                 | private   |
| #                 | protected |

See https://www.uml-diagrams.org/visibility.html

Here's an example with differing visibilities and more complex types:

```d2
D2 Parser: {
  shape: class

  # Default visibility is + so no need to specify.
  +reader: io.RuneReader
  readerPos: d2ast.Position

  # Private field.
  -lookahead: "[]rune"

  # Protected field.
  # We have to escape the # to prevent the line from being parsed as a comment.
  \#lookaheadPos: d2ast.Position

  +peek(): (r rune, eof bool)
  rewind()
  commit()

  \#peekn(n int): (s string, eof bool)
}

"github.com/terrastruct/d2parser.git" -> D2 Parser
```

#### Full example

```d2
DebitCard: Debit card {
  shape: class
  +cardno
  +ownedBy

  +access()
}

Bank: {
  shape: class
  +code
  +address

  +manages()
  +maintains()
}

ATMInfo: ATM info {
  shape: class
  +location
  +manageBy

  +identifies()
  +transactions()
}

Customer: {
  shape: class
  +name
  +address
  +dob

  +owns()
}

Account: {
  shape: class
  +type
  +owner
}

ATMTransaction: ATM Transaction {
  shape: class
  +transactionId
  +date
  +type

  +modifies()
}

CurrentAccount: Current account {
  shape: class
  +accountNo
  +balance

  +debit()
  +credit()
}

SavingAccount: Saving account {
  shape: class
  +accountNo
  +balance

  +debit()
  +credit()
}

WidthdrawlTransaction: Withdrawl transaction {
  shape: class
  +amount

  +Withdrawl()
}

QueryTransaction: Query transaction {
  shape: class
  +query
  +type

  +queryProcessing()
}

TransferTransaction: Transfer transaction {
  shape: class
  +account
  +accountNo
}

PinValidation: Pin validation transaction {
  shape: class
  +oldPin
  +newPin

  +pinChange()
}

DebitCard -- Bank: manages {
  source-arrowhead: 1..*
  target-arrowhead: 1
}

Bank -- ATMInfo: maintains {
  source-arrowhead: 1
  target-arrowhead: 1
}

Bank -- Customer: +has {
  source-arrowhead: 1
  target-arrowhead: 1
}

DebitCard -- Customer: +owns {
  source-arrowhead: 0..*
  target-arrowhead: 1..*
}

DebitCard -- Account: +provides access to {
  source-arrowhead: *
  target-arrowhead: 1..*
}

Customer -- Account: owns {
  source-arrowhead: 1..*
  target-arrowhead: 1..*
}

ATMInfo -- ATMTransaction: +identifies {
  source-arrowhead: 1
  target-arrowhead: *
}

ATMTransaction -> Account: modifies {
  source-arrowhead: *
  target-arrowhead: 1
}

CurrentAccount -> Account: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}

SavingAccount -> Account: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}

WidthdrawlTransaction -> ATMTransaction: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}
QueryTransaction -> ATMTransaction: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}
TransferTransaction -> ATMTransaction: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}
PinValidation -> ATMTransaction: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
}
```

### Sequence Diagrams — `docs/tour/sequence-diagrams.md`

Sequence diagrams are created by setting `shape: sequence_diagram` on an object.

```d2
shape: sequence_diagram
alice -> bob: What does it mean\nto be well-adjusted?
bob -> alice: The ability to play bridge or\ngolf as if they were games.
```

#### Rules

Unlike other tools, there is no special syntax to learn for sequence diagrams. The rules
are also almost exactly the same as everywhere else in D2, with two notable differences.

##### Scoping

Children of sequence diagrams share the same scope throughout the sequence diagram.

For example:

```d2
Office chatter: {
  shape: sequence_diagram
  alice: Alice
  bob: Bobby
  awkward small talk: {
    alice -> bob: uhm, hi
    bob -> alice: oh, hello
    icebreaker attempt: {
      alice -> bob: what did you have for lunch?
    }
    unfortunate outcome: {
      bob -> alice: that's personal
    }
  }
}
```

Outside of a sequence diagram, there would be multiple instances of `alice` and `bob`,
since they have different container scopes. But when nested under `shape:
sequence_diagram`, they refer to the same `alice` and `bob`.

##### Ordering

Elsewhere in D2, there is no notion of order. If you define a connection after another,
there is no guarantee is will visually appear after. However, in sequence diagrams, order
matters. The order in which you define everything is the order they will appear.

This includes actors. You don't have to explicitly define actors (except when they first
appear in a group), but if you want to define a specific order, you should.

```d2
shape: sequence_diagram
# Remember that semicolons allow multiple objects to be defined in one line
# Actors will appear from left-to-right as a, b, c, d...
a; b; c; d
# ... even if the connections are in a different order
c -> d
d -> a
b -> d
```

An actor in D2 is also known elsewhere as "participant".

#### Features

##### Sequence diagrams are D2 objects

Like every other object in D2, they can be contained, connected, relabeled, re-styled, and
treated like any other object.

```d2
direction: right
Before and after becoming friends: {
  2007: Office chatter in 2007 {
    shape: sequence_diagram
    alice: Alice
    bob: Bobby
    awkward small talk: {
      alice -> bob: uhm, hi
      bob -> alice: oh, hello
      icebreaker attempt: {
        alice -> bob: what did you have for lunch?
      }
      unfortunate outcome: {
        bob -> alice: that's personal
      }
    }
  }

  2012: Office chatter in 2012 {
    shape: sequence_diagram
    alice: Alice
    bob: Bobby
    alice -> bob: Want to play with ChatGPT?
    bob -> alice: Yes!
    bob -> alice.play: Write a play...
    alice.play -> bob.play: about 2 friends...
    bob.play -> alice.play: who find love...
    alice.play -> bob.play: in a sequence diagram
  }

  2007 -> 2012: Five\nyears\nlater
}
```

##### Spans

Spans convey a beginning and end to an interaction within a sequence diagram.

A span in D2 is also known elsewhere as a "lifespan", "activation box", and "activation bar".

You can specify a span by connecting a nested object on an actor.

```d2
shape: sequence_diagram
alice.t1 -> bob
alice.t2 -> bob.a
alice.t2.a -> bob.a
alice.t2.a <- bob.a
alice.t2 <- bob.a
```

##### Groups

Groups help you label a subset of the sequence diagram.

A group in D2 is also known elsewhere as a "fragment", "edge group", and "frame".

We saw an example of this in an earlier example when explaining scoping rules. More
formally, a group is a container within a `sequence_diagram` shape which is not connected
to anything but has connections or objects inside.

```d2
shape: sequence_diagram
# Predefine actors
alice
bob
shower thoughts: {
  alice -> bob: A physicist is an atom's way of knowing about atoms.
  alice -> bob: Today is the first day of the rest of your life.
}
life advice: {
  bob -> alice: If all else fails, lower your standards.
}
```

Due to the unique scoping rules in sequence diagrams, when you are within a group, the
objects you reference in connections must exist at the top-level. Notice in the above
example that `alice` and `bob` are explicitly declared before group declarations.

##### Notes

Notes are declared by defining a nested object on an actor with no connections going to
it.

```d2
shape: sequence_diagram
alice -> bob
bob."In the eyes of my dog, I'm a man."
# Notes can go into groups, too
important insight: {
  bob."Cold hands, no gloves."
}
bob -> alice: Chocolate chip.
```

##### Self-messages

Self-referential messages can be declared from an actor to the themselves.

```d2
shape: sequence_diagram
son -> father: Can I borrow your car?
friend -> father: Never lend your car to anyone to whom you have given birth.
father -> father: internal debate ensues
```

##### Customization

You can style shapes and connections like any other. Here we make some messages dashed and
set the shape on an actor.

```d2
shape: sequence_diagram
scorer: {shape: person}
scorer.t -> itemResponse.t: getItem()
scorer.t <- itemResponse.t: item {
  style.stroke-dash: 5
}

scorer.t -> item.t1: getRubric()
scorer.t <- item.t1: rubric {
  style.stroke-dash: 5
}

scorer.t -> essayRubric.t: applyTo(essayResp)
itemResponse -> essayRubric.t.c
essayRubric.t.c -> concept.t: match(essayResponse)
scorer <- essayRubric.t: score {
  style.stroke-dash: 5
}

scorer.t -> itemOutcome.t1: new
scorer.t -> item.t2: getNormalMinimum()
scorer.t -> item.t3: getNormalMaximum()

scorer.t -> itemOutcome.t2: setScore(score)
scorer.t -> itemOutcome.t3: setFeedback(missingConcepts)
```

Lifeline edges (those lines going from top-down) inherit the actor's `stroke` and
`stroke-dash` styles.

```d2
shape: sequence_diagram
alice -> bob: What does it mean\nto be well-adjusted?
bob -> alice: The ability to play bridge or\ngolf as if they were games.

alice.style: {
  stroke: red
  stroke-dash: 0
}
```

### Grid Diagrams — `docs/tour/grid-diagrams.md`

Grid diagrams let you display objects in a structured grid.

```d2
grid-rows: 5
style.fill: black

classes: {
  white square: {
    label: ""
    width: 120
    style: {
      fill: white
      stroke: cornflowerblue
      stroke-width: 10
    }
  }
  block: {
    style: {
      text-transform: uppercase
      font-color: white
      fill: darkcyan
      stroke: black
    }
  }
}

flow1.class: white square
flow2.class: white square
flow3.class: white square
flow4.class: white square
flow5.class: white square
flow6.class: white square
flow7.class: white square
flow8.class: white square
flow9.class: white square

dagger engine: {
  width: 800
  class: block
  style: {
    fill: beige
    stroke: darkcyan
    font-color: blue
    stroke-width: 8
  }
}

any docker compatible runtime: {
  width: 800
  class: block
  style: {
    fill: lightcyan
    stroke: darkcyan
    font-color: black
    stroke-width: 8
  }
  icon: https://icons.d2lang.com/dev%2Fdocker.svg
}

any ci: {
  class: block
  style: {
    fill: gold
    stroke: maroon
    font-color: maroon
    stroke-width: 8
  }
}
windows.class: block
linux.class: block
macos.class: block
kubernetes.class: block
```

Two keywords do all the magic:
- `grid-rows`
- `grid-columns`

Setting just `grid-rows`:

```d2
grid-rows: 3
Executive
Legislative
Judicial
```

Setting just `grid-columns`:

```d2
grid-columns: 3
Executive
Legislative
Judicial
```

Setting both `grid-rows` and `grid-columns`:

```d2
grid-rows: 2
grid-columns: 2
Executive
Legislative
Judicial
```

#### Width and height

To create specific constructions, use `width` and/or `height`.

```d2
grid-rows: 2
Executive
Legislative
Judicial
The American Government.width: 400
```

Notice how objects are evenly distributed within each row.

#### Cells expand to fill

When you define only one of row or column, objects will expand.

```d2
grid-rows: 3
Executive
Legislative
Judicial
The American Government.width: 400
Voters
Non-voters
```

Notice how `Voters` and `Non-voters` fill the space.

#### Dominant direction

When you apply both row and column, the first appearance is the dominant direction. The
dominant direction is the order in which cells are filled.

For example:

```d2-incomplete
grid-rows: 4
grid-columns: 2
# bunch of shapes
```

Since `grid-rows` is defined first, objects will fill rows before moving onto columns.

But if it were reversed:

```d2-incomplete
grid-columns: 2
grid-rows: 4
# bunch of shapes
```

It would do the opposite.

These animations are also pure D2, so you can animate grid diagrams being built-up. Use
the `animate-interval` flag with this
[code](https://github.com/d2lang/d2-docs/blob/f5c762223ce192338d9d7865df3ca8533d683cdc/static/bespoke-d2/grid-row-dominant.d2#L1).
More on this later, in the [composition](/tour/composition/) section.

#### Gap size

You can control the gap size of the grid with 3 keywords:
- `vertical-gap`
- `horizontal-gap`
- `grid-gap`

Setting `grid-gap` is equivalent to setting both `vertical-gap` and `horizontal-gap`.

`vertical-gap` and `horizontal-gap` can override `grid-gap`.

##### Gap size 0

`grid-gap: 0` in particular can create some interesting constructions:

###### Like this map of Japan

> [D2 source](https://github.com/d2lang/d2/blob/master/docs/examples/japan-grid/japan.d2)

###### Or a table of data

```d2
# Specified so that objects are written in row-dominant order
grid-rows: 2
grid-columns: 4
grid-gap: 0

classes: {
  header: {
    style.underline: true
  }
}

Element.class: header
Atomic Number.class: header
Atomic Mass.class: header
Melting Point.class: header

Hydrogen
1
"1.008"
"-259.16"

Carbon
6
"12.011"
3500

Oxygen
8
"15.999"
"-218.79"
```

You may find it easier to just use Markdown tables though, especially if there are
duplicate cells.

```d2
savings: ||md
  | Month    | Savings | Expenses | Balance |
  | -------- | ------- | -------- | ------- |
  | January  | $250    | $150     | $100    |
  | February | $80     | $200     | -$120   |
  | March    | $420    | $180     | $240    |
||
```

#### Connections

Connections for grids themselves work normally as you'd expect.

> Source code [here](https://github.com/d2lang/d2-docs/blob/eda2d8739ce21c656e7608be48cb9067df36eb53/static/d2/grid-connected.d2).

##### Connections between grid cells

Connections between shapes inside a grid work a bit differently. Because a grid structure
imposes positioning outside what the layout engine controls, the layout engine is also
unable to make routes. Therefore, these connections are center-center straight segments,
i.e., no path-finding.

> Source code [here](https://github.com/d2lang/d2/blob/master/e2etests/testdata/files/simple_grid_edges.d2).

> Source code [here](https://github.com/d2lang/d2/blob/master/docs/examples/vector-grid/vector-grid.d2).

#### Nesting

Currently you can nest grid diagrams within grid diagrams. Nesting other types is coming
soon.

```d2
grid-gap: 0
grid-columns: 1
header
body: "" {
  grid-gap: 0
  grid-columns: 2
  content
  sidebar
}
footer
```

#### Aligning with invisible elements

A common technique to align grid elements to your liking is to pad the grid with invisible
elements.

Consider the following diagram.

```d2
grid-columns: 1
us-east-1: {
  grid-rows: 1
  a
  b
  c
  d
  e
}

us-west-1: {
  grid-rows: 1
  a
}

us-east-1.c -> us-west-1.a
```

It'd be nicer if it were centered. This can be achieved by adding 2 invisible elements.

```d2
classes: {
  invisible: {
    style.opacity: 0
    label: a
  }
}

grid-columns: 1
us-east-1: {
  grid-rows: 1
  a
  b
  c
  d
  e
}

us-west-1: {
  grid-rows: 1
  pad1.class: invisible
  pad2.class: invisible
  a
  # Move the label so it doesn't go through the connection
  label.near: bottom-center
}

us-east-1.c -> us-west-1.a
```

#### Troubleshooting

##### Why is there extra padding in one cell?

Elements in a grid column have the same width and elements in a grid row have the same
height.

So in this example, a small empty space in "Backend Node" is present.

```d2
classes: {
  kuber: {
    style: {
      fill: "white"
      stroke: "#aeb5bd"
      border-radius: 4
      stroke-dash: 3
    }
  }
  sys: {
    label: ""
    style: {
      fill: "#AFBFDF"
      stroke: "#aeb5bd"
    }
  }
  node: {
    grid-gap: 0
    style: {
      fill: "#ebf3e6"
      border-radius: 8
      stroke: "#aeb5bd"
    }
  }
  clust: {
    style: {
      fill: "#A7CC9E"
      stroke: "#aeb5bd"
    }
  }
  deploy: {
    grid-gap: 0
    style: {
      fill: "#ffe6d5"
      stroke: "#aeb5bd"
      # border-radius: 4
    }
  }
  nextpod: {
    icon: https://www.svgrepo.com/show/378440/nextjs-fill.svg
    style: {
      fill: "#ECECEC"
      stroke: "#aeb5bd"
      # border-radius: 4
    }
  }
  flaskpod: {
    icon: https://www.svgrepo.com/show/508915/flask.svg
    style: {
      fill: "#ECECEC"
      stroke: "#aeb5bd"
      # border-radius: 4
    }
  }
}

classes

Kubernetes: {
  grid-columns: 2
  system: {
    grid-columns: 1
    Backend Node: {
      grid-columns: 2
      ClusterIP\nService 1
      Deployment 1: {
        grid-rows: 3
        NEXT POD 1
        NEXT POD 2
        NEXT POD 3
      }
    }
    Frontend Node: {
      grid-columns: 2
      ClusterIP\nService 2
      Deployment 2: {
        grid-rows: 3
        FLASK POD 1
        FLASK POD 2
        FLASK POD 3
      }
    }
  }
}

kubernetes.class: kuber
kubernetes.system.class: sys

kubernetes.system.backend node.class: node
kubernetes.system.backend node.clusterip\nservice 1.class: clust
kubernetes.system.backend node.deployment 1.class: deploy
kubernetes.system.backend node.deployment 1.next pod*.class: nextpod

kubernetes.system.frontend node.class: node
kubernetes.system.frontend node.clusterip\nservice 2.class: clust
kubernetes.system.frontend node.deployment 2.class: deploy
kubernetes.system.frontend node.deployment 2.flask pod*.class: flaskpod
```

It's due to the label of "Flask Pod" being slightly longer than "Next Pod". So the way we
fix that is to set `width`s to match.

```d2
classes: {
  kuber: {
    style: {
      fill: "white"
      stroke: "#aeb5bd"
      border-radius: 4
      stroke-dash: 3
    }
  }
  sys: {
    label: ""
    style: {
      fill: "#AFBFDF"
      stroke: "#aeb5bd"
    }
  }
  node: {
    grid-gap: 0
    style: {
      fill: "#ebf3e6"
      border-radius: 8
      stroke: "#aeb5bd"
    }
  }
  clust: {
    style: {
      fill: "#A7CC9E"
      stroke: "#aeb5bd"
    }
  }
  deploy: {
    grid-gap: 0
    style: {
      fill: "#ffe6d5"
      stroke: "#aeb5bd"
      # border-radius: 4
    }
  }
  nextpod: {
    width: 180
    icon: https://www.svgrepo.com/show/378440/nextjs-fill.svg
    style: {
      fill: "#ECECEC"
      stroke: "#aeb5bd"
      # border-radius: 4
    }
  }
  flaskpod: {
    width: 180
    icon: https://www.svgrepo.com/show/508915/flask.svg
    style: {
      fill: "#ECECEC"
      stroke: "#aeb5bd"
      # border-radius: 4
    }
  }
}

classes

Kubernetes: {
  grid-columns: 2
  system: {
    grid-columns: 1
    Backend Node: {
      grid-columns: 2
      ClusterIP\nService 1
      Deployment 1: {
        grid-rows: 3
        NEXT POD 1
        NEXT POD 2
        NEXT POD 3
      }
    }
    Frontend Node: {
      grid-columns: 2
      ClusterIP\nService 2
      Deployment 2: {
        grid-rows: 3
        FLASK POD 1
        FLASK POD 2
        FLASK POD 3
      }
    }
  }
}

kubernetes.class: kuber
kubernetes.system.class: sys

kubernetes.system.backend node.class: node
kubernetes.system.backend node.clusterip\nservice 1.class: clust
kubernetes.system.backend node.deployment 1.class: deploy
kubernetes.system.backend node.deployment 1.next pod*.class: nextpod

kubernetes.system.frontend node.class: node
kubernetes.system.frontend node.clusterip\nservice 2.class: clust
kubernetes.system.frontend node.deployment 2.class: deploy
kubernetes.system.frontend node.deployment 2.flask pod*.class: flaskpod
```

### Themes — `docs/tour/themes.md`

D2 comes with many themes that make your diagram look professional and ready to insert
into blogs and wikis.

### Rendered with theme "Vanilla nitro cola"

#### Setting theme on the CLI

To specify the theme used, you can set the flag `-t, --theme`.

```shell
d2 -t 101 input.d2
```

You can also use an environment variable.

```shell
D2_THEME=101 d2 input.d2
```

To see which themes are available, run

```shell
d2 themes
```

#### Dark theme

Dark themes are not set by default, so your diagram will look the same regardless of
whether the user's system preferences are light or dark.

All diagrams in these docs have a dark theme. Try toggling your system preference between
light and dark and see how it changes.

If you'd like your diagram to adapt and switch to a dark theme when the user's system
preference is dark, you can do so by specifying the following flag.

```shell
d2 --dark-theme 200 input.d2
```

Like regular themes, this can also be set with an environment variable.

```shell
D2_DARK_THEME=200 d2 input.d2
```

The themes are catalogued separately into light and dark, but there's nothing stopping you
from passing a dark theme ID to `theme` for your diagram to always be dark (or vice versa,
to give a surprise to dark mode users).

An example of a dark theme (this one's an image not an SVG, so it won't change according
to your system preference).

#### Special themes

Certain, special themes do more than just color.

For example, when you apply the `Terminal` theme, the following attributes are set as
default:
- Caps lock on all labels
- No border radius
- Monospaced font
- `fill-pattern` set to `dots` for all containers
- Most outer container has `double-border` set to `true`

Source code for the above diagram (rendered with ELK) is as follows. Notice that many of
the properties apparent in the diagram do not appear in the source, such as the casing of
the labels, because the special theme uses different defaults.

```d2
vars: {
  d2-config: {
    layout-engine: elk
    # Terminal theme code
    theme-id: 300
  }
}
network: {
  cell tower: {
    satellites: {
      shape: stored_data
      style.multiple: true
    }

    transmitter

    satellites -> transmitter: send
    satellites -> transmitter: send
    satellites -> transmitter: send
  }

  online portal: {
    ui: {shape: hexagon}
  }

  data processor: {
    storage: {
      shape: cylinder
      style.multiple: true
    }
  }

  cell tower.transmitter -> data processor.storage: phone logs
}

user: {
  shape: person
  width: 130
}

user -> network.cell tower: make call
user -> network.online portal.ui: access {
  style.stroke-dash: 3
}

api server -> network.online portal.ui: display
api server -> logs: persist
logs: {shape: page; style.multiple: true}

network.data processor -> api server
```

#### Customizing themes

You can override theme values to customize existing themes or replace them entirely with
your own theme.

This is controlled by two [configuration variables](/tour/vars/#configuration-variables):

- `theme-overrides`: replaces color codes for theme
- `dark-theme-overrides`: replaces color codes for dark theme

Adding this snippet to the above code results in the following diagram.

```d2-incomplete
vars: {
  d2-config: {
    theme-overrides: {
      B1: "#2E7D32"
      B2: "#66BB6A"
      B3: "#A5D6A7"
      B4: "#C5E1A5"
      B5: "#E6EE9C"
      B6: "#FFF59D"

      AA2: "#0D47A1"
      AA4: "#42A5F5"
      AA5: "#90CAF9"

      AB4: "#F44336"
      AB5: "#FFCDD2"
    }
  }
}
```

##### Color codes

Not all color codes are currently used right now, but that may change in the future for
new things that come to D2.

### Styles — `docs/tour/style.md`

If you'd like to customize the style of a shape, the following reserved keywords can be
set under the `style` field.

Below is a catalog of all valid styles, applied individually to this baseline diagram.

The following SVGs are rendered with `direction: right`, but omitted from the shown scripts for
brevity.

Want to change the default styles for shapes and/or connections? See [globs to change defaults](/tour/globs/#changing-defaults).

#### Style keywords

- [opacity](#opacity)
- [stroke](#stroke)
- [fill](#fill) (shape only)
- [fill-pattern](#fill-pattern) (shape only)
- [stroke-width](#stroke-width)
- [stroke-dash](#stroke-dash)
- [border-radius](#border-radius)
- [shadow](#shadow) (shape only)
- [3D](#3d) (rectangle/square only)
- [multiple](#multiple) (shape only)
- [double-border](#double-border) (rectangles and ovals)
- [font](#font)
- [font-size](#font-size)
- [font-color](#font-color)
- [animated](#animated)
- [bold, italic, underline](#bold-italic-underline)
- [text-transform](#text-transform)
- [root](#root)

#### Opacity

Float between `0` and `1`.

```d2
direction: right
x -> y: hi {
  style: {
    opacity: 0.4
  }
}
x.style.opacity: 0
y.style.opacity: 0.7
```

#### Stroke

CSS color name, hex code, or a subset of CSS gradient strings.

```d2
direction: right
x -> y: hi {
  style: {
    # All CSS color names are valid
    stroke: deepskyblue
  }
}
# We need quotes for hex otherwise it gets interpreted as comment
x.style.stroke: "#f4a261"
```

<br/>

For `sql_table`s and `class`es, `stroke` is applied as `fill` to the body (since `fill` is
already used to control header's `fill`).

#### Fill

CSS color name, hex code, or a subset of CSS gradient strings.

```d2
direction: right
x -> y: hi
y -> z
x.style.fill: "#f4a261"
y.style.fill: honeydew
z.style.fill: "linear-gradient(#f69d3c, #3f87a6)"
```

<br/>

For `sql_table`s and `class`es, `fill` is applied to the header.

Want transparent?

```d2
x: {
  y
  y.style.fill: transparent
}
x.style.fill: PapayaWhip
```

#### Fill Pattern

Available patterns:

- `dots`
- `lines`
- `grain`
- `none` (for cancelling out ones set by certain themes)

```d2
direction: right
style.fill-pattern: dots
x -> y: hi
x.style.fill-pattern: lines
y.style.fill-pattern: grain
```

#### Stroke Width

Integer between `1` and `15`.

```d2
direction: right
x -> y: hi {
  style: {
    stroke-width: 8
  }
}
x.style.stroke-width: 1
```

#### Stroke Dash

Integer between `0` and `10`.

```d2
direction: right
x -> y: hi {
  style: {
    stroke-dash: 3
  }
}
x.style.stroke-dash: 5
```

#### Border Radius

Integer between `0` and `20`.

```d2
direction: right
x -> y: hi
x.style.border-radius: 3
y.style.border-radius: 8
```

`border-radius` works on connections too, which controls how rounded the corners are. This
only applies to layout engines that use corners (e.g. ELK), and of course, only has effect
on connections whose routes have corners.

Specifying a very high value creates a "pill" effect.

```d2
tylenol.style.border-radius: 999
```

#### Shadow

`true` or `false`.

```d2
direction: right
x -> y: hi
x.style.shadow: true
```

#### 3D

`true` or `false`.

```d2
direction: right
x -> y: hi
x.style.3d: true
```

#### Multiple

`true` or `false`.

```d2
direction: right
x -> y: hi
x.style.multiple: true
```

#### Double Border

`true` or `false`.

```d2
direction: right
x -> y: hi
x.style.double-border: true
y.shape: circle
y.style.double-border: true
```

#### Font

Currently the only option is to specify `mono`. More coming soon.

```d2
direction: right
x -> y: hi {
  style: {
    font: mono
  }
}
x.style.font: mono
y.style.font: mono
```

#### Font Size

Integer between `8` and `100`.

```d2
direction: right
x -> y: hi {
  style: {
    font-size: 28
  }
}
x.style.font-size: 8
y.style.font-size: 55
```

#### Font Color

CSS color name, hex code, or a subset of CSS gradient strings.

```d2
direction: right
x -> y: hi {
  style: {
    font-color: red
  }
}
x.style.font-color: "#f4a261"
```

<br/>

For `sql_table`s and `class`es, `font-color` is applied to the header text only (theme
controls other colors in the body).

#### Animated

`true` or `false`.

```d2
direction: right
x -> y: hi {
  style.animated: true
}
x.style.animated: true
```

#### Bold, italic, underline

`true` or `false`.

```d2
direction: right
x -> y: hi {
  style: {
    bold: true
  }
}
x.style.underline: true
y.style.italic: true
# By default, shape labels are bold. Bold has precedence over italic, so unbold to see
# italic style
y.style.bold: false
```

#### Text transform

`text-transform` changes the casing of labels.

- `uppercase`
- `lowercase`
- `title`
- `none` (used for negating caps lock that special themes may apply)

```d2
direction: right
TOM -> jerry: hi {
  style: {
    text-transform: capitalize
  }
}
TOM.style.text-transform: lowercase
jerry.style.text-transform: uppercase
```

#### Root

Some styles are applicable at the root level. For example, to set a diagram background
color, use `style.fill`.

Currently the set of supported keywords are:

- `fill`: diagram background color
- `fill-pattern`: background fill pattern
- `stroke`: frame around the diagram
- `stroke-width`
- `stroke-dash`
- `double-border`: two frames, which is a popular framing method

```d2
direction: right
x -> y: hi
style: {
  fill: LightBlue
  stroke: FireBrick
  stroke-width: 2
}
```

All diagrams in this documentation are rendered with `pad=0`. If you're using `stroke` to
create a frame for your diagram, you'll likely want to add some padding.

### Classes — `docs/tour/classes.md`

Classes let you aggregate attributes and reuse them.

```d2
direction: right
classes: {
  load balancer: {
    label: load\nbalancer
    width: 100
    height: 200
    style: {
      stroke-width: 0
      fill: "#44C7B1"
      shadow: true
      border-radius: 5
    }
  }
  unhealthy: {
    style: {
      fill: "#FE7070"
      stroke: "#F69E03"
    }
  }
}

web traffic -> web lb
web lb.class: load balancer

web lb -> api1
web lb -> api2
web lb -> api3

api2.class: unhealthy

api1 -> cache lb
api3 -> cache lb

cache lb.class: load balancer
```

#### Connection classes

As a reminder of D2 syntax, you can apply classes to connections both at the initial
declaration as well as afterwards.

On initial declaration:

```d2
a -> b: {class: something}
```

Targeting:

```d2
a -> b
# ...
(a -> b)[0].class: something
```

#### Overriding classes

If your object defines an attribute that the class also has defined, the object's
attribute overrides the class attribute.

```d2
classes: {
  unhealthy: {
    style.fill: red
  }
}
x.class: unhealthy
x.style.fill: orange
```

#### Multiple classes

You may use arrays for the value as well to apply multiple classes.

```d2
classes: {
  d2: {
    label: ""
    icon: https://play.d2lang.com/assets/icons/d2-logo.svg
  }
  sphere: {
    shape: circle
    style.stroke-width: 0
  }
}

logo.class: [d2; sphere]
```

##### Order matters

When multiple classes are given, they are applied left-to-right.

```d2
classes: {
  uno: {
    label: 1
  }
  dos: {
    label: 2
  }
}

x.class: [uno; dos]
y.class: [dos; uno]
```

#### Advanced: Using classes as tags

If you want to post-process D2 diagrams, you can also use classes to arbitrarily tag
objects. Any `class` you apply is written into the SVG element as a `class` attribute. So
for example, you can then apply custom CSS like `.stuff { ... }` (or use Javascript for
  onclick handlers and such) on a web page that D2 SVG is embedded in.

### Dimensions — `docs/tour/dimensions.md`

You can specify the `width` and `height` of most shapes.

These keywords cannot be set on containers, since containers resize to fit their children.

```d2
direction: right

small jerry: "" {
  shape: image
  icon: https://static.wikia.nocookie.net/tomandjerry/images/4/46/JerryJumbo3-1-.jpg
  width: 200
  height: 200
}

med jerry: "" {
  shape: image
  icon: https://static.wikia.nocookie.net/tomandjerry/images/4/46/JerryJumbo3-1-.jpg
  width: 300
  height: 300
}

big jerry: "" {
  shape: image
  icon: https://static.wikia.nocookie.net/tomandjerry/images/4/46/JerryJumbo3-1-.jpg
  width: 500
  height: 400
}

big jerry -> med jerry -> small jerry
```

### Positions — `docs/tour/positions.md`

In general, positioning is controlled entirely by the layout engine. It's one of the
primary benefits of text-to-diagram that you don't have to manually define all the
positions of objects.

However, there are occasions where you want to have some control over positions.
Currently, there are two ways to do that.

#### Near

D2 allows you to position items on set points around your diagram.

`top-left`, `top-center`, `top-right`,

`center-left`, `center-right`,

`bottom-left`, `bottom-center`, `bottom-right`

Let's explore some use cases:

##### Giving your diagram a title

```d2
title: |md
  # A winning strategy
| {near: top-center}

poll the people -> results
results -> unfavorable -> poll the people
results -> favorable -> will of the people
```

##### Creating a legend

```d2
direction: right

x -> y: {
  style.stroke: green
}

y -> z: {
  style.stroke: red
}

legend: {
  near: bottom-center
  color1: foo {
    shape: text
    style.font-color: green
  }

  color2: bar {
    shape: text
    style.font-color: red
  }
}
```

##### Longform description or explanation

```d2
explanation: |md
  # LLMs
  The Large Language Model (LLM) is a powerful AI\
    system that learns from vast amounts of text data.\
  By analyzing patterns and structures in language,\
  it gains an understanding of grammar, facts,\
  and even some reasoning abilities. As users input text,\
  the LLM predicts the most likely next words or phrases\
  to create coherent responses. The model\
  continuously fine-tunes its output, considering both the\
  user's input and its own vast knowledge base.\
  This cutting-edge technology enables LLM to generate human-like text,\
  making it a valuable tool for various applications.
| {
  near: center-left
}

ML Platform -> Pre-trained models
ML Platform -> Model registry
ML Platform -> Compiler
ML Platform -> Validation
ML Platform -> Auditing

Model registry -> Server.Batch Predictor
Server.Online Model Server
```

#### Label and icon positioning

The `near` can be nested to `label` and `icon` to specify their positions.

```d2
direction: right
x -> y

x: worker {
  label.near: top-center
  icon: https://icons.d2lang.com/essentials%2F005-programmer.svg
  icon.near: outside-top-right
}

y: profits {
  label.near: bottom-right
  icon: https://icons.d2lang.com/essentials%2Fprofits.svg
  icon.near: outside-top-left
}
```

##### Outside and border

When positioning labels and icons, in addition to the values that `near` can take
elsewhere, an `outside-` prefix can be added to specify positioning outside the bounding
box of the shape.

`outside-top-left`, `outside-top-center`, `outside-top-right`,

`outside-left-center`, `outside-right-center`,

`outside-bottom-left`, `outside-bottom-center`, `outside-bottom-right`

Note that `outside-left-center` is a different order than `center-left`.

You can also add `border-x` prefix to specify the label being on the border.

```d2
style.fill: "#222a25"
env: Your environment {
  # --- Outside label ---
  label.near: outside-bottom-center
  style.fill: "#222a25"
  style.stroke-dash: 2
  style.double-border: false
  style.stroke: "#1e402d"
  style.font-color: "#3ddb89"
  app: Your applicaton {
    # --- Border label ---
    label.near: border-top-center
    style.stroke: "#3d9069"
    style.fill: "#222a25"
    style.font-color: "#63c08c"

    *.style.stroke: "#adf1c6"
    *.style.fill: "#306a4a"
    *.style.font-color: "#eef9f3"
    Workflow
    SDK
    Workers
    Workflow -> SDK: hello {
      style.stroke: "#fbfdfd"
      style.font-color: "#adf1c6"
    }
  }
}
```

#### Tooltip near

Usually, `tooltip` is a on-hover effect. However, if you specify a `near` field, it will
permanently show.

```d2
ci-runner
codedeploy: {
  tooltip: |md
    God has abandoned this pipeline
  |
  tooltip.near: center-left
}
aws instance

ci-runner -> codedeploy -> aws instance: safe deploy
ci-runner -> aws instance: direct deploy
```

#### Near objects

Works in TALA only. We are working on shims to make this possible in other layout engines.

You can also set `near` to the absolute ID of another shape to hint to the layout engine
that they should be in the vicinity of one another.

```d2
vars: {
  d2-config: {
    layout-engine: tala
  }
}
aws: {
  load_balancer -> api
  api -> db
}
gcloud: {
  auth -> db
}

gcloud -> aws

explanation: |md
  # Why do we use AWS?
  - It has more uptime than GCloud
  - We have free credits
| {
  near: aws
}
```

Notice how the text is positioned near the `aws` node and not the `gcloud` node.

#### Top and left

On the TALA engine, you can also directly set the `top` and `left` values for objects, and
the layout engine will only move other objects around it.

For more on this, see page 17 of the [TALA user
manual](https://github.com/terrastruct/TALA/blob/master/TALA_User_Manual.pdf).

### Sketch (Hand-drawn) — `docs/tour/sketch.md`

D2 can render diagrams to give the aesthetic of a hand-drawn sketch.

- If you're using the CLI, enable this with the `--sketch` flag.
- [https://play.d2lang.com](https://play.d2lang.com/?script=qlDQtVOo5AIEAAD__w%3D%3D&sketch=1)
  supports this as well.

See our [blog post](/blog/hand-drawn-diagrams) on sketch mode

### Interactive — `docs/tour/interactive.md`

#### Tooltips

Tooltips are text that appear on hover. They serve two purposes:
1. Add secondary context.
    - You want to add a description to an object. It's not so important that everyone
      needs it, but those who want extra information can access it.
2. Tidy.
    - Your diagram is getting messy. Instead of adding more text, you can tuck some into
      tooltips.

```d2
x: {tooltip: Total abstinence is easier than perfect moderation}
y: {tooltip: Gee, I feel kind of LIGHT in the head now,\nknowing I can't make my satellite dish PAYMENTS!}
x -> y
```

Try it out, hover over `x` and `y`. Notice that they have an icon indicating that they
have a tooltip.

When you export to a static format like PNG, D2 will
1. Change all the icons to be numbered.
2. Add an appendix, where each line corresponds to the number.

Tooltips are implemented with HTML
[title](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/title) tags,
which have basic support for text formatting. Markdown won't be rendered as expected in
tooltips.

#### Links

Links are like tooltips, except you click to go to an external link.

When the link contains the `#` character as part of a URI fragment, e.g.,
`https://example.com/page#fragment`, remember that the fragment will be
treated as a comment if unquoted and unescaped.

```d2
x: I'm a Mac {
  link: https://apple.com
}
y: And I'm a PC {
  link: https://microsoft.com
}
x -> y: gazoontite {
  link: https://google.com
}
```

Try clicking on each.

### Fonts — `docs/tour/fonts.md`

D2 uses 4 font families:

- [Source Sans Pro](https://fonts.google.com/specimen/Source+Sans+Pro) for the majority of
  text, including labels, Markdown, etc.
- [Source Code Pro](https://fonts.google.com/specimen/Source+Code+Pro) for code blocks and
  text in Class shape.
- A blend of [Architect's Daughter](https://fonts.google.com/specimen/Architects+Daughter)
  and [Fuzzy Bubbles](https://fonts.google.com/specimen/Fuzzy+Bubbles) for `sketch` mode
  text.

Currently on the CLI, you can customize fonts by replacing Source Sans Pro with your own
TTF files through the following flags:

- `--font-regular`
- `--font-italic`
- `--font-bold`
- `--font-semibold`

These should point to a `.ttf` file, for example:

```shell
d2 --font-regular=./helvetica-regular.ttf input.d2
```

It's advisable to supply either none or all of the fonts, for consistency. If you supply
one but not all of the fonts, it will fall back to Source Sans Pro for the missing styles.
For example, if you give a `--font-regular`, `--font-bold`, and `--font-semibold`, then the
italic will remain as Source Sans Pro Italic.

#### Mono fonts

If you'd like to customize the mono fonts:

- `--font-regular`
- `--font-italic`
- `--font-bold`
- `--font-semibold`

#### Sketch font

In sketch mode, if you supply a font, it will replace the default hand-drawn font family
instead of Source Sans Pro.

### Overview — `docs/tour/layouts.md`

D2 supports using a variety of different layout engines. The choice of layout engines can
significantly influence your overall diagram. Each layout also has varying degrees of
support for certain keywords. Though we try our best to keep things consistent, ultimately
we have the most control over our custom-built layout engine and are limited by what the
other layout engines support.

#### Layout engines

- [dagre](/tour/dagre/) (default): A fast, directed graph layout engine that produces
  layered/hierarchical layouts. Based on Graphviz's DOT algorithm.
- [ELK](/tour/elk/): Also a directed graph layout engine. More mature than dagre, better
  maintained (part-time academic research team working on it), with recent releases.
- [TALA](/tour/tala/): New layout engine designed specifically for software architecture
  diagrams.

You can choose whichever layout engine you like and works best for the diagram you're
making. Each one has its tradeoffs, visit the individual pages to learn more.

To see available layouts on your machine, you can run `d2 layout`. Each layout engine can
also have specific configurable flags, which you can find by running `d2 layout [engine]`,
e.g. `d2 layout dagre`.

To specify the layout used, you can either set the flag `--layout=dagre` or set it as an
environment variable, `$D2_LAYOUT=dagre`.

##### Layout-specific functionality

Some keywords and functionality are only available for certain layout engines. We authored
and maintain TALA, so it is the only one we have full control over. We write shims for
Dagre and ELK, but some things are fundamental to the layout engines, and the only way to
support everything we want to do on those is to fork (which we may eventually do).

These are mentioned in other parts of the doc and aggregated here:

- `near` set to another object. `near` can be set to constants for all layout engines, but
  only TALA can use it to set to objects.
- `width` and `height` on containers. TALA will add this soon, but currently it is only in
  ELK. Note that these keywords work on non-containers in all layout engines.
- `top` and `left` to lock positions only work in TALA.
- Connections from ancestors to descendants (e.g. a container to its child) do not work in
  Dagre.

#### Direction

Set `direction` to one of the following to influence an explicit direction your diagram
flows towards.

- `up`
- `down`
- `right`
- `left`

```d2
direction: right
x -> y -> z: hello
```

```d2
direction: up
x -> y -> z: hello
```

##### Directions per container (TALA only)

Directions can only be set at a global level for all the layout engines except TALA. This
is a limitation of their algorithms, which are hierarchical and only work in one
direction. We are investigating ways to hack it to work.

```d2
vars: {
  d2-config: {
    layout-engine: tala
  }
}
direction: down
a -> b -> c

b: {
  direction: right
  1 -> 2 -> 3
}

a: {
  direction: left
  foo -> bar
}
```

### Dagre — `docs/tour/dagre.md`

**[🔗 Gallery](/examples/dagre)**

Dagre is D2's default layout engine.

#### Reference

[https://github.com/dagrejs/dagre](https://github.com/dagrejs/dagre)

#### Pros

- Very fast.
- Battle tested (thanks to MermaidJS, which exclusively uses Dagre for its flowcharts).
- Generally good results.
- Theory behind algorithms are the papers that power Graphviz.
- Renders hierarchical layouts well.

#### Cons

- Unmaintained. Development stopped in 2018.
- Makes some inexplicable edge routing decisions occasionally
  ([https://github.com/dagrejs/dagre/issues/256](https://github.com/dagrejs/dagre/issues/256)).
- Layout algorithm is strictly hierarchical, even if underlying diagram is not
  hierarchical.
- Container child to another container (or another container child) is not natively
  supported by dagre. D2 has added a shim to make it work, but there's some core algorithm
  considerations that are missed due to the shim.
- Multi-segment edge routes are curved, instead of orthogonal. Can result in unaesthetic
  squiggly lines.

### ELK — `docs/tour/elk.md`

**[🔗 Gallery](/examples/elk)**

ELK is a mature, hierarchical layout, actively maintained by an academic research group at
[Christian Albrechts University in
Kiel](https://www.rtsys.informatik.uni-kiel.de/en/team).

#### Reference

[https://www.eclipse.org/elk/reference.html](https://www.eclipse.org/elk/reference.html)

#### Pros

- Clean, orthogonal routes.
- Highly customizable.
- Fast.
- Good at minimizing crossings.
- Natively supports container to container routing, handling these better than dagre.
- Undergoing active improvements with regular releases.
- Routes SQL tables with exact columns.

#### Cons

- Strictly hierarchical, like dagre.
- Some routes have unnecessary bends.
- Minimal consideration for symmetry.

### TALA — `docs/tour/tala.md`

**[🔗 Gallery](/examples/tala)**

Proprietary layout engine developed by Terrastruct, designed specifically for software
architecture diagrams.

TALA is a separate install from D2, to keep a clean cut between 100% free and
open-source D2, and proprietary, closed-source TALA. You can download it here:
[https://github.com/terrastruct/tala](https://github.com/terrastruct/tala#installation).

#### Reference

[https://terrastruct.com/tala/](https://terrastruct.com/tala/)

For the most up-to-date information, please see the [official TALA
manual](https://github.com/terrastruct/TALA/blob/master/TALA_User_Manual.pdf).

#### Pros

- As a general orthogonal layout engine, TALA is not constrained to one type like
  hierarchies or trees or radial. For fundamentally non-hierarchical layouts, TALA can
  produce diagrams like a human would on a whiteboard.
- `top` and `left` can be used to lock positions.
- Considers and prefers symmetry.
- First-class consideration for containers.
- `direction` can be set per-container.
- `near` can be specified to be to another shape.
- `sql_table` connections point to exact row.
- Dynamic label positioning to avoid obstructions.
- Connections for grid cells use TALA's routing engine instead of always straight lines.

#### Cons

- Not free.
- Relatively new. ~2 years in production compared to the 10+ years that alternative layout
  engines have.
- More random than other layout engines. A small change to a label can cascade into an
  entirely different layout.

### Strings — `docs/tour/strings.md`

#### Unquoted strings

You may have noticed by now that the examples thus far have not used any quotes. It's our
goal for D2 to be easy to use and quotes tend to get in the way of that.

Quotes add friction in several ways. First, you have to close opened quotes. Second, you
have to remember whether to use single or double quotes. Lastly, they add syntactical
noise.

That means for the most part, don't worry about quotes!

Leading and trailing whitespace is trimmed.

```d2
   Office Bulb   :     Philips
            Switch   ->   Office Bulb
```

Unquoted strings may not contain certain characters that are used elsewhere in the
language. The syntax highlighting will make it clear if you're using a forbidden symbol.

#### Quoted strings

If you need to use such symbols, you can use single or double quoted strings:

```d2
'$$$' -> "###"
```

You would use double quotes if your text contains single quotes, and vice-versa. If it includes both, use double quotes and simply `\` escape as you would in other languages.

#### Autoformat

If your block string's indent is not sufficient, the autoformatter will correct it.

```d2
parent: {
example_code: |go
  package fs

  type FS interface {
    Open(name string) (File, error)
  }

  type File interface {
    Stat() (FileInfo, error)
    Read([]byte) (int, error)
    Close() error
  }

  var (
    ErrInvalid    = errInvalid()    // "invalid argument"
    ErrPermission = errPermission() // "permission denied"
    ErrExist      = errExist()      // "file already exists"
    ErrNotExist   = errNotExist()   // "file does not exist"
    ErrClosed     = errClosed()     // "file already closed"
  )
|
}
```

Will become:

```d2
parent: {
  example_code: |go
    package fs

    type FS interface {
      Open(name string) (File, error)
    }

    type File interface {
      Stat() (FileInfo, error)
      Read([]byte) (int, error)
      Close() error
    }

    var (
      ErrInvalid    = errInvalid()    // "invalid argument"
      ErrPermission = errPermission() // "permission denied"
      ErrExist      = errExist()      // "file already exists"
      ErrNotExist   = errNotExist()   // "file does not exist"
      ErrClosed     = errClosed()     // "file already closed"
    )
  |
}
```

Autoformat will check if there are any non empty lines with insufficient indent. If so, all
lines will be prepended with the correct amount of indent (while respecting existing
common indent). This way you don't have to fuss with your editor to get the indent right.
Just paste any code on the first column after starting a block string and autoformat will
correct it for you.

You can use tabs to indent block strings after indenting to the base block string indent
with two spaces. Any tabs in the base block string indent will be automatically converted
to two spaces.

### Variables & Substitutions — `docs/tour/vars.md`

`vars` is a special keyword that lets you define variables. These variables can be
referenced with the substitution syntax: `${}`.

```d2
direction: right
vars: {
  server-name: Cat
}

server1: ${server-name}-1
server2: ${server-name}-2

server1 <-> server2
```

#### Variables can be nested

Use `.` to refer to nested variables.

```d2
vars: {
  primaryColors: {
    button: {
      active: "#4baae5"
      border: black
    }
  }
}

button: {
  width: 100
  height: 40
  style: {
    border-radius: 5
    fill: ${primaryColors.button.active}
    stroke: ${primaryColors.button.border}
  }
}
```

#### Variables are scoped

They work just like variable scopes in programming. Substitutions can refer to variables
defined in a more outer scope, but not a more inner scope. If a variable appears in two
scopes, the one closer to the substitution is used.

```d2
vars: {
  region: Global
}

lb: ${region} load balancer

zone1: {
  vars: {
    region: us-east-1
  }
  server: ${region} API
}
```

#### Single quotes bypass substitutions

```d2
direction: right
vars: {
  names: John and Joyce
}
a -> b: 'Send field ${names}'
```

#### Spread substitutions

If `x` is a map or an array, `...${x}` will spread the contents of `x` into either a map
or an array.

```d2
vars: {
  base-constraints: [NOT NULL; UNQ]
  disclaimer: DISCLAIMER {
    I am not a lawyer
    near: top-center
  }
}

data: {
  shape: sql_table
  a: int {constraint: [PK; ...${base-constraints}]}
}

custom-disclaimer: DRAFT DISCLAIMER {
  ...${disclaimer}
}
```

#### Configuration variables

Some configurations can be made directly in `vars` instead of using flags or environment
variables.

```d2
vars: {
  d2-config: {
    theme-id: 4
    dark-theme-id: 200
    pad: 0
    center: true
    sketch: true
    layout-engine: elk
  }
}

direction: right
x -> y
```

This is equivalent to calling the following with no `vars`:
```shell
d2 --layout=elk --theme=4 --dark-theme=200 --pad=0 --sketch --center input.d2
```

Flags and environment variables take precedence.

In other words, if you call `D2_PAD=2 d2 --theme=1 input.d2`, it doesn't matter what
`theme-id` and `pad` are set to in `input.d2`'s `d2-config`; it will use the options from
the command.

`data` is an anything-goes map of key-value pairs. This is used in contexts where
third-party software read configuration, such as when D2 is used as a library, or D2 is
run with an external plugin.

For example,

```d2
vars: {
  d2-config: {
    data: {
      power-level: 9000
    }
  }
}
```

### Globs — `docs/tour/globs.md`

> The glob command, short for global, originates in the earliest versions of Bell Labs' Unix... to expand wildcard characters in unquoted arguments ...

[https://en.wikipedia.org/wiki/Glob_(programming)](https://en.wikipedia.org/wiki/Glob_(programming))

Globs are a powerful language feature to make global changes in one line.

```d2
iphone 10
iphone 11 mini
iphone 11 pro
iphone 12 mini

*.height: 300
*.width: 140
*mini.height: 200
*pro.height: 400
```

#### Globs apply backwards and forwards

In the following example, the instructions are as follows:
1. Create a shape `a`.
2. Apply a glob rule. This immediately applies to existing shapes, i.e., `a`.
3. Create a shape `b`. Existing glob rules are re-evaluated, and applied if they meet the
   criteria. This does, so it applies to `b`.
4. Same with `c`.

```d2
a

* -> y

b
c
```

#### Globs are case insensitive

```d2
diddy kong
Donkey Kong

*kong.style.fill: brown
```

#### Globs can appear multiple times

```d2
teacher
thriller
thrifter

t*h*r.shape: person
```

#### Glob connections

You can use globs to create connections.

```d2
vars: {
  d2-config: {
    layout-engine: elk
  }
}

Spiderman 1
Spiderman 2
Spiderman 3

* -> *: 👉
```

Notice how self-connections were omitted. While not entirely consistent with what you may
expect from globs, we feel it is more pragmatic for this to be the behavior.

You can also use globs to target modifying existing connections.

```d2
lady 1
lady 2

barbie

lady 1 -> barbie: hi barbie
lady 2 -> barbie: hi barbie

(lady* -> barbie)[*].style.stroke: pink
```

#### Scoped globs

Notice that in the below example, globs only apply to the scope they are specified in.

```d2
foods: {
  pizzas: {
    cheese
    sausage
    pineapple
    *.shape: circle
  }
  humans: {
    john
    james
    *.shape: person
  }
  humans.* -> pizzas.pineapple: eats
}
```

#### Recursive globs

`**` means target recursively.

```d2
a: {
  b: {
    c
  }
}

**.style.border-radius: 7
```

```d2
zone-A: {
  machine A
  machine B: {
    submachine A
    submachine B
  }
}

zone-A.** -> load balancer
```

Notice how `machine B` was not captured. Similar to the exception with `* -> *` omitting
self-connections, recursive globs in connections also make an exception for practical
diagramming: it only applies to non-container (AKA leaf) shapes.

#### Filters

Use `&` to filter what globs target. You may use any reserved keyword to filter on.

```d2
bravo team.shape: person
charlie team.shape: person
command center.shape: cloud
hq.shape: rectangle

*: {
  &shape: person
  style.multiple: true
}
```

##### Property filters

Aside from reserved keywords, there are special property filters for more specific
targeting.

- `connected: true|false`
- `leaf: true|false`

```d2
**: {
  &connected: true
  style.fill: yellow
}

**: {
  &leaf: true
  style.stroke: red
}

container: {
  a -> b
}
c
```

##### Filters on array values

If the filtered attribute has an array value, the filter will match if it matches any
element of the array.

```d2
the-little-cannon: {
  class: [server; deployed]
}
dino: {
  class: [internal; deployed]
}
catapult: {
  class: [server]
}

*: {
  &class: server
  style.multiple: true
}
```

##### Globs as filter values

Globs can also appear in the value of a filter. `*` by itself as a value for a filter
means the key must be specified.

```d2
*: {
  &link: *
  style.fill: red
}

x.link: https://google.com
y
```

##### AND filter

Adding multiple lines of filters counts as an AND.

```d2
*: {
  &shape: person
  &connected: true
  style.fill: red
}
(** -> **)[*]: {
  &src: a
  &dst: c
  style.stroke: yellow
}
a -> b
a.shape: person
a -> c
```

##### Connection endpoint filters

Connections can be filtered by properties on their source and destination shapes.

```d2
a: {
  shape: circle
  style: {
    fill: blue
    opacity: 0.8
  }
}
b: {
  shape: rectangle
  style: {
    fill: red
    opacity: 0.5
  }
}
c: {
  shape: diamond
  style.fill: green
  style.opacity: 0.8
}
(* -> *)[*]: {
  &src.style.fill: blue
  style.stroke-dash: 3
}
(* -> *)[*]: {
  &dst.style.opacity: 0.8
  style.stroke: cyan
}
(* -> *)[*]: {
  &src.shape: rectangle
  &dst.style.fill: green
  style.stroke-width: 5
}
a -> b
b -> c
a -> c
```

Endpoint filters also work with IDs, e.g. `&src: b`.

Endpoint IDs are absolute. For example, `a.c` instead of just `c`, even if the glob is
declared within `a`.

#### Inverse filters

Use `!&` to inverse-filter what globs target.

```d2
bravo team.shape: person
charlie team.shape: person
command center.shape: cloud
hq.shape: rectangle

*: {
  !&shape: person
  style.multiple: true
}
```

#### Nested globs

You can nest globs, combining the features above.

```d2
conversation 1: {
  shape: sequence_diagram
  alice -> bob: hi
  bob -> alice: hi
}

conversation 2: {
  shape: sequence_diagram
  alice -> bob: hello again
  alice -> bob: hello?
  bob -> alice: hello
}

# Recursively target all shapes...
**: {
  # ... that are sequence diagrams
  &shape: sequence_diagram
  # Then recursively set all shapes in them to person
  **: {shape: person}
}
```

#### Global globs

Triple globs apply globally to the whole diagram. The difference between a double glob and
a triple glob is that a triple glob will apply to nested `layers` (see the section on
[composition](/tour/composition/) for more on `layers`), as well as persist across imports.

```d2
***.style.fill: yellow
**.shape: circle
*.style.multiple: true

x: {
  y
}

layers: {
  next: {
    a
  }
}
```

If you import a file, the globs declared inside it are usually not carried over. Triple
globs are the exception -- since they are global, importing a file with triple glob will
carry that glob as well.

#### Changing defaults

One common use case of globs is to change the default styling of a theme.

```d2
# Add to the top of your diagram
***.style.fill: lightblue
(*** -> ***)[*]: {
  style.stroke: red
}

x -> y
```

### Comments — `docs/tour/comments.md`

D2 has line comments and block comments.

#### Line comments

Line comments begin with a hash.

They can be added as their own line

```d2
# Comments start with a hash character and continue until the next newline or EOF.
x -> y
```

Or at the end of a line

```d2
x -> y # I am at the end
```

#### Block comments

Block comments begin and end with three double quotes:

```d2
x -> y

"""
This is a
block comment
"""

y -> z
```

### Overrides — `docs/tour/overrides.md`

If you redeclare a shape, the new declaration is merged with the previous declaration.

```d2
visual studio code text editor
visual studio code text editor: visual_studio_code_text_editor
# Remember that shape keys are case insensitive
visual studio CODE text editor: VisualStudioCodeTextEditor
visual studio code TEXT editor: Visual Studio Code Text Editor
visual STUDIO code text editor
```

The latest explicit setting of the label takes priority.

Here's a more complex example of overrides involving containers:

```d2
aws_s3: AWS S3 California {
  Monitoring -> California
}
aws_s3: "AWS S3 San Francisco, California" {
  California.San Francisco
}

# Equal to:
# aws_s3: "AWS S3 San Francisco, California" {
#   Monitoring -> California
#   California.San Francisco
# }
```

#### Null

You may override with the value `null` to delete the shape/connection/attribute.

```d2
one
two

one: null
```

When is this useful?
- [Import](/tour/imports/) a diagram from a colleague and remove the things you don't want.
- [Multi-board compositions](/tour/composition/) where you inherit all the objects from a
  board with some exceptions.
- Use [globs](/tour/globs/) to define connections between a batch of objects except one in
  particular you want to leave out.

##### Nulling a connection

```d2
one -> two

(one -> two)[0]: null
```

##### Nulling an attribute

```d2
one: {
  style: {
    fill: pink
    stroke: green
  }
}

one.style.stroke: null
```

##### Implicit nulls

If you null a shape with connections, its connections are also nulled (since every
connection in D2 needs an endpoint).

```d2
one -> two

two: null
```

If you null a shape with descendents, those descendants are also nulled.

```d2
one: {
  two: {
    three
  }
}

one.two: null
```

### Models — `docs/tour/models.md`

Let's say you want to define all models and relationships between models once, then
display them in different ways.

First, let's define the models and relationships.

```d2
# -----
# Models
# -----
restaurants: Restaurants {
  style.stroke-dash: 2
  *.style.fill: "#66c4e3"
  chip: Chipotle
  cfa: Chick-Fil-A
  bk: Burger King

  chip -> bk: competes with
}

diners: Diners {
  daniel
  zack
}

# -----
# Model Relationships
# -----
diners -> restaurants: eat at

diners.daniel -> restaurants.chip: likes
diners.daniel -> restaurants.cfa: dislikes

diners.zack -> restaurants.bk: likes
diners.zack -> restaurants.chip: likes
```

We will use this as the example for multiple views of the same model. How do we treat
these as models and not just ordinary shapes and connections? We use the following
keywords:

1. `suspend`: This marks the shape or connection for deletion
2. `unsuspend`: This restores the shape or connection

Since models are meant to be invisible until used, we define models at the top of our
diagram and `suspend` all of them with the following globs.

```d2
**: suspend
(** -> **)[*]: suspend
```

We then use globs to selectively `unsuspend` the models we want to show. Let's take a look
at some use cases.

If you haven't yet, please familiarize yourself with [globs](globs.md).

#### Show only top-level

```d2
# -----
# Models
# -----
restaurants: Restaurants {
  style.stroke-dash: 2
  *.style.fill: "#66c4e3"
  chip: Chipotle
  cfa: Chick-Fil-A
  bk: Burger King

  chip -> bk: competes with
}

diners: Diners {
  daniel
  zack
}

# -----
# Model Relationships
# -----
diners -> restaurants: eat at

diners.daniel -> restaurants.chip: likes
diners.daniel -> restaurants.cfa: dislikes

diners.zack -> restaurants.bk: likes
diners.zack -> restaurants.chip: likes

# Treat the above as models
**: suspend
(** -> **)[*]: suspend

# Display only top level
*: unsuspend
(* -> *)[*]: unsuspend
```

#### Show only connection to X

```d2
# -----
# Models
# -----
restaurants: Restaurants {
  style.stroke-dash: 2
  *.style.fill: "#66c4e3"
  chip: Chipotle
  cfa: Chick-Fil-A
  bk: Burger King

  chip -> bk: competes with
}

diners: Diners {
  daniel
  zack
}

# -----
# Model Relationships
# -----
diners -> restaurants: eat at

diners.daniel -> restaurants.chip: likes
diners.daniel -> restaurants.cfa: dislikes

diners.zack -> restaurants.bk: likes
diners.zack -> restaurants.chip: likes

# Treat the above as models
**: suspend
(** -> **)[*]: suspend

# Display only models connected to bk and their relationships
(** -> **)[*]: unsuspend {
  &dst: restaurants.bk
}
```

#### Show only likes

```d2
# -----
# Models
# -----
restaurants: Restaurants {
  style.stroke-dash: 2
  *.style.fill: "#66c4e3"
  chip: Chipotle
  cfa: Chick-Fil-A
  bk: Burger King

  chip -> bk: competes with
}

diners: Diners {
  daniel
  zack
}

# -----
# Model Relationships
# -----
diners -> restaurants: eat at

diners.daniel -> restaurants.chip: likes
diners.daniel -> restaurants.cfa: dislikes

diners.zack -> restaurants.bk: likes
diners.zack -> restaurants.chip: likes

# Treat the above as models
**: suspend
(** -> **)[*]: suspend

# Display only who likes what
(** -> **)[*]: unsuspend {
  &label: likes
}
```

#### Utilizing imports

As you may have noticed, each of these examples repeated the initial models. You can
further apply the "one model" principle by defining models once in their own file and
importing them. See the [import model-view pattern](/tour/model-view/) for more.

### Legend — `docs/tour/legend.md`

Use a special variable, `d2-legend`, to declare a legend.

```d2
vars: {
  d2-legend: {
    a: {
      label: Microservice
    }
    b: Database {
      shape: cylinder
      style.stroke-dash: 2
    }
    a <-> b: Good relationship {
      style.stroke: red
      style.stroke-dash: 2
      style.stroke-width: 1
    }
    a -> b: Bad relationship
    a -> b: Tenuous {
      target-arrowhead.shape: circle
    }
  }
}

api-1
api-2

api-1 -> postgres
api-2 -> postgres

postgres: {
  shape: cylinder
}
postgres -> external: {
  style.stroke: black
}

api-1 <-> api-2: {
  style.stroke: red
  style.stroke-dash: 2
}
api-1 -> api-3: {
  target-arrowhead.shape: circle
}
```

#### Hiding shapes

Since `a -> b` declares 3 things (1 connection and 2 shapes), 3 things will show up on the
legend. If you only intended to show the connection in the legend, you can set the opacity
of shapes to exclude them from the legend.

```d2
vars: {
  d2-legend: {
    a <-> b: Good relationship {
      style.stroke: red
      style.stroke-dash: 2
    }
    a.style.opacity: 0
    b.style.opacity: 0
  }
}

api-1 <-> api-2: {
  style.stroke: red
  style.stroke-dash: 2
}
api-1 -> api-3: {
  target-arrowhead.shape: circle
}
```

#### Rename "legend"

You may rename "legend" by simply giving it a label. This is particularly useful for
non-English diagrams.

```d2
vars: {
  d2-legend: "凡例" {
    # Legend items...
  }
}
# Rest of diagram...
```

### Autoformat — `docs/tour/auto-formatter.md`

You almost never have to think about style decisions like indentation, newlines,
number of hyphens, or spacing. D2's auto-formatter will format your D2 file for you on
compile, keeping all your declarations consistent and readable, effortlessly.

If your file is

```d2
aws_s3:    AWS S3 California{
  Monitoring ---------->California
}
```

When you compile, it becomes

```d2
aws_s3: AWS S3 California {
  Monitoring -> California
}
```

#### Running formatter

If you're using the `d2` CLI, you can run the formatter on files with

```sh
d2 fmt file.d2
```

The formatter is meant to be integrated into plugins and extensions which automatically
call the formatter upon file writing. This functionality is dependent on the plugin.

### Intro to Composition — `docs/tour/composition.md`

This section's documentation is incomplete. We'll be adding more to this section soon.

D2 has built-in mechanisms for you to compose multiple boards into one diagram.

For example, this is a composition of 2 boards, exported as an animated SVG:

The way to define another board in a D2 diagram is to use 1 of 3 keywords. Each of these
declare boards with different inheritance rules.

| Keyword   | Inheritance                                       |
|-----------|---------------------------------------------------|
| `layers`    | Boards which do not inherit. They are a new base. |
| `scenarios` | Boards which inherit from the base layer.         |
| `steps`     | Boards which inherit from the previous step.      |

Each one serves different use cases. The example above is achieved by defining a Scenario
(the scenario of when we have to deploy a hotfix).

Thus far, all D2 diagrams we've encountered are single-board diagrams, the root board.

```d2-incomplete
# Root board
x -> y
```

Composition in D2 is when you use one of those keywords to declare another board.

```d2-incomplete
# Root board
x -> y
layers: {
  # Board named "numbers" that does not inherit anything from root
  numbers: {
    1 -> 2
  }
}
```

So now we have two boards: root and `numbers`. They cannot be visible at the same time of
course, so exports have to accommodate these more dynamic diagrams, such as the animated
SVG you see above.

Composition is one of D2's most powerful features, as you'll see from the use cases in this
section.

### Layers — `docs/tour/layers.md`

A "Layer" represents "a layer of abstraction". Each Layer starts off as a blank
board, since you're representing different objects at every level of abstraction.

Try clicking on the objects.

```d2
explain: |md
  This is the top layer, highest level of abstraction.
| {
  near: top-center
}

Tik Tok's User Data: {
  link: layers.tiktok
}

layers: {
  tiktok: {
    explain: |md
      One layer deeper:

      Tik Tok's CEO explained that user data is stored in two places currently.
    | {
      near: top-center
    }
    Virginia data center <-> Hong Kong data center
    Virginia data center.link: layers.virginia
    Hong Kong data center.link: layers.hongkong
    
    layers: {
      virginia: {
        direction: right
        explain: |md
          Getting deeper into details:

          TikTok's CEO explains that Virginia data center has strict security measures.
        | {
          near: top-center
        }
        Oracle Databases: {
          shape: cylinder
          style.multiple: true
        }
        US residents -> Oracle Databases: access
        US residents: {
          shape: person
        }
        Third party auditors -> Oracle Databases: verify
      }
      hongkong: {
        direction: right
        explain: |md
          TikTok's CEO says data is actively being deleted and should be done by the end of the year.
        | {
          near: top-center
        }
        Legacy Databases: {
          shape: cylinder
          style.multiple: true
        }
      }
    }
  }
}
```

### Scenarios — `docs/tour/scenarios.md`

A "Scenario" represents a different view of the base Layer.

Each Scenario inherits from its base Layer. Any new objects are added onto all objects in
the base Layer, and you can reference any objects from the base Layer to update them.

Notice that in the below Scenario, we simply turn some objects opacity lower, and define a
new connection to show an alternate view of the deployment diagram.

```d2
direction: right

title: {
  label: Normal deployment
  near: bottom-center
  shape: text
  style.font-size: 40
  style.underline: true
}

local: {
  code: {
    icon: https://icons.d2lang.com/dev/go.svg
  }
}
local.code -> github.dev: commit

github: {
  icon: https://icons.d2lang.com/dev/github.svg
  dev
  master: {
    workflows
  }

  dev -> master.workflows: merge trigger
}

github.master.workflows -> aws.builders: upload and run

aws: {
  builders -> s3: upload binaries
  ec2 <- s3: pull binaries

  builders: {
    icon: https://icons.d2lang.com/aws/Developer%20Tools/AWS-CodeBuild_light-bg.svg
  }
  s3: {
    icon: https://icons.d2lang.com/aws/Storage/Amazon-S3-Glacier_light-bg.svg
  }
  ec2: {
    icon: https://icons.d2lang.com/aws/_Group%20Icons/EC2-instance-container_light-bg.svg
  }
}

local.code -> aws.ec2: {
  style.opacity: 0.0
}

scenarios: {
  hotfix: {
    title.label: Hotfix deployment
    (local.code -> github.dev)[0].style: {
      stroke: "#ca052b"
      opacity: 0.1
    }

    github: {
      dev: {
        style.opacity: 0.1
      }
      master: {
        workflows: {
          style.opacity: 0.1
        }
        style.opacity: 0.1
      }

      (dev -> master.workflows)[0].style.opacity: 0.1
      style.opacity: 0.1
      style.fill: "#ca052b"
    }

    (github.master.workflows -> aws.builders)[0].style.opacity: 0.1

    (local.code -> aws.ec2)[0]: {
      style.opacity: 1
      style.stroke-dash: 5
      style.stroke: "#167c3c"
    }
  }
}
```

### Steps — `docs/tour/steps.md`

A "Step" represents a step in a sequence of events.

Each Step inherits from its the Step before it. The first step inherits from its parent,
whether that's a Scenario or Layer.

Notice how in Step 3 for example, the object "Approach road" exists even though it's not
defined, because it was inherited from Step 2, which inherited it from Step 1.

```d2
Chicken's plan: {
  style.font-size: 35
  near: top-center
  shape: text
}

steps: {
  1: {
    Approach road
  }
  2: {
    Approach road -> Cross road
  }
  3: {
    Cross road -> Make you wonder why
  }
}
```

### Linking between boards — `docs/tour/linking.md`

We've introduced `link` before as a way to jump to external resources. They can also be
used to create interactivity to jump to other boards. We'll call these "internal links".

Example of internal link:

```d2
how does the cat go?: {
  link: layers.cat
}

layers: {
  cat: {
    meoowww
  }
}
```

If your board name has a `.`, use quotes to target that board.
For example:

```d2-incomplete
a.link: layers."2012.06"

layers: {
  "2012.06": {
    hello
  }
}
```

#### Parent reference

The underscore `_` is used to refer to the parent scope, but when used in `link` values,
they refer not to parent containers, but to parent boards.

```d2
The shire

journey: {
  link: layers.rivendell
}

layers: {
  rivendell: {
    elves: {
      elrond -> frodo: gives advice
    }

    take me home sam.link: _
    go deeper: {
      link: layers.moria
    }
    
    layers: {
      moria: {
        dwarves

        take me home sam.link: _._
      }
    }
  }
}
```

#### Backlinks

Notice how the navigation bar at the top is clickable. You can easily return to the root
or any ancestor page by clicking on the text.

### Export formats — `docs/tour/composition-formats.md`

Since a diagram composed of multiple boards can't be represented as a single image, the
export options are different.

- Multiple SVGs
  - The default output writes multiple SVG files to your output path.
  - They are nicely organized on the file system, with appropriate directories and file
    names.
  - Internal board links are rewritten to point to those file paths, so they work if you
    open the SVG and just click on it.
- Single animated SVG
  - This is useful for small compositions. It's great for a small number of Steps or
    flipping between some Scenarios, but if the composition has too many boards, the
    viewer may get confused or wait until a loop.
  - On the CLI, passing `--animate-interval=1200` sets the resulting SVG to be an
    animation that stays on each board for 1200ms.
- Single animated GIF
  - Same as above, but useful in different contexts, like where SVG is not rendered.
- PDF
  - PDF can be multiple pages, so this medium is suitable for multi-board diagrams.
    Each board is simply another page, and objects can be linked to those pages.
  - This is the most suitable medium for layers currently.
- PowerPoint
  - Specify the output as `.pptx` to get a PowerPoint presentation.
  - Works on Google Slides, for easy web sharing of multi-board diagrams.

### Syntax — `docs/tour/imports.md`

There are two ways to import. These two examples both have the same result:

> Result of running both types of imports below

In the next section, we'll see examples of common import use cases.

#### Two types of imports

##### 1. Regular import

- `x.d2`
```d2-incomplete
x: {
  shape: circle
}
```
- `y.d2`
```d2-incomplete
a: @x.d2
a -> b
```

This is the equivalent of giving the entire file of `x` as a map that `a` sets as its
value.

##### 2. Spread import

- `x.d2`
```d2-incomplete
x: {
  shape: circle
}
```
- `y.d2`
```d2-incomplete
a: {
  ...@x.d2
}
a -> b
```

This tells D2 to take the contents of the file `x` and insert it into the map.

Spread imports only work within maps. Something like `a: ...@x.d2` is an invalid usage.

#### Omit the extension

Above, we wrote the full file name for clarity, but the correct usage is to just specify
the file name without the suffix. If you run D2's autoformatter, it'll change

```d2-incomplete
x: @x.d2
```

into

```d2-incomplete
x: @x
```

D2 will not open files that don't have `.d2` extension, which means an import like
`@x.txt` won't work.

#### Partial imports

You don't have to import the full file.

For example, if you have a file that defines all the people in your organization, and you
just want to show some relations between managers, you can import a specific object.

`donut-flowchart.d2`
```d2
...@people.management
joe -> donuts: loves
jan -> donuts: brings
```

`people.d2`
```d2
management: {
  joe: {
    shape: person
    label: Joe Donutlover
  }
  jan: {
    shape: person
    label: Jan Donutbaker
  }
}
# Notice how these do not appear in the rendered diagram
employees: {
  toby: {
    shape: person
    label: Toby Simonton
  }
}
```

Since `.` is used for targeting, if you want to import from a file with `.` in its name,
use string quotes.

`@"schema-v0.1.2"`

#### Relative imports

Relative imports are relative to the file, not the executing path.

Consider that your working directory is `/Users/You/dev`. Your D2 files:

- `/Users/you/dev/d2-stuff/x.d2`
```d2-incomplete
y: @../y.d2
```

The above import will search directory `/Users/you/dev/` for `y.d2`, not `/Users/You`.

Unnecessary relative imports are removed by autoformat.

`@./x` will be autoformatted to `@x`.

#### Absolute imports

You can also use absolute paths for imports.

```d2-incomplete
# Unix/Linux/Mac
x: @/absolute/path/to/file

# Windows - must use quotes due to backslashes and colons
x: @"C:\absolute\path\to\file"
```

### Overview — `docs/tour/imports-use-cases.md`

The following are examples of some popular use cases for imports. Fundamentally, D2
imports behave just like dependencies in other programming languages, so it is flexible
for doing much more than the ones shown here.

#### Patterns

- [Model-view](/tour/model-view/)
- [Modular classes](/tour/modular-classes/)
- [Nested composition](/tour/nested-composition/)

#### Principles

Alongside the patterns that imports can be used for, splitting your diagram into multiple
files can also fulfill useful principles for organizations:

- **Compliance**. Some core piece of architecture needs to follow a spec exactly, and that
  file should not change while others around it can.
- **Domain-driven design**. Diagramming a large architecture? Get different domain experts to
  diagram their parts, and put them together in one diagram.
- **Code reviews**. While text-based diagramming makes reviewing changes possible, we've
  all been in situations where the diff shown makes the review appear more complex than it
  is. When your diagram is more modular, it's easier for everyone to know what's changed.
  Maybe the changes to `style.d2` don't need as much scrutiny as the `security.d2` file
  changes.
- **Reusability**. Your organization can define one `color-classes.d2`, and that can be
  imported and used across all diagrams for a consistent diagram style.
- **Don't repeat yourself**. When multiple files import an object, you only have to make
  changes to that one object to update it everywhere else.

#### More Examples

Some more creative, practical examples of using imports that mix and match the above
patterns and principles.

- [Version visualization](/tour/version-visualization/)
- [Template](/tour/imported-template/)

### Model-view — `docs/tour/model-view.md`

A popular pattern defines your models once, and then reuses it across a number of
different views.

#### `models.d2`
```d2
postgres: {
  shape: cylinder
  icon: https://icons.d2lang.com/dev%2Fpostgresql.svg
  icon.near: bottom-center
}
it: IT Guy {
  shape: person
  style: {
    fill: maroon
  }
}
vpn: {
  style: {
    shadow: true
  }
  tooltip: IP is 192.2.2.1
}
```

#### `access-view.d2`
```d2
...@models
it -> vpn -> postgres
```

#### `ssh-view.d2`
```d2
...@models
it -> postgres: ssh, bypassing VPN
```

### Modular classes — `docs/tour/modular-classes.md`

This pattern mirrors web development, separating HTML and CSS.

#### `classes.d2`
```d2
classes: {
  base: {
    style: {
      border-radius: 4
      shadow: true
    }
  }
  error: {
    style.fill: pink
    style.stroke: red
  }
  med: {
    width: 200
    height: 200
    style.font-size: 24
  }
  large: {
    width: 300
    height: 300
    style.font-size: 28
  }
  xlarge: {
    width: 400
    height: 400
    style.font-size: 32
  }
  person: {
    shape: person
    style.stroke-dash: 3
  }
}
```

#### `main.d2`
```d2
...@classes
user.class: person
error.class: [base; error]
modal.class: [base; med]

user -> app.signup: click
app.signup -> error: invalid fields
app.signup -> modal: continue registration
```

### Nested composition — `docs/tour/nested-composition.md`

Imports make large compositions much more manageable.

Large diagrams like the ones that take you from high-level overview to low-level details
becomes possible to cleanly construct.

Rendering `overview.d2` gives us a nested diagram while each file is kept flat and
readable.

##### `overview.d2`
```d2
serviceA -> serviceB
serviceB.link: layers.serviceB

layers: {
  serviceB: @serviceB
}
```

##### `serviceB.d2`
```d2
aws vault: {
  key
  token
}
stripe: {
  customer id
}
aws vault.key -> data
aws vault.token -> data
stripe.customer id -> data
data.link: layers.data

layers: {
  data: @data
}
```

##### `data.d2`
```d2
users: {
  shape: sql_table
  id: int
  token: string
  customer_id: string
}

# Continue nesting as needed!
# layers: {
#   ...
# }
```

### Version visualization — `docs/tour/version-visualization.md`

#### History

You want to understand how the schema of a system has evolved over time. As long as the
diagram is modularized with imports, such a visualization is easy to whip up.

- `history.d2`
```d2
direction: right
Users 1: Users Table (v0.1) {
  ...@"users-v0.1"
}

Users 2: Users Table (current) {
  ...@users-current
}

Users 1 -> Users 2
```

- `users.d2` (latest version, 0.2)
```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  email: int {constraint: foreign_key}
  name: string
  password: text
  created_at: timestamp
  last_updated: timestamp
}

emails: {
  shape: sql_table
  id: int {constraint: [primary_key; unique]}
  local: string
  domain: string
  verified: boolean
}
users.email -> emails.id
```

- `users.d2` (0.1)
```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  email: string
  name: string
  verified_email: boolean
  password: string
  created_at: timestamp
}
```

Since you want how `users.d2` looked like at `v0.1`, you use `git` to get that version:

```sh
cp users.d2 users-current.d2
git checkout tags/v0.1 users.d2
mv users.d2 users-v0.1.d2
```

#### Compare

You're a manager at Apple who has two teams secretly working on the same product for
multiple years. After years of iterating in their silos, you form a committee to compare
the two results. The evaluation starts by comparing their design decisions in an
overarching diagram projected in a dark room behind a closed door.

- `compare.d2`
```d2-incomplete
Team Alpha: {
  Quick facts: |md
    - 3 L6 engineers
  |
  Schema: {
    ...@alpha-schema
  }
  API: {
    ...@alpha-api
  }
  # etc etc
}

Team Charlie: {
  Quick facts: |md
    - 2 L5
    - 5 L4
    - 15 L3
  |
  Schema: {
    ...@charlie-schema
  }
  API: {
    ...@charlie-api
  }
  # etc etc
}
```

And then you checkout the corresponding diagrams from the different repositories.
```sh
gh repo clone apple/team-alpha
gh repo clone apple/team-charlie

cp apple/team-alpha/schema.d2 alpha-schema.d2
cp apple/team-charlie/schema.d2 charlie-schema.d2

cp apple/team-alpha/api.d2 alpha-api.d2
cp apple/team-charlie/api.d2 charlie-api.d2
```

The rendered diagram is left as an exercise to the reader.

### Template — `docs/tour/imported-template.md`

You make diagrams for external consulting clients. In order to appear professional, all
diagrams must be contained within a template that your designer has created that is
on-brand.

- `diagram.d2`
```d2
template: {
  ...@imports-wrapper-template
  synergy: {
    our firm -> yours: value add
  }
  stakeholders: {
    george.shape: person
    tim.shape: person
    tim.tooltip: is this web scale?
  }
}
```

- `wrapper-template.d2`
```d2
style: {
  fill: "#E3EDE6"
  fill-pattern: dots
  stroke: "#820758"
  stroke-width: 3
  border-radius: 2
  shadow: true
}
label: ""
```

This use case will be made much more powerful when D2 finishes glob (`*`) support.

### Exports — `docs/tour/exports.md`

On the CLI, you may export `.d2` into
* [SVG](#svg)
* [PNG](#png)
* [PDF](#pdf)
* [PPTX](#pptx)
* [GIF](#gif)
* [ASCII](#ascii)
* [Stdout](#stdout)

#### SVG

```shell
d2 in.d2 out.svg
```

SVG is the default export format on the CLI. If you don't specify an output, the export
file will be the input name as an SVG file.

For example, `d2 in.d2` will produce a file named `in.svg`.

The resulting SVG has CSS injected into it. This, along with the use of HTML
`<foreignObject>`s used to make Markdown work, means that the SVG is meant to be viewed in
a web context. For example, opening it up in your browser, embedding it onto a webpage. It
may not look right without a web context, like in Inkscape or Adobe Illustrator.

On the CLI, if you pass in `-`
- for the input, it reads D2 from stdin
- for the output, it writes SVG to stdout

planning on doing post-processing on the SVG exports.

**Element IDs**: All shape elements get CSS classes with base64-encoded IDs for safe CSS
targeting. For example, a shape with ID `my-shape` gets class `bXktc2hhcGU` (base64
encoding of "my-shape").

**Unique identifiers**: Each diagram gets a deterministic hash prefix (e.g.,
`d2-1234567890`) used for clip paths, gradients, and other SVG elements to prevent
conflicts when multiple diagrams are on the same page.

#### PNG

```shell
d2 in.d2 out.png
```

PNG exports work by [Playwright](https://github.com/microsoft/playwright) spinning up a
headless browser, putting the SVG onto it, and taking a screenshot. The first invocation
of Playwright will download its dependencies, if they don't already exist on the machine.

If you get a message like `err: failed to launch Chromium`, you can try installing
Playwright dependencies outside of D2 on your machine. For example:

```
npm install -g @playwright
npx playwright install --with-deps chromium
```

See [#744](https://github.com/d2lang/d2/issues/744#issuecomment-1446641870) for more.

#### PDF

```shell
d2 in.d2 out.pdf
```

PDF exports are the result of taking PNG exports and placing them on PDF pages, along with
headers and fonts. As such, dependencies needed for PNG exports are also needed for PDF
exports.

PDF is _more_ interactive than PNG, but _less_ interactive than SVG.

For example, `animate` keyword won't show up in PDF exports like they would in SVG.

But `link`s can still be clickable in PDFs.

#### PPTX

```shell
d2 in.d2 out.pptx
```

Similar to PDF exports. This export format is useful for giving presentations when used
with composition (e.g. diagram with multiple Layers, Scenarios, Steps).

#### GIF

```shell
d2 in.d2 out.gif
```

This export format is useful for giving presentations when used with short compositions.
For example, show two Scenarios, show a couple of steps. Something that the audience can
digest in a loop that lasts a couple of seconds without needing to flip through it
manually.

#### ASCII

ASCII outputs are new as of 0.7.1. They are to be considered in beta, and many diagrams
may not render correctly.

ASCII exports render diagrams as text-based art, perfect for documentation, terminals, and environments where graphical formats aren't suitable. D2 automatically detects the `.txt` file extension and renders in ASCII format.

```shell
d2 in.d2 out.txt
```

##### Character sets

D2 supports two ASCII character modes:

###### Extended mode (default)
Uses Unicode box-drawing characters for cleaner output:

```shell
d2 in.d2 out.txt
```

```
┌───────┐       ┌───────┐
│ Hello │──────▶│ World │
└───────┘       └───────┘
```

###### Standard mode
Uses basic ASCII characters for maximum compatibility:

```shell
d2 --ascii-mode standard in.d2 out.txt
```

```
+-------+       +-------+
| Hello |------>| World |
+-------+       +-------+
```

##### Notes

- Renders only with ELK and TALA, due to curved lines not rendering well in ASCII. If
  Dagre (or unspecified) is chosen, it will render in ELK.
- Some shapes are supported, like Person, but some shapes are hard to represent cleanly in
  ASCII. It's best to avoid using these shapes when the output is ASCII, but if it can't
  be avoided, in these cases, an icon on the top-left corner represents what the shape is
  meant to be.
- Many styles are moot in ASCII, such as shadow or multiple or animated. It's best to keep
  it as simple box and arrow type diagrams.

#### Stdout

D2 accepts `-` in place of the input and/or output arguments. SVG is used as the format
for Stdout output.

For example, this writes a D2 script of `x -> y` and outputs it to a file `example.svg`.

```shell
echo "x -> y" | d2 - - > example.svg
```

### Troubleshooting — `docs/tour/troubleshoot.md`

* [It won't compile a specific label or value](#it-wont-compile-a-specific-label-or-value)
* [The text is rendered too wide/long](#the-text-is-rendered-too-widelong)
* [Connections look cluttered](#connections-look-cluttered)
* [Reserved keywords as regular keys](#reserved-keywords-as-regular-keys)
* [My diagram is breaking with HTML in Markdown](#my-diagram-is-breaking-with-html-in-markdown)
* [Markdown SVGs won't render in certain SVG viewers](#markdown-svgs-wont-render-in-certain-svg-viewers)
* [My SVG isn't interactive when I embed into HTML](#my-svg-isnt-interactive-when-i-embed-into-html)
* [Non-ASCII text breaks stuff](#non-ascii-text-breaks-stuff)

#### It won't compile a specific label or value

It probably has some reserved characters, wrap it around `'` or `"`.

```d2
"x(int y)": "[]int"
'$dollarbills$'
```

#### The text is rendered too wide/long

Add newlines.

```d2
x: When you go out to buy,\ndon't show your silver.
```

#### Connections look cluttered

If you have a highly connected diagram with many connections on shapes with short labels,
you will get better results by manually settings widths and heights on them. By default,
D2 adds a minimal amount of padding to shapes past the label dimensions. When a shape has
many connections, increasing dimensions will give it more surface area for the connections
to route aesthetically to.

#### Reserved keywords as regular keys

If you'd like to use a reserved keyword as a key, just quote it:

```d2
x: {
  "width": width
}
```

#### My diagram is breaking with HTML in Markdown

Your HTML must be semantic to be parsed in SVG XML correctly, e.g. use `<br/>` instead of `<br>`.

#### Markdown SVGs won't render in certain SVG viewers

D2's Markdown support is added via xhtml foreign objects, which means the SVG viewer must
have HTML rendering capabilities. The vast majority of SVG viewing is, but if you intend
to use a pure SVG editor on D2 diagrams that don't have such capabilities (e.g. Adobe
Illustrator), it won't render correctly there.

#### My SVG isn't interactive when I embed into HTML

There's a few different ways to embed SVG into HTML, each with tradeoffs. If you use plain
`` tags, interactivity is blocked. Here are two good resources to learn more:

1. tldr:
   [https://docs.asciidoctor.org/asciidoc/latest/macros/image-svg/#options-for-svg-images](https://docs.asciidoctor.org/asciidoc/latest/macros/image-svg/#options-for-svg-images)
2. The official W3 spec:
   [https://www.w3.org/Graphics/SVG/IG/resources/svgprimer.html#SVG_in_HTML](https://www.w3.org/Graphics/SVG/IG/resources/svgprimer.html#SVG_in_HTML)

#### Non-ASCII text breaks stuff

D2 works with any language, but sometimes non-ASCII characters look like reserved characters when they're not.

```d2
hello世界：مرحبا بالعال
```

The character `：` is not the same as the ASCII `:`, and so it won't register as a label. For foreign language diagrams, please take care to use the ASCII versions of special characters like `:`, `;`, `.`, among others.


## Example gallery: diagrams laid out by TALA

### Bank Securities

```d2
bank:   {
  style.fill: white
  Corporate:   {
    style.fill: white
    app14506: Data Source\ntco:      100,000\nowner: Lakshmi  {
      style:  {
        fill: '#fce7c6'
      }
    }
  }
  Equities:   {
    app14491: Risk Global\ntco:      600,000\nowner: Wendy  {
      style:  {
        fill: '#f6c889'
      }
    }
    app14492: Credit guard\ntco:      100,000\nowner: Lakshmi  {
      style:  {
        fill: '#fce7c6'
      }
    }
    app14520: Seven heaven\ntco:      100,000\nowner: Tomos  {
      style:  {
        fill: '#fce7c6'
      }
    }
    app14522: Apac Ace\ntco:      400,000\nowner: Wendy  {
      style:  {
        fill: '#f9d8a7'
      }
    }
    app14527: Risk Global\ntco:      900,000\nowner: Tomos  {
      style:  {
        fill: '#f4b76c'
      }
    }
  }
  Securities:   {
    style.fill: white
    app14517: Zone out\ntco:      500,000\nowner: Wendy  {
      style:  {
        fill: '#f6c889'
      }
    }
  }
  Finance:   {
    style.fill: white
    app14488: Credit guard\ntco:      700,000\nowner: India  {
      style:  {
        fill: '#f6c889'
      }
    }
    app14502: Ark Crypto\ntco:    1,500,000\nowner: Wendy  {
      style:  {
        fill: '#ed800c'
      }
    }
    app14510: Data Solar\ntco:    1,200,000\nowner: Deepak  {
      style:  {
        fill: '#f1a64f'
      }
    }
  }
  Risk:   {
    style.fill: white
    app14490: Seven heaven\ntco:            0\nowner: Joesph  {
      style:  {
        fill: '#fce7c6'
      }
    }
    app14507: Crypto Bot\ntco:    1,100,000\nowner: Wendy  {
      style:  {
        fill: '#f1a64f'
      }
    }
  }
  Funds:   {
    style.fill: white
    app14497: Risk Global\ntco:      500,000\nowner: Joesph  {
      style:  {
        fill: '#f6c889'
      }
    }
  }
  Fixed Income:   {
    style.fill: white
    app14523: ARC3\ntco:      600,000\nowner: Wendy  {
      style:  {
        fill: '#f6c889'
      }
    }
    app14500: Acmaze\ntco:      100,000\nowner: Tomos  {
      style:  {
        fill: '#fce7c6'
      }
    }
  }
}
bank.Risk.app14490 -> bank.Equities.app14527: client master
bank.Equities.app14491 -> bank.Equities.app14527: greeks  {
  style:  {
    stroke-dash: 5
    animated: true
    stroke: red
  }
}
bank.Funds.app14497 -> bank.Equities.app14520: allocations  {
  style:  {
    stroke-dash: 5
    animated: true
    stroke: brown
  }
}
bank.Equities.app14527 -> bank.Corporate.app14506: trades  {
  style:  {
    stroke-dash: 5
    animated: false
    stroke: blue
  }
}
bank.Fixed Income.app14523 -> bank.Equities.app14491: orders  {
  style:  {
    stroke-dash: 10
    animated: false
    stroke: green
  }
}
bank.Finance.app14488 -> bank.Equities.app14527: greeks  {
  style:  {
    stroke-dash: 5
    animated: true
    stroke: red
  }
}
bank.Equities.app14527 -> bank.Equities.app14522: orders  {
  style:  {
    stroke-dash: 10
    animated: false
    stroke: green
  }
}
bank.Equities.app14522 -> bank.Finance.app14510: orders  {
  style:  {
    stroke-dash: 10
    animated: false
    stroke: green
  }
}
bank.Equities.app14527 -> bank.Finance.app14502: greeks  {
  style:  {
    stroke-dash: 5
    animated: true
    stroke: red
  }
}
bank.Equities.app14527 -> bank.Risk.app14507: allocations  {
  style:  {
    stroke-dash: 5
    animated: true
    stroke: brown
  }
}
bank.Securities.app14517 -> bank.Equities.app14492: trades  {
  style:  {
    stroke-dash: 5
    animated: false
    stroke: blue
  }
}
bank.Equities.app14522 -> bank.Fixed Income.app14500: security reference
```

### Udp Tunnel

```d2
shape: sequence_diagram

backend_server
local_server
ssh_server
other_server

启动阶段: {
    local_server->ssh_server:ssh_login
    local_server<-ssh_server:ssh 登录成功
    local_server->ssh_server:sftp_copy 辅助转发服务器
    local_server->ssh_server:ssh  启动转发服务器
}

启动成功运行阶段:{

        other_server->ssh_server.a:请求udp packet{
            style.animated: true
            style.stroke: red
        }

        ssh_server.a->local_server.a:udp forward 发送给 udp client {
            style.animated: true
            style.stroke: red
        }

        local_server.a->backend_server.a: "udp 转发给 udp server"{
            style.animated: true
            style.stroke: red
        }

        backend_server.b->local_server.b:发送ok字符串给 udp的请求端{
            style.animated: true
            style.stroke: green
        }

        ssh_server.b<-local_server.b: 发送给 ssh 所在的 udp forawrd {
            style.animated: true
            style.stroke: green
        }

        other_server<-ssh_server.b:返回udp 请求回复{
            style.animated: true
            style.stroke:green
        }
        other_server.一次交互完成

}
```

### Llm Framework Architecture

```d2
vars: {
  d2-config: {
    theme-id: 3 # terrastruct
    sketch: true
    layout-engine: elk
  }
  colors: {
    c2: "#C7F1FF" # light turkuaz
    c3: "#B5AFF6" # dark purple
    c4: "#DEE1EB" # gray
    c5: "#88DCF7" # turkuaz
    c6: "#E4DBFE" # purple
  }
}

LangUnits: {
  style.fill: ${colors.c6}
  RegexVal: {
    ds
  }
  SQLSelect: {
    ds
  }
  PythonTr: {
    ds
  }
  langunit ₙ: {
    style.multiple: true
    style.stroke-dash: 10
    style.stroke: black
    style.animated: 1
    "... ds"
  }
}

LangUnits <- ExperimentHost.Dataset: "load dataset"
Dataset UI -> LangUnits: "manage datasets"

Dataset UI: {
  style.fill: ${colors.c4}
}

ExperimentHost: {
  style.fill: ${colors.c4}
  Experiment: {
    style.multiple: true
  }
  Dataset
  # Experiment <-> Dataset
}
ExperimentHost.Experiment -> Experiment

Experiment.ModelConfigurations: {
  style.multiple: true
}
Experiment.LangUnit

Experiment.ModelConfigurations -> ModelConfiguration

ModelConfiguration.Prompting
ModelConfiguration.Model
ModelConfiguration.LangUnit
```

### Terraform Resources

```d2
vars: {
  d2-config: {
    layout-engine: elk
  }
}

*.style.font-size: 22
*.*.style.font-size: 22

title: |md
  # Terraform resources (v1.0.0)
| {near: top-center}

direction: right

project_connection: {
  style: {
    fill: "#C5C6C7"
    stroke: grey
  }
}

privatelink_endpoint: {tooltip: Datasource only}
group
group_partial_permissions
service_token
job: {
  style: {
    fill: "#ACE1AF"
    stroke: green
  }
}

conns: Connections (will be removed in the future,\nuse global_connection) {
  bigquery_connection
  fabric_connection
  connection

  bigquery_connection.style.fill: "#C5C6C7"
  fabric_connection.style.fill: "#C5C6C7"
  connection.style.fill: "#C5C6C7"
}
conns.style.fill: "#C5C6C7"

env_creds: Environment Credentials {
  grid-columns: 2
  athena_credential
  databricks_credential
  snowflake_credential
  bigquery_credential
  fabric_credential
  postgres_credential: {tooltip: Is used for Redshift as well}
  teradata_credential
}

service_token -- project: can scope to {
  style: {
    stroke-dash: 3
  }
}
group -- project
group_partial_permissions -- project
user_groups -- group
user_groups -- group_partial_permissions
project -- environment
project -- snowflake_semantic_layer_credential
job -- environment
job -- environment_variable_job_override
notification -- job
partial_notification -- job

webhook -- job: triggered by {
  style: {
    stroke-dash: 3
  }
}
environment -- global_connection
environment -- conns
global_connection -- privatelink_endpoint
global_connection -- oauth_configuration

environment -- env_creds
conns -- privatelink_endpoint
project -- project_repository
lineage_integration -- project
project_repository -- repository
environment -- environment_variable
environment -- partial_environment_variable
environment -- extended_attributes
environment -- semantic_layer_configuration
model_notifications -- environment

project -- project_connection {
  style: {
    stroke: "#C5C6C7"
  }
}
project_connection -- conns {
  style: {
    stroke: "#C5C6C7"
  }
}

(job -- *)[*].style.stroke: green
(* -- job)[*].style.stroke: green

account_level_settings: "Account level settings" {
  account_features
  ip_restrictions_rule
  license_map
  partial_license_map
}
account_level_settings.style.fill-pattern: dots
```

### Game State Sequence

```d2
shape: sequence_diagram

User
Session
Lua

User."Init"

User.t1 -> Session.t1: "SetupFight()"
Session.t1 -> Session.t1: "Create clean fight state"
Session.t1 -> Lua: "Trigger OnPlayerTurn"
User.t1 <- Session.t1

User."Repeat"

User.mid -> Session.mid: "PlayerCastHand() etc."
Session.mid -> Lua: "Trigger OnDamage etc."
User.mid <- Session.mid

User.t2 -> Session.t2: "FinishPlayerTurn()"
Session.t2 -> Lua: "Trigger OnTurn"
Session.t2 -> Session.t2: "Update and remove status effects"
Session.t2 -> Lua: "Trigger OnPlayerTurn"
User.t2 <- Session.t2
```

### Golang Queue

```d2
direction: right

classes: {
  base: {
    style: {
      bold: true
      font-size: 28
    }
  }

  person: {
    shape: person
  }

  animated: {
    style: {
      animated: true
    }
  }

  multiple: {
    style: {
      multiple: true
    }
  }

  enqueue: {
    label: Enqueue Task
  }

  dispatch: {
    label: Dispatch Task
  }

  library: {
    style: {
      bold: true
      font-size: 32
      fill: PapayaWhip
      fill-pattern: grain
      border-radius: 8
      font: mono
    }
  }

  task: {
    style: {
      bold: true
      font-size: 32
    }
  }
}

user01: {
  label: User01
  class: [base; person; multiple]
}

user02: {
  label: User02
  class: [base; person; multiple]
}

user03: {
  label: User03
  class: [base; person; multiple]
}

user01 -> container.task01: {
  label: Create Task
  class: [base; animated]
}
user02 -> container.task02: {
  label: Create Task
  class: [base; animated]
}
user03 -> container.task03: {
  label: Create Task
  class: [base; animated]
}

container: Application {
  direction: right
  style: {
    bold: true
    font-size: 28
  }
  icon: https://icons.d2lang.com/dev%2Fgo.svg

  task01: {
    icon: https://icons.d2lang.com/essentials%2F092-graph%20bar.svg
    class: [task; multiple]
  }

  task02: {
    icon: https://icons.d2lang.com/essentials%2F095-download.svg
    class: [task; multiple]
  }

  task03: {
    icon: https://icons.d2lang.com/essentials%2F195-attachment.svg
    class: [task; multiple]
  }

  queue: {
    label: Queue Library
    icon: https://icons.d2lang.com/dev%2Fgo.svg
    style: {
      bold: true
      font-size: 32
      fill: honeydew
    }

    producer: {
      label: Producer
      class: library
    }

    consumer: {
      label: Consumer
      class: library
    }

    database: {
      label: Ring\nBuffer
      shape: cylinder
      style: {
        bold: true
        font-size: 32
        fill-pattern: lines
        font: mono
      }
    }

    producer -> database
    database -> consumer
  }

  worker01: {
    icon: https://icons.d2lang.com/essentials%2F092-graph%20bar.svg
    class: [task]
  }

  worker02: {
    icon: https://icons.d2lang.com/essentials%2F095-download.svg
    class: [task]
  }

  worker03: {
    icon: https://icons.d2lang.com/essentials%2F092-graph%20bar.svg
    class: [task]
  }

  worker04: {
    icon: https://icons.d2lang.com/essentials%2F195-attachment.svg
    class: [task]
  }

  task01 -> queue.producer: {
    class: [base; enqueue]
  }
  task02 -> queue.producer: {
    class: [base; enqueue]
  }
  task03 -> queue.producer: {
    class: [base; enqueue]
  }
  queue.consumer -> worker01: {
    class: [base; dispatch]
  }
  queue.consumer -> worker02: {
    class: [base; dispatch]
  }
  queue.consumer -> worker03: {
    class: [base; dispatch]
  }
  queue.consumer -> worker04: {
    class: [base; dispatch]
  }
}
```

### Lambda Infra

````d2
direction: right

github: GitHub {
  shape: image
  icon: https://icons.d2lang.com/dev%2Fgithub.svg
  style: {
    font-color: green
    font-size: 30
  }
}

github_actions: GitHub Actions {
  lambda_action: Lambda Action {
    icon: https://icons.d2lang.com/dev%2Fgithub.svg
    style.multiple: true
  }
  style: {
    stroke: blue
    font-color: purple
    stroke-dash: 3
    fill: white
  }
}

aws: AWS Cloud VPC {
  style: {
    font-color: purple
    fill: white
    opacity: 0.5
  }
  lambda01: Lambda01 {
    icon: https://icons.d2lang.com/aws%2FCompute%2FAWS-Lambda.svg
    shape: parallelogram
    style.fill: "#B6DDF6"
  }
  lambda02: Lambda02 {
    icon: https://icons.d2lang.com/aws%2FCompute%2FAWS-Lambda.svg
    shape: parallelogram
    style.fill: "#B6DDF6"
  }
  lambda03: Lambda03 {
    icon: https://icons.d2lang.com/aws%2FCompute%2FAWS-Lambda.svg
    shape: parallelogram
    style.fill: "#B6DDF6"
  }
}

github -> github_actions: GitHub Action Flow {
  style: {
    animated: true
    font-size: 20
  }
}
github_actions -> aws.lambda01: Update Lambda {
  style: {
    animated: true
    font-size: 20
  }
}
github_actions -> aws.lambda02: Update Lambda {
  style: {
    animated: true
    font-size: 20
  }
}
github_actions -> aws.lambda03: Update Lambda {
  style: {
    animated: true
    font-size: 20
  }
}

explanation: |md
  ```yaml
  deploy_source:
    name: deploy lambda from source
    runs-on: ubuntu-latest
    steps:
      - name: checkout source code
        uses: actions/checkout@v3
      - name: default deploy
        uses: appleboy/lambda-action@v0.1.7
        with:
          aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws_region: ${{ secrets.AWS_REGION }}
          function_name: gorush
          source: example/index.js
  ```
| {near: bottom-center}
````

### Stripe

```d2
👤 Customer -> US Company: '$'
Customer action: |md
  *Customers buy iPhone cases\
  from the US company*
| {
  near: 👤 Customer
}

US Company -> Hong Kong Company: Royalties + price\n of cases
Hong Kong Company -> US Company: Cases, services,\n and IP
US and HK action: |md
  *US company buys cases, services,\
  and IP from Hong Kong company*
| {
  near: Income (US)
}

US Company -> Expenses (US): '$'
US Company -> Income (US): '$'
Income (US) -> Tax (US): '$'
Income action: |md
  *US Company pays\
  taxes on US income*
| {
  near: Income (US)
}

Hong Kong Company -> Expenses (HK): '$'
Hong Kong Company -> Wages: '$'
Hong Kong Company -> Income (Hong Kong): '$'
Income (Hong Kong) -> Tax (Hong Kong): '$'


style: {
  fill: "#F6F9FC"
  stroke: "#CBD6E0"
  stroke-width: 2
  border-radius: 12
}

US Company: {
  style.fill: "#fff"
  style.stroke-width: 0
  style.border-radius: 6
  style.shadow: true
  style.font-color: "#6772E5"
}

Hong Kong Company: {
  style.fill: "#fff"
  style.stroke-width: 0
  style.border-radius: 6
  style.shadow: true
  style.font-color: "#6772E5"
}

👤 Customer: {
  style.fill: "#E6EBF1"
  style.stroke-width: 0
  style.border-radius: 20
  style.font-color: "#525F7F"
}

Expenses (US): {
  style.fill: "#FFE0F5"
  style.stroke-width: 0
  style.border-radius: 20
  style.font-color: "#7939A8"
}

Wages: {
  style.fill: "#FFE0F5"
  style.stroke-width: 0
  style.border-radius: 20
  style.font-color: "#7939A8"
}

Expenses (HK): {
  style.fill: "#FFE0F5"
  style.stroke-width: 0
  style.border-radius: 20
  style.font-color: "#7939A8"
}

Income (Hong Kong): {
  style.fill: "#FFF9C9"
  style.stroke-width: 0
  style.border-radius: 20
  style.font-color: "#9D341E"
}

Income (US): {
  style.fill: "#FFF9C9"
  style.stroke-width: 0
  style.border-radius: 20
  style.font-color: "#9D341E"
}

Tax (US): {
  style.fill: "#FFE7CB"
  style.stroke-width: 0
  style.border-radius: 20
  style.font-color: "#9E2146"
}

Tax (Hong Kong): {
  style.fill: "#FFE7CB"
  style.stroke-width: 0
  style.border-radius: 20
  style.font-color: "#9E2146"
}
```


## Example diagrams from the D2 repository

### `docs/flow.d2`

```d2
# How we actually want it formatted (d2 fmt removes line continuations currently):
# inputFile \
#  -> d2parser\
#  -> d2ast\
#  -> d2compiler\
#  -> d2graph\
#  -> d2layouts/d2dagrelayout\
#  -> d2exporter\
#  -> d2target
inputFile -> d2parser -> d2ast -> d2compiler -> d2graph -> d2layouts/d2dagrelayout -> d2exporter -> d2target
```

### `docs/examples/chess/dia.d2`

```d2
# Actors
hans: Hans Niemann

defendants: {
  mc: Magnus Carlsen
  playmagnus: Play Magnus Group
  chesscom: Chess.com
  naka: Hikaru Nakamura

  mc -> playmagnus: Owns majority
  playmagnus <-> chesscom: Merger talks
  chesscom -> naka: Sponsoring
}

# Accusations
hans -> defendants: 'sueing for $100M'

# Offense
defendants.naka -> hans: Accused of cheating on his stream
defendants.mc -> hans: Lost then withdrew with accusations
defendants.chesscom -> hans: 72 page report of cheating
```

### `docs/examples/flipt/input.d2`

```d2
classes: {
  block: {
    style: {
      font: mono
      stroke-dash: 2
      stroke: black
      border-radius: 5
    }
  }
  grid-block: {
    label: ""
    style: {
      fill: "#6EF759"
      border-radius: 5
    }
    width: 40
    height: 40
  }
}

direction: right

Build: {
  class: block
  style: {
    fill: "#FFEBCD"
  }
  source -> linked
  source -> assets
  linked -> artifacts
  assets -> artifacts
  artifacts: "" {
    shape: image
    icon: https://icons.terrastruct.com/essentials/220-layers.svg
    width: 100
    height: 100
  }
}

Test: {
  class: block
  style: {
    fill: "#ffc9d6"
  }
  grid: "" {
    grid-columns: 4
    grid-rows: 4
    1.class: grid-block
    2.class: grid-block
    3.class: grid-block
    4.class: grid-block
    5.class: grid-block
    6.class: grid-block
    7.class: grid-block
    8.class: grid-block
    9.class: grid-block
    10.class: grid-block
    11.class: grid-block
    12.class: grid-block
    13.class: grid-block
    14.class: grid-block
    15.class: grid-block
    16.class: grid-block

    6.style.fill: red
    12.style.fill: red
  }
}

Release: {
  class: block
  style: {
    fill: "#d5ffcd"
  }

  incoming.class: grid-block
  incoming -> db1
  incoming -> db2

  db1: "" {
    shape: image
    icon: https://icons.terrastruct.com/essentials/117-database.svg
    width: 70
    height: 70
  }
  db2: "" {
    shape: image
    icon: https://icons.terrastruct.com/essentials/117-database.svg
    width: 70
    height: 70
  }
}

Build.artifacts -> Test.grid -> Release.incoming
```

### `docs/examples/japan-grid/japan.d2`

```d2
classes: {
  NONE: {style.opacity: 0}
  GREEN: {style.stroke: "#2b9464"; style.fill: "#2b9464"}
  RED: {style.stroke: "#d14d28"; style.fill: "#d14d28"}
  YELLOW: {style.stroke: "#f5df65"; style.fill: "#f5df65"}
  BLUE: {style.stroke: "#59c8df"; style.fill: "#59c8df"}
}

grid-rows: 12
grid-columns: 12
grid-gap: 0

12-1: "" {class: NONE}
12-2: "" {class: NONE}
12-3: "" {class: NONE}
12-4: "" {class: NONE}
12-5: "" {class: NONE}
12-6: "" {class: NONE}
12-7: "" {class: NONE}
12-8: "" {class: NONE}
12-9: "" {class: NONE}
12-10: "" {class: NONE}
12-11: "" {class: GREEN}
12-12: "北海道" {class: GREEN}

11-1: "" {class: NONE}
11-2: "" {class: NONE}
11-3: "" {class: NONE}
11-4: "" {class: NONE}
11-5: "" {class: NONE}
11-6: "" {class: NONE}
11-7: "" {class: NONE}
11-8: "" {class: NONE}
11-9: "" {class: NONE}
11-10: "" {class: NONE}
11-11: "" {class: GREEN}
11-12: "" {class: GREEN}

10-1: "" {class: NONE}
10-2: "" {class: NONE}
10-3: "" {class: NONE}
10-4: "" {class: NONE}
10-5: "" {class: NONE}
10-6: "" {class: NONE}
10-7: "" {class: NONE}
10-8: "" {class: NONE}
10-9: "" {class: NONE}
10-10: "" {class: NONE}
10-11: "青森" {class: RED}
10-12: "" {class: NONE}

9-1: "" {class: NONE}
9-2: "" {class: NONE}
9-3: "" {class: NONE}
9-4: "" {class: NONE}
9-5: "" {class: NONE}
9-6: "" {class: NONE}
9-7: "" {class: NONE}
9-8: "" {class: NONE}
9-9: "" {class: NONE}
9-10: "" {class: NONE}
9-11: "秋田" {class: YELLOW}
9-12: "岩手" {class: GREEN}

8-1: "" {class: NONE}
8-2: "" {class: NONE}
8-3: "" {class: NONE}
8-4: "" {class: NONE}
8-5: "" {class: NONE}
8-6: "" {class: NONE}
8-7: "" {class: NONE}
8-8: "石川" {class: GREEN}
8-9: "" {class: NONE}
8-10: "新潟" {class: BLUE}
8-11: "山形" {class: RED}
8-12: "宮城" {class: BLUE}

7-1: "" {class: NONE}
7-2: "" {class: NONE}
7-3: "" {class: NONE}
7-4: "" {class: NONE}
7-5: "" {class: NONE}
7-6: "" {class: NONE}
7-7: "" {class: NONE}
7-8: "福井" {class: RED}
7-9: "富山" {class: YELLOW}
7-10: "群馬" {class: GREEN}
7-11: "栃木" {class: YELLOW}
7-12: "福島" {class: GREEN}

6-1: "" {class: NONE}
6-2: "" {class: NONE}
6-3: "山口" {class: RED}
6-4: "島根" {class: YELLOW}
6-5: "鳥取" {class: RED}
6-6: "兵庫" {class: BLUE}
6-7: "京都" {class: YELLOW}
6-8: "滋賀" {class: GREEN}
6-9: "長野" {class: RED}
6-10: "山梨" {class: YELLOW}
6-11: "埼玉" {class: BLUE}
6-12: "茨城" {class: RED}

5-1: "" {class: NONE}
5-2: "" {class: NONE}
5-3: "" {class: NONE}
5-4: "広島" {class: BLUE}
5-5: "岡山" {class: YELLOW}
5-6: "大阪" {class: GREEN}
5-7: "奈良" {class: RED}
5-8: "岐阜" {class: BLUE}
5-9: "愛知" {class: YELLOW}
5-10: "静岡" {class: BLUE}
5-11: "TOKYO" {class: GREEN}
5-12: "千葉" {class: YELLOW}

4-1: "長崎" {class: BLUE}
4-2: "佐賀" {class: RED}
4-3: "福岡" {class: GREEN}
4-4: "" {class: NONE}
4-5: "" {class: NONE}
4-6: "" {class: NONE}
4-7: "和歌山" {class: GREEN}
4-8: "三重" {class: RED}
4-9: "" {class: NONE}
4-10: "" {class: NONE}
4-11: "神奈川" {class: RED}
4-12: "" {class: NONE}

3-1: "" {class: NONE}
3-2: "熊本" {class: YELLOW}
3-3: "大分" {class: BLUE}
3-4: "" {class: NONE}
3-5: "愛媛" {class: RED}
3-6: "香川" {class: BLUE}
3-7: "" {class: NONE}
3-8: "" {class: NONE}
3-9: "" {class: NONE}
3-10: "" {class: NONE}
3-11: "" {class: NONE}
3-12: "" {class: NONE}

2-1: "" {class: NONE}
2-2: "鹿児島" {class: RED}
2-3: "宮崎" {class: GREEN}
2-4: "" {class: NONE}
2-5: "高知" {class: GREEN}
2-6: "徳島" {class: YELLOW}
2-7: "" {class: NONE}
2-8: "" {class: NONE}
2-9: "" {class: NONE}
2-10: "" {class: NONE}
2-11: "" {class: NONE}
2-12: "" {class: NONE}

1-1: "沖縄" {class: BLUE}
1-2: "" {class: NONE}
1-3: "" {class: NONE}
1-4: "" {class: NONE}
1-5: "" {class: NONE}
1-6: "" {class: NONE}
1-7: "" {class: NONE}
1-8: "" {class: NONE}
1-9: "" {class: NONE}
1-10: "" {class: NONE}
1-11: "" {class: NONE}
1-12: "" {class: NONE}
```

### `docs/examples/twitter/in.d2`

```d2
timeline mixer: "" {
  explanation: |md
    ## **Timeline mixer**
    - Inject ads, who-to-follow, onboarding
    - Conversation module
    - Cursoring,pagination
    - Tweat deduplication
    - Served data logging
  |
}
People discovery: "People discovery \nservice"
admixer: Ad mixer {
  style.fill: "#c1a2f3"
}

onboarding service: "Onboarding \nservice"
timeline mixer -> People discovery
timeline mixer -> onboarding service
timeline mixer -> admixer
container0: "" {
  graphql
  comment
  tlsapi
}
container0.graphql: GraphQL\nFederated Strato Column {
  shape: image
  icon: https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/GraphQL_Logo.svg/1200px-GraphQL_Logo.svg.png
}
container0.comment: |md
  ## Tweet/user content hydration, visibility filtering
|
container0.tlsapi: TLS-API (being deprecated)
container0.graphql -> timeline mixer
timeline mixer <- container0.tlsapi
twitter fe: "Twitter Frontend " {
  icon: https://icons.terrastruct.com/social/013-twitter-1.svg
  shape: image
}
twitter fe -> container0.graphql: iPhone web
twitter fe -> container0.tlsapi: HTTP Android
web: Web {
  icon: https://icons.terrastruct.com/azure/Web%20Service%20Color/App%20Service%20Domains.svg
  shape: image
}

Iphone: {
  icon: 'https://ss7.vzw.com/is/image/VerizonWireless/apple-iphone-12-64gb-purple-53017-mjn13ll-a?$device-lg$'
  shape: image
}
Android: {
  icon: https://cdn4.iconfinder.com/data/icons/smart-phones-technologies/512/android-phone.png
  shape: image
}

web -> twitter fe
timeline scorer: "Timeline\nScorer" {
  style.fill: "#ffdef1"
}
home ranker: Home Ranker

timeline service: Timeline Service
timeline mixer -> timeline scorer: Thrift RPC
timeline mixer -> home ranker: {
  style.stroke-dash: 4
  style.stroke: "#000E3D"
}
timeline mixer -> timeline service
home mixer: Home mixer {
  # style.fill: "#c1a2f3"
}
container0.graphql -> home mixer: {
  style.stroke-dash: 4
  style.stroke: "#000E3D"
}
home mixer -> timeline scorer
home mixer -> home ranker: {
  style.stroke-dash: 4
  style.stroke: "#000E3D"
}
home mixer -> timeline service
manhattan 2: Manhattan
gizmoduck: Gizmoduck
socialgraph: Social graph
tweetypie: Tweety Pie
home mixer -> manhattan 2
home mixer -> gizmoduck
home mixer -> socialgraph
home mixer -> tweetypie
Iphone -> twitter fe
Android -> twitter fe
prediction service2: Prediction Service {
  shape: image
  icon: https://cdn-icons-png.flaticon.com/512/6461/6461819.png
}
home scorer: Home Scorer {
  style.fill: "#ffdef1"
}
manhattan: Manhattan
memcache: Memcache {
  icon: https://d1q6f0aelx0por.cloudfront.net/product-logos/de041504-0ddb-43f6-b89e-fe04403cca8d-memcached.png
}

fetch: Fetch {
  style.multiple: true
  shape: step
}

feature: Feature {
  style.multiple: true
  shape: step
}
scoring: Scoring {
  style.multiple: true
  shape: step
}
fetch -> feature
feature -> scoring

prediction service: Prediction Service {
  shape: image
  icon: https://cdn-icons-png.flaticon.com/512/6461/6461819.png
}
scoring -> prediction service
fetch -> container2.crmixer

home scorer -> manhattan: ""

home scorer -> memcache: ""
home scorer -> prediction service2
home ranker -> home scorer
home ranker -> container2.crmixer: Candidate Fetch
container2: "" {
  style.stroke: "#000E3D"
  style.fill: "#ffffff"
  crmixer: CrMixer {
    style.fill: "#F7F8FE"
  }
  earlybird: EarlyBird
  utag: Utag
  space: Space
  communities: Communities
}
etc: ...etc

home scorer -> etc: Feature Hydration

feature -> manhattan
feature -> memcache
feature -> etc: Candidate sources
```

### `docs/examples/vector-grid/vector-grid.d2`

```d2
classes: {
  empty: {
    label: ""
    style: {
      fill: transparent
      stroke-width: 0
    }
  }
  text: {
    style: {
      fill: transparent
      stroke-width: 0
    }
  }
  cluster: {
    style: {
      fill: transparent
      stroke-dash: 4
      stroke: "#C6D3DF"
    }
  }
  grid: {
    grid-columns: 1
    label: ""
    style: {
      fill: white
      stroke-width: 0
    }
  }
  row: {
    grid-rows: 1
    label: ""
    style: {
      fill: transparent
      stroke-width: 0
    }
  }
}

vars: {
  left-cluster: {
    label: "n-sized Vector"
    class: cluster
    0*.style.fill: "#DFEFFA"
    0*.style.stroke: black
    grid-rows: 1
    grid-gap: 0
    label.near: outside-top-left

    "0.62"
    "0.15"
    empty1.class: empty
    n.class: text
    empty2.class: empty
    "0.91"
    "0.48"

    "0.15" <- n -> "0.91"
  }
  right-cluster: {
    label: "m-sized Vector"
    class: cluster
    0*.style.fill: "#72F5FF"
    0*.style.stroke: black
    grid-rows: 1
    grid-gap: 0
    label.near: outside-top-left

    "0.62"
    "0.15"
    empyt1.class: empty
    m.class: text
    empty2.class: empty
    "0.91"
    "0.48"

    "0.15" <- m -> "0.91"
  }
}

grid-rows: 2

top-row: {
  class: row
  empty.class: empty
  empty.width: 1100

  Random Matrix Generator: {
    width: 300
    height: 170
    style.font-size: 20
    style.fill: "#A7BBCF"
    style.stroke: black
    style.border-radius: 10
  }
}

bottom-row: {
  class: row
  left-grid: {
    class: grid

    1: ${left-cluster}
    2: ${left-cluster}
    3: ${left-cluster}
  }

  dot-container: {
    class: empty
    grid-columns: 1
    empty1.class: empty
    dot: Dot product {
      class: text
      circle: "" {
        shape: circle
        style.fill: black
        style.stroke-width: 0
        width: 20
        height: 20
      }
      label.near: outside-bottom-center
    }
  }

  matrix-container: {
    class: empty
    grid-columns: 1
    matrix: Target dimension matrix {
      label.near: outside-top-center
      grid-rows: 4
      grid-gap: 0
      *.width: 100
      *.height: 100
      *.style.fill: "#F1F6F9"
      *.style.stroke: black
      "0.41"
      "0.32"
      "0.92"
      "0.13"

      "0.74"
      "0.15"
      "0.53"
      "0.21"

      "0.97"
      "0.45"
      "0.11"
      "0.05"

      "0.61"
      "0.77"
      "0.59"
      "0.83"
    }
  }

  empty.class: empty

  right-grid: {
    class: grid

    1: ${right-cluster}
    2: ${right-cluster}
    3: ${right-cluster}
  }

  matrix-container -> right-grid
}

top-row.Random Matrix Generator -> bottom-row.matrix-container.matrix
```

### `docs/examples/wcc/wcc.d2`

```d2
How to become the World Chess Champion: {
  near: top-center
  shape: text
  style.font-size: 55
}

gm: Become a Grandmaster (GM) {
  link: layers.gm
}
qualify: Qualify for the Candidates Tournament {
  link: layers.qualify
}
win: Win the Candidates Tournament {
  link: layers.win
}
match: Defeat the former Champion {
  link: layers.match
}

gm -> qualify -> win -> match

layers: {
  gm: {
    description: |md
      # Become a Grandmaster (GM)
      A Grandmaster is the highest title awarded by FIDE (the International Chess Federation).
    | {
      near: top-center
    }
    play: Play in FIDE-rated tournaments
    ➡️: {
      shape: text
      near: center-right
      link: steps.1
      style.font-size: 24
    }

    steps: {
      1: {
        titled: Earn pre-requisite titles (IM)
        play -> titled
        ➡️.link: _.steps.2
      }
      2: {
        ➡️.link: _._
        rating: Achieve 2500 rating
        norms: Earn 3 GM norms\n(defeat other GMs in tournaments)
        titled -> rating
        titled -> norms
      }
    }
  }
  qualify: {
    description: |md
      # Qualify for the Candidates Tournament
      The Candidates tournament is played among the best players in the world to determine the challenger for the next world chess championship.
    | {
      near: top-center
    }
    One of: {
      Runner-up to last championship
      Finish top 2 in FIDE Grand Prix
      Top 2 highest rated
      Organizer wild card
      Occasional other FIDE events: {
        This varies year to year
      }
    }
  }
  win: {
    description: |md
      # Winning the Candidates tournament

      8-players face off in a double round-robin.

      Which mean each player plays every other player, one with white and once with black.
    | {
      near: top-center
    }

    2022 Players: {
      grid-rows: 9
      grid-columns: 3
      grid-gap: 0

      Player
      Rating
      World ranking

      Ian Nepomniachtchi
      2766
      7

      Teimour Radjabov
      2753
      13

      Jan-Krzysztof Duda
      2750
      16

      Alireza Firouzja
      2793
      3

      Fabiano Caruana
      2783
      4

      Hikaru Nakamura
      2760
      11

      Richard Rapport
      2764
      8

      Ding Liren
      2806
      2
    }
  }
  match: {
    description: |md
      # World Chess Championship Match
      A 14-game 1v1 between the challenger and the current world champion[0].

      [0] Usually. In 2023, Magnus Carlsen declined to participate.

      Instead, the runner-up of the Candidates tournament plays.
    | {
      near: top-center
    }

    ding: Ding Liren {
      icon: https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/World_Chess_Championship_2023%2C_game_01%2C_Ding_Liren.jpg/220px-World_Chess_Championship_2023%2C_game_01%2C_Ding_Liren.jpg
      shape: image
      near: center-left
      height: 300
      width: 200
    }

    nepo: Ian Nepomniachtchi {
      icon: https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/World_Chess_Championship_2021%2C_game_07%2C_Ian_Nepomniachtchi_%28cropped%29.jpg/220px-World_Chess_Championship_2021%2C_game_07%2C_Ian_Nepomniachtchi_%28cropped%29.jpg
      shape: image
      near: center-right
      height: 300
      width: 200
    }

    best of 14 games -> tiebreaks: if needed
    tiebreaks.link: layers.tiebreaks

    layers: {
      tiebreaks: {
        description: |md
          # Tiebreaks

          Use faster time controls to induce errors.
        | {
          near: top-center
        }

        rapid: 4 rapid games {
          25 mins per side
          10-second increment
        }

        blitz: 2 blitz games {
          5 mins per side
          3-second increment
        }

        sudden death: {
          3 mins per side
          2-second increment
          repeat until a win
        }

        rapid -> blitz -> sudden death: if needed
      }
    }
  }
}
```


## Further material in the vendored repos

Paths are relative to `/Users/dan/src/devenv/skills/d2`.

- `d2-docs/docs/tour/` — tour pages not inlined above: api, cheat-sheet, community, design, editor-support, experience, extensions, faq, future, help, install, intro, man, obsidian, vim, vscode.
- `d2-docs/static/d2/` — the D2 source of every example in the tour, one file each.
- `d2-docs/docs/examples/dagre.md` and `elk.md` — more galleries, laid out by those
  engines.
- `d2/e2etests/testdata/files/` — 67 test diagrams, many of them real-world
  architecture diagrams. Largest first: `spyre_encoder.d2`, `grid_oom.d2`, `tpmjs_architecture.d2`, `label_positions.d2`, `grid_large_checkered.d2`, `arrowhead_scaling.d2`, `ross_overview.d2`, `jupyter_k8s_oidc.d2`, `queue_workers.d2`, `lion_reader_frontend.d2`.
- `d2/e2etests/*_test.go` — named feature-by-feature diagram snippets.
- `d2/d2compiler/compile_test.go` and `d2/d2ir/` — compiler semantics, including the
  errors D2 reports for invalid programs.
- `d2/ci/release/changelogs/` — release notes; `next.md` covers the unreleased version.
- `d2/d2layouts/d2talalayout/README.md` and `ARCHITECTURE.md` — how TALA works, and its
  Go API.
- `d2/ci/release/template/man/d2.1` — man page.
- `d2/docs/assets/cheat_sheet.pdf` — one-page language cheat sheet.
- `d2/docs/examples/lib/` — driving D2 as a Go library.
- Icons for the `icon` keyword: https://icons.d2lang.com.
