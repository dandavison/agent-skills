# D2 CLI Reference

## Basic Usage

```bash
d2 input.d2 output.svg       # compile to SVG
d2 input.d2 output.png       # compile to PNG
d2 input.d2                   # defaults to input.svg
echo 'a -> b' | d2 - -       # stdin to stdout
```

## Key Flags

```bash
d2 --layout=elk input.d2 output.svg       # layout engine
d2 --theme=6 input.d2 output.svg          # theme
d2 --dark-theme=200 input.d2 output.svg   # dark mode theme
d2 --sketch input.d2 output.svg           # hand-drawn style
d2 --pad=50 input.d2 output.svg           # padding (default 100)
d2 --scale=0.5 input.d2 output.svg        # scale factor
d2 --center input.d2 output.svg           # center in viewbox
d2 --animate-interval=1000 in.d2 out.svg  # multi-board animation
d2 --target='layers.x' input.d2 out.svg   # render specific board
d2 --force-appendix input.d2 output.svg   # tooltip appendix in SVG
```

## Watch Mode

```bash
d2 --watch input.d2 output.svg            # live reload in browser
d2 --watch --host=0.0.0.0 --port=8080 input.d2 output.svg
```

## Other Commands

```bash
d2 fmt input.d2         # format d2 file
d2 themes               # list available themes
d2 layout               # list layout engines
d2 layout dagre         # show engine-specific options
```
