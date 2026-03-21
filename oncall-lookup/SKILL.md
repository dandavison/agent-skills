---
name: oncall-lookup
description: |
  Look up Temporal Cloud oncall operational knowledge — alert triage, incident patterns,
  dashboards, commands, gotchas, and component behavior. Use this skill whenever the user
  asks about: oncall triage or alert handling, PagerDuty alert names or symptoms, Temporal
  Cloud operational issues (latency, errors, scaling, replication, visibility), what to do
  when paged, cell/namespace debugging, Astra/WAL/OpenSearch operational behavior, or
  anything related to running Temporal Cloud in production. Also use when the user mentions
  specific alert names like "PersistenceLatencySevereFiveMinutes" or symptoms like
  "shard ownership lost". Even if the user doesn't say "oncall", if their question is about
  Temporal Cloud operational triage, production incidents, or alert response — use this skill.
  Triggers: "oncall", "paged", "alert", "triage", "incident", "PagerDuty", "cell health",
  "shard ownership", "persistence latency", "visibility latency", "ResourceExhausted",
  "replication lag", "DLQ", "Astra", "WAL", "OpenSearch", "chronicle", "gotcha",
  "what do I do when", "how to handle", "on-call"
---

# Oncall Knowledge Lookup

This skill gives you access to a structured knowledge base synthesized from 502 real
Temporal Cloud incidents, 14 months of #oncall-hosted-service messages (~20,000), and
9,114 PagerDuty alerts. The repo lives at `~/src/temporal-all/repos/oncall`.

## What's available

The repo contains three tiers of information, from synthesized to raw:

### Tier 1: Synthesized artifacts (start here)

**`oncall-knowledge-base.md`** (~2,300 lines) — the primary artifact. Contains:
- **Symptom-to-Alert Quick Reference** (lines 7-36): table mapping observed symptoms to
  likely alert names and which section to read next
- **Universal Triage Checklist** (lines 39-110): first-5-minutes procedure when paged
- **Gotchas & Tribal Knowledge** (lines 112-204): non-obvious failure modes organized by
  subsystem (auth, rate limiting, database, UI, migration, monitoring)
- **Essential Tools & Dashboards** (lines 207-375): Grafana URLs, CLI commands, Chronicle
  queries, Prometheus queries, runbook links, escalation paths
- **Alert Reference Cards** (lines 377-2045): ~80 individual alert types, each with
  frequency stats, auto-resolution rate, median resolution time, top affected cells,
  root causes, triage steps, and resolution actions. Organized into four groups:
  - Persistence, Database & Latency (lines 377-825)
  - Replication, Migration & Visibility (lines 825-1333)
  - Infrastructure, Scaling & Metrics (lines 1333-1845)
  - Control Plane, Canary, Workflow & Operational (lines 1845-2045)
- **Symptom-Based Diagnosis** (lines 2047-2172): decision trees for common symptoms like
  "I'm seeing high API latency", "I'm seeing ResourceExhausted errors", etc.
- **Component Quick Reference** (lines 2174-end): per-component summaries for
  Astra/Cassandra, WAL/BookKeeper, OpenSearch, Control Plane, Networking/Proxy, Metrics Pipeline

### Tier 2: Structured correlation data

In `correlation/`:
- **`alert-stats.json`** — per-alert-type statistics: total count, monthly average,
  median resolution time (minutes), auto-resolution rate, top affected cells
- **`symptom-map.json`** — symptom keywords mapped to alert types with frequency counts
- **`alert-incidents.json`** — alert types mapped to formal incident channel references

These are useful for quantitative questions ("which alerts fire most often?", "what's the
auto-resolution rate for X?", "which cells are most affected by Y?").

### Tier 3: Raw and intermediate data (rarely needed)

- `incidents/*/slack.txt` — stripped incident channel transcripts
- `incidents/*/extracted.json` — per-incident LLM-extracted diagnostics, root cause, resolution
- `oncall-channel/YYYY-MM.txt` — stripped monthly oncall channel transcripts
- `oncall-channel/YYYY-MM-extracted.json` — per-month extracted alert patterns
- `pagerduty/YYYY-MM.json` — raw PagerDuty incident data

Use Tier 3 only when Tiers 1 and 2 don't answer the question — e.g., the user wants
the full transcript of a specific incident, or wants to find a conversation about a
particular customer or namespace that isn't covered in the synthesized material.

## How to answer questions

### For alert-specific questions
1. Search `oncall-knowledge-base.md` for the alert name (e.g., grep for
   `PersistenceLatencySevereFiveMinutes`). Each alert reference card has frequency,
   resolution time, root causes, and triage steps.
2. If you need quantitative stats beyond what's in the card, read `correlation/alert-stats.json`
   and look up the alert name.
3. If you need to know which incidents involved this alert, check `correlation/alert-incidents.json`.

### For symptom-based questions ("I'm seeing X")
1. Check the **Symptom-to-Alert Quick Reference** table (top of knowledge base) to identify
   which alerts correspond to the symptom.
2. Read the **Symptom-Based Diagnosis** section (lines 2047-2172) for the decision tree.
3. Then look up specific alert reference cards as needed.

### For "how do I triage" / "what do I do when paged"
Read the **Universal Triage Checklist** (lines 39-110).

### For "what's the gotcha with X" / tribal knowledge
Read the **Gotchas & Tribal Knowledge** section (lines 112-204), which is organized by
subsystem: auth, rate limiting, database, UI/frontend, migration, monitoring.

### For tooling questions (dashboards, commands, queries)
Read the **Essential Tools & Dashboards** appendix (lines 207-375).

### For component behavior questions
Read the **Component Quick Reference** (lines 2174-end) for Astra, WAL, OpenSearch,
Control Plane, Networking, or Metrics Pipeline.

### For quantitative / statistical questions
Read the JSON files in `correlation/`:
- `alert-stats.json` for per-alert frequency, resolution time, auto-resolution rate
- `symptom-map.json` for symptom-to-alert mappings with counts
- `alert-incidents.json` for alert-to-incident linkage

### For deep-dive into a specific past incident
Search `incidents/*/extracted.json` for keywords, or grep `incidents/*/slack.txt` for
specific namespaces, cells, or error messages.

## Important context

- Data covers **Jan 2025 – Feb 2026** (14 months)
- `oncall-knowledge-base.md` supersedes the older `playbook.md` and `oncall-guide.md`
- Alert reference cards include PagerDuty statistics — these are historical frequencies
  and may shift as the system evolves
- The repo is at `~/src/temporal-all/repos/oncall` — all paths above are relative to it
