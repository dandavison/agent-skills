# D2 UML Class Diagrams

Source: https://d2lang.com/tour/uml-classes

## Basic Syntax

```d2
MyClass: {
  shape: class

  # Fields (no parentheses)
  +name: string
  -id: int
  #email: string

  # Methods (have parentheses)
  +getName(): string
  +setName(name string)
  -validate(): bool
}
```

## Visibility Prefixes

| Prefix | Meaning |
|--------|---------|
| (none) | Public (default) |
| `+` | Public |
| `-` | Private |
| `#` | Protected |

## Complex Types

```d2
Handler: {
  shape: class
  +fields: []string
  +process(ctx context.Context): (Result, error)
}
```

## Relationships

Combine with connections for full UML class diagrams:
```d2
Animal: {
  shape: class
  +name: string
  +speak(): string
}

Dog: {
  shape: class
  +breed: string
  +speak(): string
}

Dog -> Animal: inherits
```
