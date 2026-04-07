# D2 Shapes

Source: https://d2lang.com/tour/shapes

## Declaring Shapes

```d2
imAShape
im_a_shape
im a shape
i'm a shape
```

Multiple shapes on one line with semicolons:
```d2
a; b; c
```

## Labels

By default the label is the key. Override with:
```d2
pg: PostgreSQL
```

## Shape Types

Set via `shape` keyword. Default is `rectangle`.

```d2
my_cloud: {
  shape: cloud
}
```

### All Available Shapes

**Basic**: rectangle, square, page, parallelogram, document, cylinder, queue, package, step, callout, stored_data, person, diamond, oval, circle, hexagon, cloud

**Special**: c4-person, image, sequence_diagram, sql_table, class

**Aspect-ratio locked (1:1)**: circle, square — if you set both width and height, both dimensions use the larger value.

## Size

```d2
my_shape: {
  width: 200
  height: 100
}
```

## Case Sensitivity

Keys are case-insensitive: `postgresql` and `postgreSQL` reference the same shape.
