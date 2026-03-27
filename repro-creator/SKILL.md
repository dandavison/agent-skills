---
name: repro-creator
description: |
  Procedure for an AI agent to create a bug-reproduction script that produces a markdown report.
  Use this skill whenever you need to reproduce a bug — whether the user explicitly asks
  ("create a repro", "reproduce this issue") or you're investigating a bug report and need
  to make it concrete before attempting a fix. If a bug has been identified but not yet
  demonstrated with evidence, this skill applies.
---

# Create Bug Reproduction

Write a runnable script that reproduces a bug and produces a **markdown report** as output.
The report is the deliverable — it should be a self-contained document that a human can read
to understand exactly what's going wrong, with the evidence right there in front of them.

If you cannot reproduce the bug, say so and stop.

## Script behavior

The script should output a markdown document on stdout with the following sections

1. Introduce the problem in a brief header.
2. For each scenario that demonstrates the bug:
   - Describe what the scenario is testing and what you'd expect to see.
   - Show the commands that were run in a bash code block (so that the reader sees exactly what was
     executed).
   - Show captured stdout, stderr, and exit code.
   - If the evidence is visual (e.g. a UI bug), capture a screenshot and embed it.
3. Summarize the findings — what's broken and how the output differs from what's expected.

The markdown output should be clear enough that someone unfamiliar with the bug can read it and
understand what should happen and what actually happens, and can copy and paste the commands to
recreate the same output.

## Practical details

- Place the script somewhere sensible for the project. Study the project's layout before
  choosing.
- Include a comment at the top with the single command needed to run it.
- Use `set -euo pipefail` (or the equivalent for the script's language) so failures are
  caught rather than silently swallowed.
