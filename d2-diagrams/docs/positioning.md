# D2 Positioning

Source: https://d2lang.com/tour/positions

## Near Keyword

Position elements at diagram edges:
```d2
title: My Diagram {
  near: top-center
}
```

### Valid Positions

`top-left`, `top-center`, `top-right`, `center-left`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`

## Use Cases

### Diagram Title
```d2
title: Architecture Overview {
  near: top-center
  style.font-size: 28
  style.bold: true
}
```

### Legend
```d2
legend: |md
  **Legend**
  - Blue: services
  - Red: databases
| {
  near: bottom-right
}
```

### Label and Icon Positioning
```d2
my_shape: {
  label.near: top-center
  icon: ./icon.svg
  icon.near: top-left
}
```

## Note

By default, positioning is controlled entirely by the layout engine. `near` is the primary mechanism for manual position override. Full position locking (`top`/`left`) is only available with the TALA layout engine.
