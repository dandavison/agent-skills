# D2 Globs (Wildcards)

Source: https://d2lang.com/tour/globs

## Overview

Globs apply bulk changes using wildcard patterns. They apply both backward (existing shapes) and forward (new shapes).

## Basic Glob

Style all shapes:
```d2
*.style.fill: "#eee"

a
b
c
```

## Connection Globs

Connect all shapes to one target:
```d2
* -> server

client1
client2
client3
server
```

Self-connections from globs are omitted by design.

## Scoped Globs

Globs respect scope — only affect shapes within their container:
```d2
container: {
  *.style.fill: red
  a
  b
}
outside  # not affected
```

## Case Insensitive

Glob matching is case-insensitive.

## Multiple Globs

Multiple glob rules can coexist:
```d2
*.style.fill: "#eee"
*.style.stroke: "#333"
```
