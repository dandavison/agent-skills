# D2 Variables

Source: https://d2lang.com/tour/vars

## Declaration

```d2
vars: {
  primary: "#4A90D9"
  app-name: My App
}
```

## Substitution

```d2
vars: {
  primary: "#4A90D9"
}

header: {
  style.fill: "${primary}"
}
```

## Nested Variables

```d2
vars: {
  db: {
    host: localhost
    port: 5432
  }
}
connection_string: "${db.host}:${db.port}"
```

## Scoping

Substitutions use the closest scope. Inner vars shadow outer:
```d2
vars: {
  x: outer
}
container: {
  vars: {
    x: inner
  }
  label: "${x}"  # resolves to "inner"
}
```

Can reference outer scope vars but not inner scope vars from outside.

## Escaping

Single quotes prevent substitution:
```d2
vars: {
  name: Alice
}
literal: '${name}'  # displays literally as ${name}
```

## Spread Substitution

Distribute map contents:
```d2
vars: {
  common-style: {
    style.fill: "#eee"
    style.stroke: "#333"
  }
}
my_shape: {
  ...${common-style}
}
```

## Configuration Variables (d2-config)

```d2
vars: {
  d2-config: {
    theme-id: 6
    dark-theme-id: 200
    pad: 50
    sketch: true
  }
}
```

CLI flags and env vars take precedence over d2-config.
