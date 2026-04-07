# D2 Icons

Source: https://d2lang.com/tour/icons

## Adding Icons

```d2
server: Server {
  icon: https://icons.terrastruct.com/essentials%2F112-server.svg
}
```

## Local Images

```d2
logo: {
  icon: ./my_logo.svg
}
```

## Standalone Icon (Image Shape)

```d2
github: {
  shape: image
  icon: https://icons.terrastruct.com/dev%2Fgithub.svg
}
```

## Icon Placement

Automatic by layout engine:
- Container icons: top-left corner
- Non-container icons: centered

Manual positioning (TALA layout only):
```d2
my_shape: {
  icon: ./icon.svg
  icon.near: top-right
}
```

## Icon Library

Free architecture icons: https://icons.terrastruct.com

Categories include: AWS, GCP, Azure, Kubernetes, networking, databases, essentials, dev tools.
