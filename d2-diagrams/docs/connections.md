# D2 Connections

Source: https://d2lang.com/tour/connections

## Connection Operators

```d2
a -- b       # undirected
a -> b       # directed (left to right)
a <- b       # directed (right to left)
a <-> b      # bidirectional
```

Shapes referenced in connections are auto-created if not declared.

## Labels

```d2
a -> b: sends request
```

Connections reference shape keys, not labels.

## Chaining

```d2
a -> b -> c -> d
```

## Repeated Connections

Each declaration creates an additional connection (does not override):
```d2
db -> s3: daily backup
db -> s3: weekly snapshot
```

## Cycles

```d2
stage1 -> stage2 -> stage3 -> stage1
```

## Arrowheads

```d2
a -> b: {
  source-arrowhead: {
    shape: diamond
    style.filled: true
  }
  target-arrowhead: {
    shape: cf-many-required
    label: 1
  }
}
```

### Arrowhead Shapes

- `triangle` (default; `style.filled: false` for open)
- `arrow` (pointed variant)
- `diamond` (supports `style.filled: true`)
- `circle` (supports `style.filled: true`)
- `box` (supports `style.filled: true`)
- `cf-one` (crow's foot: one)
- `cf-one-required` (crow's foot: exactly one)
- `cf-many` (crow's foot: many)
- `cf-many-required` (crow's foot: one or more)
- `cross`

Keep arrowhead labels short.

## Referencing Connections

Style existing connections by index:
```d2
a -> b
a -> b
(a -> b)[0].style.stroke: red
(a -> b)[1].style.stroke: blue
```
