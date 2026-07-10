---
name: temporal-logs
description: |
  Query Temporal Cloud logs from Loki (LogQL) using the `temporal-logs` CLI. Use this
  skill whenever the user wants to look at, search, grep, tail, count, or aggregate logs
  from services running on our EKS clusters — history, matching, frontend, worker,
  saas-api, or anything in a cell — by cluster, namespace, container, pod, or node. Also
  use it when the user gives a cell/cluster id (e.g. s-cd015, newton, endurance) and asks
  what happened, wants error rates or top error causes, or wants to pull raw logs for a
  time window. Prefer this over ad-hoc kubectl/logcli. Even if the user doesn't say
  "Loki" or "LogQL", if they're asking about server/cell logs, use this skill.
  Triggers: "logs", "Loki", "LogQL", "grep the logs", "check the logs", "log volume",
  "error rate", "top errors", "what happened in cell", "history logs", "frontend logs",
  "pull logs", "tail logs", "count log lines", "logs for pod".
version: 0.1.0
---

# temporal-logs

Query the central Loki log store for a Temporal Cloud environment. Logs from everything on
our EKS clusters ship to one Loki per environment; you reach it through a kubectl
port-forward to `loki-query-frontend` (bypassing ALB mTLS) and issue LogQL queries against
the HTTP API. The `temporal-logs` CLI wraps all of this.

## The tool

`temporal-logs` (in `~/bin`, source at `~/src/devenv/tools/python/temporal-logs`).

**Read its help first** — it carries the LogQL cheat-sheet, indexed-label list, and worked
examples, and is the source of truth for flags:

```
temporal-logs --help
temporal-logs query --help      # LogQL guidance + examples
temporal-logs labels --help
```

Subcommands:
- `query '<logql>'` — run a query, print log lines (or metric samples).
- `labels [name]` — list indexed label names, or the values of one label (great for
  discovering which clusters/containers exist before querying).
- `port-forward` — hold a long-lived tunnel; `query`/`labels` start one automatically when
  needed, so you rarely call this.

## How to use it

1. **Pick the environment.** `--env prod` (default) or `--env test`. Prod holds the
   customer-serving fleet — `p-*`, `o-*`, `c-prod-*`, the ring cells `s-aw*`/`s-gc*`/etc.,
   and named cells like `newton`; test holds dev/bench/release cells (`s-wlkr-*`,
   `s-cgsrel-*`, `s-compute-*`, …). The `s-` prefix appears in both, so don't infer the
   env from it — if a cluster id returns nothing, it's probably in the other env.
2. **Discover selectors if unsure.** `temporal-logs labels cluster` (add `--env test` for
   the test fleet) lists cluster ids; `temporal-logs labels k8s_container` lists container
   names. This avoids guessing.
3. **Query.** Start the selector as narrow as you can, then filter. Keep the time window
   tight — queries scan a lot of data.

```bash
# Recent history-service logs in a prod cell
temporal-logs query '{cluster="s-aw031", k8s_namespace="temporal", k8s_container="history"}' --since 30m

# Errors only, as JSON objects (for further processing)
temporal-logs query '{cluster="s-aw031", k8s_container="history"} |= `"level":"error"`' -o jsonl --since 1h

# Top 10 error causes in the last hour (metric query — note the [1h] range in the query)
temporal-logs query 'topk(10, sum(count_over_time({cluster="s-aw031", k8s_container=~"frontend|matching|history|worker"} |= "error" | json | level="error" [1h])) by (error))' --instant --since 1h

# A specific historical window, on a test cell
temporal-logs query '{cluster="s-wlkr-a-aws395"} |= "shard ownership lost"' --env test \
  --from 2025-08-10T15:03:59Z --to 2025-08-10T19:04:16Z
```

## LogQL essentials

The full cheat-sheet is in `temporal-logs query --help`; the key mental model:

- A query is a **stream selector** `{...}` using only **indexed labels**
  (`cluster, env, k8s_app, k8s_container, k8s_namespace, k8s_node_name, k8s_pod`),
  optionally followed by filters and, for aggregations, a metric function.
- **Line filters** (grep on the raw line): `|= "x"` contains, `!= "x"` excludes,
  `|~`/`!~` regex.
- **Parse then filter non-indexed fields** — most logs are JSON: append `| json` and you
  can filter any field, e.g. `| json | level="error"` or `| json | grpc_time_ms > 200`.
  `| json` adds real overhead, so filter with line filters first where possible.
- **Metric queries** aggregate: `count_over_time`, `sum(...) by (label)`, `topk`. The range
  selector (`[5m]`, `[1h]`) is part of the LogQL and is **required** inside
  `count_over_time(...)` — the CLI does not add it. Pass `--instant` for a single snapshot
  or `--step 1m` for a time series; those control when/how often the query is evaluated,
  not the range vector.

## Cost discipline

These queries can touch gigabytes. Before running anything broad:
- Always constrain `cluster`, and add `k8s_namespace`/`k8s_container` when you can.
- Keep the window small (`--since 15m` beats `--since 24h`); widen only if needed.
- Log queries are capped at `--limit` (default 1000). The CLI prints the returned line
  count to stderr and warns when results were truncated — if you hit the cap, narrow the
  query rather than just raising the limit.

## When access fails

The CLI auto-starts the port-forward via `ct`. If `ct` isn't on PATH or auth is needed,
it prints the exact manual command. Since that command is long-running and may need
interactive auth, ask the user to start it themselves — in a Claude Code session they can
run it with the `!` prefix — then re-run with `--addr http://localhost:3100` (or set
`LOKI_ADDR`). Do not invent fallbacks; use the single documented path.

## Grafana

For interactive exploration the user may prefer Grafana Explore (prod:
https://observabilityprod2.tmprl-internal.cloud/explore , internal:
https://grafana.tmprl-internal.cloud/explore) with the `loki` datasource. The LogQL is
identical to what this CLI takes, so you can hand the user a query to paste, or run it here.
