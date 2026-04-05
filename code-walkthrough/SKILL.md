---
name: code-walkthrough
description: |
  Explain how code, a feature, PR, diff, or branch works by adding numbered walkthrough
  comments and producing a reordered diff that reads as a coherent narrative. Use this skill
  whenever the user asks you to "walk through", "explain with comments", "annotate", or
  "create a walkthrough" for code, a PR, a diff, a branch, or a feature. Also use when the
  user wants a guided tour of how something works in the codebase.
---

# Code Walkthrough

Produce a walkthrough: numbered comments inserted into code, presented as a diff whose hunks
are reordered so they read sequentially as a narrative explanation.

The reorder-diff script is at: `~/.agents/skills/code-walkthrough/scripts/reorder-diff`

## Procedure

### 1. Determine scope

Figure out what the user wants walked through:

- **A branch or PR**: diff against the base branch (`git merge-base` to find the fork point,
  then read the changed files).
- **A feature or mechanism in the codebase**: read the relevant code paths.
- **A specific diff the user provides**: use that directly.

If ambiguous, ask the user to clarify. Prefer to ask one targeted question rather than
guessing wrong.

### 2. Study the code

Read and understand the relevant code thoroughly before writing any comments. Trace the
execution flow, understand the data transformations, identify the key design decisions.
The quality of the walkthrough depends entirely on the depth of your understanding.

### 3. Write walkthrough comments

Add comments to the working tree that walk the reader through the code in a logical
narrative order. Each comment starts with `[WALKTHROUGH i/N]` where i is the step number
and N is the total count.

**Walkthrough comments must be pure additions.** The final walkthrough diff is a
presentation format: the reader sees the original code as context, with your `+` comment
lines interleaved as annotations. If you modify or replace existing code, the diff will
contain `-` lines, which breaks this format — the reader would see deletions that have
nothing to do with the walkthrough narrative. So: only insert new comment lines, never
touch existing code or comments.

Use the language's idiomatic comment syntax. Place each comment on the line above the
code it describes. Keep comments concise — one to three sentences. The sequence should
tell a story: what happens first, what happens next, why something is done a certain way.

Choose an order that makes sense as a narrative for the reader, not necessarily the order
the code appears in source files. For example, you might start with the entry point, then
follow the call chain, then explain a helper that was invoked earlier.

### 4. Generate the raw diff

```bash
git diff -U77 > /tmp/walkthrough-raw.diff
```

Default to 77 lines of context. The user may request a different value. Large context
means multiple walkthrough comments will often share a hunk — that's fine. The
reorder-diff script handles this by creating a separate copy of the hunk for each
walkthrough step, stripping the other steps' markers from each copy.

### 5. Reorder and clean the diff

Run the bundled script:

```bash
~/.agents/skills/code-walkthrough/scripts/reorder-diff /tmp/walkthrough-raw.diff /tmp/walkthrough.diff
```

This reorders hunks by walkthrough number and strips other walkthrough markers from each
hunk's context, so the reader sees only the current step's comment in each hunk.

### 6. Revert the walkthrough comments

```bash
git checkout -- .
```

The comments were scaffolding. The final artifact is the diff file, not the modified source.

### 7. Present the result

Tell the user where the walkthrough diff is (e.g. `/tmp/walkthrough.diff`) and briefly
summarize what the walkthrough covers and how many steps it has.
