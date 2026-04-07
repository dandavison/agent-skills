# D2 Sequence Diagrams

Source: https://d2lang.com/tour/sequence-diagrams

## Creating a Sequence Diagram

Set `shape: sequence_diagram` on a container:

```d2
my_sequence: {
  shape: sequence_diagram

  alice
  bob
  server

  alice -> bob: Hello
  bob -> server: Check auth
  server -> bob: OK
  bob -> alice: Hi back
}
```

## Key Rules

1. **Ordering matters**: Definition order = visual order (unlike other d2 diagrams).
2. **Shared scope**: All children share the same scope. `alice` in a group refers to the same top-level `alice`.
3. **Standard d2 syntax**: No special syntax — use normal connections.

## Actors

Declare actors explicitly to control their order:
```d2
seq: {
  shape: sequence_diagram
  client
  api
  db
  # Now connections can reference them in any order
  client -> api: POST /users
  api -> db: INSERT
  db -> api: row
  api -> client: 201 Created
}
```

Actors can have custom labels and shapes:
```d2
seq: {
  shape: sequence_diagram
  a: Alice {
    shape: person
  }
  b: Bob
}
```

## Spans (Activation Boxes)

Show when an actor is active by nesting:
```d2
seq: {
  shape: sequence_diagram
  client
  server
  db

  client -> server.handler: request
  server.handler -> db: query
  db -> server.handler: result
  server.handler -> client: response
}
```

## Groups (Fragments)

Label subsets of interactions:
```d2
seq: {
  shape: sequence_diagram
  alice
  bob

  auth check: {
    alice -> bob: credentials
    bob -> alice: token
  }

  data flow: {
    alice -> bob: request with token
    bob -> alice: data
  }
}
```

Objects referenced in group connections must exist at the top level.

## Notes

Unconnected nested objects on actors:
```d2
seq: {
  shape: sequence_diagram
  alice
  bob

  alice -> bob: hello
  alice.note: Waiting for response
  bob -> alice: hi
}
```

## Self-Referential Messages

```d2
seq: {
  shape: sequence_diagram
  server

  server -> server: health check
}
```

## Integration

Sequence diagrams are standard d2 objects — they can be contained in other shapes, connected to other shapes, styled, and composed with other diagram types.

```d2
system: {
  frontend
  backend: {
    shape: sequence_diagram
    api
    db
    api -> db: query
    db -> api: result
  }
  frontend -> backend: HTTP
}
```
