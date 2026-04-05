---
name: code-walkthrough
description: |
  Explain how some code feature or PR/diff/branch works by adding numbered comments
  and then creating a diff to present them (a "walkthrough").
---

When the user asks you to use comments to explain how some code works, or how a PR/diff works,
follow these steps:

1. Study the relevant code or code change thoroughly. When you have understood it, add a sequence of
   numbered commments to the code "walking them through" the change. Choose the comments so that if
   the user reads them in order they form a coherent sequential narrative explaining the feature or
   PR/diff to them. Start each comment with [WALKTHROUGH <i/N>].

2. Use `git diff -U99 > $tempfile` to capture a diff containing your walkthrough comments

3. Rearrange that diff so that it presents the diff hunks in walkthrough sequence, ensuring that the
   final result is still valid git diff format. When one file contains multiple walkthrough comments
   then (unless they happen to be consecutive) you'll have to copy the file header to accompany the
   different diff hunks in their reordered location. If the diff context in one walkthrough hunk
   happened to capture other walkthrough comments, remove them from that diff hunk (they'll appear
   in their own).


Finally, tell the user the location of the final walkthrough diff.
