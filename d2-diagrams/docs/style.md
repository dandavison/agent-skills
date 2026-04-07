# D2 Style Properties

Source: https://d2lang.com/tour/style

## Applying Styles

```d2
my_shape: {
  style: {
    fill: "#ff6347"
    stroke: "#333"
    stroke-width: 2
    border-radius: 8
    shadow: true
    font-size: 18
  }
}
```

On connections:
```d2
a -> b: {
  style: {
    stroke: red
    stroke-dash: 5
    animated: true
  }
}
```

## All Style Properties

### Shape and Connection
- **opacity**: float 0-1
- **stroke**: CSS color, hex, or gradient
- **stroke-width**: integer
- **stroke-dash**: integer (dash length)
- **font**: font name
- **font-size**: integer
- **font-color**: CSS color or hex
- **bold**: true/false
- **italic**: true/false
- **underline**: true/false
- **text-transform**: uppercase, lowercase, capitalize, none

### Shape Only
- **fill**: CSS color, hex, or gradient
- **fill-pattern**: dots, lines, grain, paper
- **border-radius**: integer
- **shadow**: true/false
- **3d**: true/false (rectangles/squares only)
- **multiple**: true/false (stacked appearance)
- **double-border**: true/false (rectangles and ovals)

### Connection Only
- **animated**: true/false (animated dashes)

### Root Level
- **root**: styles applied to the diagram background

```d2
style.root: {
  fill: "#f0f0f0"
}
```

## SQL Table / Class Special Behavior

For `sql_table` and `class` shapes:
- `fill` controls the **header** color
- `stroke` applies as fill to the **body**
