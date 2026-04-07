# D2 Containers

Source: https://d2lang.com/tour/containers

Containers group shapes hierarchically via nesting.

## Basic Nesting

```d2
clouds: {
  aws: {
    load_balancer
    api
    db
  }
  gcloud: {
    auth
    compute
  }
}
```

## Dot Notation (Flat Syntax)

Equivalent to nesting:
```d2
clouds.aws.load_balancer
clouds.aws.api
```

## Container Labels

```d2
server: Backend Server {
  handler
  db
}
```

Or with the reserved `label` keyword:
```d2
server: {
  label: Backend Server
  handler
  db
}
```

## Cross-Container Connections

```d2
frontend: {
  app
}
backend: {
  api
  db
}
frontend.app -> backend.api: HTTP
backend.api -> backend.db: SQL
```

## Parent Reference with Underscore

`_` refers to the parent scope:
```d2
christmas: {
  birthday: {
    presents
  }
  presents
  birthday.presents -> _.presents: regift
}
```
