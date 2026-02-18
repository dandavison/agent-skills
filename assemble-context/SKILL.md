---
name: assemble-context
description: |
  Assemble a task-specific context brief by searching across multiple sources (Slack, Notion, git repos, Temporal docs, meeting notes). Runs as a subagent to avoid burning tokens in the main conversation. Use when starting a non-trivial task that benefits from gathering relevant context from enterprise sources first.
  Triggers: "assemble context", "gather context", "research context for", "context brief", "seed prompt"
---

# Assemble Context

Given a task description, launch a subagent that searches across available sources,
triages results for relevance, and writes a structured context brief to a file. The
main conversation stays clean; context arrives as a file you can reference with `@`.

## Workflow

1. Ask the user for the **task description** if not already provided.

2. Ask which sources to search (default: all). Available sources:
   - **Slack** — via `agent-slack` CLI
   - **Notion** — via `user-notion` MCP (`notion-search`, `notion-query-meeting-notes`, `notion-fetch`)
   - **Git repos** — at `~/src/temporal-all/repos` and any other relevant repos
   - **Temporal docs** — via `user-temporal-docs` MCP (requires auth first)
   - **Meeting notes** — via `notion-query-meeting-notes`
   - **Meeting transcripts** — via `hyprnote-search` CLI (see `~/.cursor/skills/hyprnote/SKILL.md`)
   - **Temporal Cloud operational details** - via `oncall` repo

3. Launch a `generalPurpose` subagent using the Task tool. Pass it a prompt
   constructed from the template in [subagent-prompt.md](subagent-prompt.md),
   substituting the task description and selected sources.

4. The subagent writes its output to `~/context-briefs/<slug>.md` where `<slug>`
   is a short kebab-case name derived from the task.

5. Tell the user the file path so they can `@`-reference it.

## Notes

- Use multiple subagents in parallel if the task has clearly separable research areas.
- The subagent should prefer breadth over depth: surface many potentially-relevant
  items with brief summaries, rather than deeply reading a few.
- Token budget guidance for the brief: aim for 15-30K tokens of assembled context.
  Prioritize by estimated relevance. Summarize long items; include short items verbatim.
