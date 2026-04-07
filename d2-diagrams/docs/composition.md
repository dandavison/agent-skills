# D2 Composition (Multi-Board)

Source: https://d2lang.com/tour/composition

## Three Board Keywords

### Layers
Independent boards (no inheritance):
```d2
a -> b

layers: {
  network: {
    server -> client
  }
  database: {
    primary -> replica
  }
}
```

### Scenarios
Inherit from the base layer:
```d2
server -> db: normal query

scenarios: {
  cache_hit: {
    server -> cache: lookup
    cache -> server: hit
  }
  error: {
    server -> db: query
    db -> server: timeout
  }
}
```

### Steps
Each step inherits from the previous step (sequential):
```d2
steps: {
  step1: {
    client -> server: request
  }
  step2: {
    server -> db: query
  }
  step3: {
    db -> server: result
    server -> client: response
  }
}
```

## Rendering

Multiple boards export as animated SVG with `--animate-interval`:
```bash
d2 --animate-interval=1000 input.d2 output.svg
```

## Nulling in Scenarios/Steps

Remove inherited elements:
```d2
base_shape -> other

scenarios: {
  minimal: {
    base_shape -> other: null
  }
}
```
