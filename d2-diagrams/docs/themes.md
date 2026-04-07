# D2 Themes

Source: https://d2lang.com/tour/themes

## Setting Themes

### In d2 file
```d2
vars: {
  d2-config: {
    theme-id: 200
    dark-theme-id: 200
  }
}
```

### CLI
```bash
d2 --theme=6 input.d2 output.svg
d2 --dark-theme=200 input.d2 output.svg
```

## Available Themes

### Light
| ID | Name |
|----|------|
| 0 | Neutral default |
| 1 | Neutral Grey |
| 3 | Flagship Terrastruct |
| 4 | Cool classics |
| 5 | Mixed berry blue |
| 6 | Grape soda |
| 7 | Aubergine |
| 8 | Colorblind clear |
| 100 | Vanilla nitro cola |
| 101 | Orange creamsicle |
| 102 | Shirley temple |
| 103 | Earth tones |
| 104 | Everglade green |
| 105 | Buttered toast |
| 300 | Terminal |
| 301 | Terminal Grayscale |
| 302 | Origami |

### Dark
| ID | Name |
|----|------|
| 200 | Dark Mauve |
| 201 | Dark Flagship Terrastruct |

## Terminal Theme Special Behavior

The Terminal theme (300) applies unique defaults:
- All caps labels
- No border radius
- Monospaced font
- Fill-pattern: dots for containers
- Double-border on outermost containers

## Theme Overrides

```d2
vars: {
  d2-config: {
    theme-overrides: {
      N1: "#000000"
      B1: "#ff0000"
    }
    dark-theme-overrides: {
      N1: "#ffffff"
    }
  }
}
```

### Color Codes
- N1-N7: Neutrals (backgrounds, text, borders)
- B1-B6: Blues (primary)
- AA2-AA5: Accent A
- AB4-AB5: Accent B
