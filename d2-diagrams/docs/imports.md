# D2 Imports

Source: https://d2lang.com/tour/imports

## Regular Import

Assign an entire file as a map value:
```d2
network: @network
```

Imports `network.d2` into the `network` container.

## Spread Import

Insert file contents directly into the current map:
```d2
...@common-styles
```

Spread imports only work within maps.

## Partial Import

Access specific objects within files:
```d2
db_config: @infrastructure.databases
```

## File Paths

```d2
@x              # relative, omit .d2 extension
@../shared/base # parent directory
@/absolute/path # absolute path
```

Extension is optional (`.d2` appended automatically).

## Filenames with Dots

Quote filenames containing periods:
```d2
@"schema-v0.1.2"
```

## Constraints

- Only `.d2` files can be imported
- Paths are relative to the importing file, not the working directory
