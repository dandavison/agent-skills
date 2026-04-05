---
name: code-walkthrough
description: |
  Explain how code, a feature, PR, diff, or branch works by adding numbered walkthrough
  comments and producing a reordered diff that reads as a coherent narrative. Use this skill
  whenever the user asks you to "walk through", "explain with comments", "annotate", or
  "create a walkthrough" for code, a PR, a diff, a branch, or a feature. Also use when the
  user wants a guided tour of how something works in the codebase.
---

I'm considering making a more formal guarantee in the case of PRs/branches/commits that the
walkthrough diff guarantees to "cover" the original diff, in the sense that if the reader reads
through each walkthrough comment with its surrounding context, by the end they are _guaranteed_ to
have read a superset of the actual diff. I think in this line of thinking it might make sense for
the llm to choose the context shown with each walkthrough comment. I think the resulting diff should
have the property that one never encounters "floating" diff content without first having read a
walkthrough comment; in other words each diff hunk should start with a walkthrough comment, even if
it (comment N) is just a brief intro to that area of code and is followed by a more substantial
comment (N+1) some lines later.

To state this differently and more formally: we are here restricting attention to the diff case, not
the "codebase feature" case.  Define a diff to be [file1, [file2, ...]] where fileN is [hunk1,
[hunk2, ...]]. The skill and python code must together essentially implement a function that takes
in a diff and outputs a diff. The output diff has the following properties:

1. A file may occur multiple times in the diff
2. Looking at the entire diff, the WALKTHROUGH comments are consecutively numbered and occur in order.
3. Each hunk is structured as a "walkthrough subsequence". A walkthrough subsequence contains a
   subsequence of the walkthrough comment sequence. It is a valid diff hunk structured as
   [walkthrough_subhunk1, [walkthrough_subhunk2, ...]]. A walkthrough subhunk always starts with
   some added lines for walkthrough comment i, followed by some real diff lines (additions or
   removals or both), followed optionally by some non-diff code context lines. The number of diff
   lines (and optional code context lines) following each walkthrough comment should
4. You should choose the number of lines of context _following_ each walkthrough comment on a
   semantic basis (lines that are reasonably relevant to understanding this walkthrough comment).
   You will need to strike a balance between on the one hand explaining related code in one
   walkthrough subsequence, and on the other hand recognizing where to stop and treat the ensuing
   code in a separate walkthrough subsequence.
5. The union of all diff lines in all walkthrough subhunks is equal to the set of diff lines in the
   original diff. This is non-negotiable and must be verified by the python code.

In other words, you have partitioned the input diff into semantically coherent sections and then
reordered them in narrative order, with the result remaining a valid diff.


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
