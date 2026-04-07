# D2 Interactive Features

Source: https://d2lang.com/tour/interactive

## Tooltips

Display text on hover:
```d2
server: Backend Server {
  tooltip: Handles API requests and auth
}
```

Tooltips use HTML title tags — Markdown is not rendered in tooltips.

In PNG export, tooltips become numbered footnotes in an appendix.

## Links

Navigate on click:
```d2
docs: Documentation {
  link: https://docs.example.com
}
```

### URL Fragments

Escape `#` in URLs (otherwise treated as d2 comment):
```d2
page: {
  link: "https://example.com/page#section"
}
```
