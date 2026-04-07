# D2 Overrides and Nulling

Source: https://d2lang.com/tour/overrides

## Merge Behavior

Redeclaring a shape merges with the previous declaration:
```d2
server: {
  style.fill: blue
}
server: {
  style.stroke: red
}
# server now has both fill: blue and stroke: red
```

The latest label setting takes priority.

## Nulling (Deletion)

Remove elements with `null`:
```d2
a -> b
a -> b: null    # removes connection

unwanted_shape: null  # removes shape
shape.attribute: null # removes attribute
```

Nulling a container removes all its descendants. Nulling a shape removes its connections.

## Use Cases

- Remove elements from imported diagrams
- Selective overrides in scenarios/steps
- Bulk glob rules with specific exclusions
