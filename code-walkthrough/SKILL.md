---
name: code-walkthrough
description: |
  Explain how code, a feature, PR, diff, or branch works by adding numbered walkthrough
  comments and producing a reordered diff that reads as a coherent narrative. Use this skill
  whenever the user mentions "walkthrough" in the context of code, a PR, a diff, a branch,
  or a feature — including "walk through", "code walkthrough", "create a walkthrough",
  "explain with comments", "annotate", or "guided tour".
---

# Code Walkthrough

Produce a walkthrough of code changes or a codebase feature. The output is a diff that
interleaves walkthrough comments with the actual code, reordered so that reading the diff
from top to bottom tells a coherent story.

The build-walkthrough script is at: `~/.agents/skills/code-walkthrough/scripts/build-walkthrough`

## How it works

The walkthrough is a transformation from an input diff to an output diff. You study the
diff and codebase, then produce a **manifest** (JSON) that tells the script how to
partition, reorder, and annotate the diff. The script constructs the output mechanically
and validates a critical invariant: every `+`/`-` line from the original diff appears
exactly once in the output.

Your job is codebase comprehension and narrative decisions. The script handles all diff
syntax, hunk headers, and line counts.

## Procedure

### 1. Obtain the input diff

Determine what the user wants walked through and obtain a diff:

**A branch, PR, or commit** — generate the diff directly:
```bash
git diff -U77 $(git merge-base HEAD <base-branch>)..HEAD > /tmp/original.diff
```

Make absolutely sure at this stage that you are working with the diff that the user intends. For
example, are you really sure what the base branch should be? Is it from main, or master, or is it
part of a stacked PR? If it's a GitHub PR, what branch is the PR targeting? Check that their local
branch is up to date with the remote. Etc. If you have any uncertainty, stop and ask the user.


**An existing feature in the codebase** — create a synthetic diff. The working tree must
be clean (error out if it isn't). Remove the feature from the codebase (it doesn't need
to compile; this is for explanation purposes). Commit that removal. Revert the commit.
Now the revert commit's diff is your input: it shows the feature being "added", which is
exactly the narrative you want. Generate the diff of that revert and use it as input.

If the scope is ambiguous, ask the user to clarify.

### 2. Study the diff and codebase

Read the diff with line numbers (`cat -n /tmp/original.diff`). Read the changed files in
full. Trace execution flow, understand data transformations, identify key design decisions.
The walkthrough quality depends entirely on the depth of your understanding.

### 3. Write the manifest

Produce a JSON file that partitions the original diff into narrative-ordered, annotated
steps. Every `+`/`-` line in the original diff must be assigned to exactly one step.

```json
{
  "summary": "Adds request validation to the handler and wraps the return value.",
  "steps": [
    {
      "comment": "New validation function checks for required fields.",
      "start_line": 19,
      "end_line": 24,
      "context_before": 0,
      "context_after": 1
    },
    {
      "comment": "The handler now calls validate() (step 1) before processing.",
      "start_line": 7,
      "end_line": 9,
      "context_before": 1,
      "context_after": 3
    }
  ]
}
```

**Fields:**
- `summary`: A brief, reader-friendly description of what the overall diff achieves.
  Prefer a gentle, high-level framing over terse changelog language. Emitted as
  `[WALKTHROUGH 0/N]` at the top of the output.
- `comment`: Your walkthrough text for one step. The script puts `[WALKTHROUGH i/N]`
  on its own line, then your text on subsequent lines, formatted with the file's comment
  syntax and a `▶` prefix. Write plain prose, not code comments.
- `start_line` / `end_line`: Inclusive, 1-indexed line numbers in the original diff file.
  Must start and end on `+`/`-` lines. Any context (` `) lines between them are included
  automatically.
- `context_before`: Number of context lines to show before the first diff line, for
  orientation ("where am I in this file?"). Default: 3.
- `context_after`: Number of context lines to show after the last diff line. Default: 3.

**Narrative design guidelines:**

**Start with a gentle overview.** The walkthrough should feel welcoming to a reader who
does not yet know why the change exists. Use the summary and early steps to establish:
what problem this branch is solving, why the old behavior was insufficient, and the broad
shape of the solution. Prefer explanatory framing like "This branch teaches history how
to..." or "The core challenge is..." over abrupt formulations like "Adds X" unless the
change is truly tiny.

Steps are in narrative order — the array position determines the walkthrough number. The
reader will read them sequentially, so the sequence should tell a story: start with the
entry point or the most important concept, then follow the execution flow or the logical
dependencies.

**Group related changes into one step.** An addition and the removal it replaces belong
together — the reader wants to see old and new side by side, not as separate steps. A
function and the import it requires are one logical change. The goal is one step per
*concept*, not one step per contiguous block of `+`/`-` lines.

**Orient the reader in the call graph.** When explaining a function, connect it to what
the reader has already seen or will see next. If the reader already saw the call site,
remind them: "This is the validate() function called in step 2." If they haven't seen
the caller yet, foreshadow it: "This helper will be called from the main handler in
step 4." The reader should never wonder "when does this get called?"

Choose context amounts semantically. A step introducing a new function in an unfamiliar
file needs more context than a one-line change in a function the reader just saw.

**Flag questionable code.** Your primary job is narrative explanation, not code review.
But if you encounter something that looks wrong, risky, or suspicious — a potential bug,
a race condition, a missing error check, a security concern — don't silently pass over
it. Prefix that step's comment with ❗ and briefly say what concerns you.

Every `+`/`-` line must appear in exactly one step. Less interesting changes (imports,
formatting, boilerplate) still get steps — just brief comments, placed later in the
sequence. The script will reject a manifest that doesn't cover all diff lines.

### 4. Build the walkthrough

```bash
~/.agents/skills/code-walkthrough/scripts/build-walkthrough \
  /tmp/original.diff /tmp/manifest.json .task/walkthrough.diff
```

If the user requested extra context lines (e.g. "with 77 context lines", "lots of
context"), pass `--context N` to override every step's `context_before`/`context_after`:

```bash
~/.agents/skills/code-walkthrough/scripts/build-walkthrough \
  --context 77 \
  /tmp/original.diff /tmp/manifest.json .task/walkthrough.diff
```

This is useful when the output will be viewed with a pager like delta that supports its
own `-U` flag for controlling displayed context, and `n`/`N` navigation between
walkthrough comments.

The script:
- Constructs the output diff with walkthrough comments interleaved
- Validates that every `+`/`-` line appears exactly once (the coverage invariant)
- Validates hunk header line counts are correct
- Exits with an error if anything is wrong — fix the manifest and rerun

### 5. Present the result

Tell the user the walkthrough diff location and introduce it with a gentle, reasonably
comprehensive overview before summarizing the mechanics.

Your presentation should usually include:
- A short introductory paragraph that explains the user-visible goal of the branch and
  the main challenge it had to solve.
- A concise narrative-arc summary: how many steps there are, what the major sections
  cover, and what the reader will learn by following them.

Avoid dropping straight into file lists or step counts with no framing. The reader should
understand the "why" before they start reading the diff.
