# D2 Text and Labels

Source: https://d2lang.com/tour/text

## Standalone Text

Standalone text renders as Markdown:
```d2
explanation: |md
  # Overview
  This system handles **authentication** and *authorization*.
  - OAuth2 flow
  - JWT tokens
|
```

## Markdown Labels on Shapes

Declare the shape first, then set its label:
```d2
my_shape: {
  shape: rectangle
  label: |md
    ## Title
    Some **bold** text
  |
}
```

## LaTeX

```d2
formula: |latex
  \\frac{n!}{k!(n-k)!}
|
```

Use `latex` or `tex` as the language identifier.

## Code Blocks

```d2
my_code: |go
  func main() {
      fmt.Println("Hello")
  }
|
```

## Language Support

D2 supports any language: Chinese, Japanese, Korean, Lao, Khmer, emojis.
