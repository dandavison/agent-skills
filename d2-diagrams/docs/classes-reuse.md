# D2 Classes (Style Reuse)

Source: https://d2lang.com/tour/classes

## Defining Classes

```d2
classes: {
  error: {
    style.fill: "#ff4444"
    style.stroke: "#cc0000"
    style.font-color: white
  }
  success: {
    style.fill: "#44ff44"
    style.stroke: "#00cc00"
  }
}
```

## Applying to Objects

```d2
my_shape.class: error
```

Or inline:
```d2
my_shape: {
  class: error
}
```

## Applying to Connections

At declaration:
```d2
a -> b: {
  class: error
}
```

After declaration:
```d2
(a -> b)[0].class: error
```

## Multiple Classes

```d2
my_shape.class: [error; success]
```

Applied left-to-right (later classes override earlier).

## Override Precedence

Object attributes override class attributes:
```d2
classes: {
  base: {
    style.fill: blue
  }
}
my_shape: {
  class: base
  style.fill: red  # wins over class
}
```

## SVG Integration

Classes are written as `class` attributes in SVG output, enabling custom CSS/JS post-processing.
