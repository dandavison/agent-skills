# D2 Grid Diagrams

Source: https://d2lang.com/tour/grid-diagrams

## Basic Grid

```d2
my_grid: {
  grid-rows: 2
  grid-columns: 3

  a; b; c
  d; e; f
}
```

## Single Dimension

Rows only (vertical stack):
```d2
stack: {
  grid-rows: 3
  first
  second
  third
}
```

Columns only (horizontal):
```d2
row: {
  grid-columns: 4
  a; b; c; d
}
```

## Gap Control

```d2
my_grid: {
  grid-rows: 2
  grid-columns: 2
  grid-gap: 20
  a; b; c; d
}
```

Individual control:
```d2
my_grid: {
  grid-rows: 2
  grid-columns: 2
  vertical-gap: 10
  horizontal-gap: 30
  a; b; c; d
}
```

`grid-gap: 0` removes all spacing (useful for tile maps).

## Cell Sizing

```d2
my_grid: {
  grid-rows: 2
  grid-columns: 2
  a: { width: 200; height: 100 }
  b
  c
  d
}
```

## Nested Grids

```d2
outer: {
  grid-rows: 2
  top: {
    grid-columns: 3
    a; b; c
  }
  bottom: {
    grid-columns: 2
    d; e
  }
}
```

## Fill Order

When both grid-rows and grid-columns are set, whichever keyword appears first determines the dominant fill direction.
