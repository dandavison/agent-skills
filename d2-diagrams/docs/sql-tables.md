# D2 SQL Tables

Source: https://d2lang.com/tour/sql-tables

## Basic Syntax

```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: varchar
  email: varchar {constraint: unique}
  created_at: timestamp
}
```

## Constraints

| Full Name | Abbreviation |
|-----------|-------------|
| primary_key | PK |
| foreign_key | FK |
| unique | UNQ |

Custom constraints are displayed as-is.

### Multiple Constraints

```d2
id: {
  type: int
  constraint: [primary_key; unique]
}
```

## Foreign Key Connections

```d2
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: varchar
}

posts: {
  shape: sql_table
  id: int {constraint: primary_key}
  user_id: int {constraint: foreign_key}
  title: varchar
}

posts.user_id -> users.id
```

With ELK or TALA layout engines, connections point to exact rows.

## Reserved Keywords

Wrap SQL reserved words in quotes:
```d2
my_table: {
  shape: sql_table
  "select": varchar
  "order": int
}
```
