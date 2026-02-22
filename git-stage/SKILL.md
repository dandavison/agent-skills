---
name: git-stage
description: |
  Hunk and line-level git staging for splitting changes into atomic commits.
  Reimplements magit's staging plumbing (git apply --cached -p0) in Python.
  Use when:
  - Splitting working tree changes into multiple commits
  - Staging specific hunks or individual lines
  - Producing clean, reviewable commit histories
  Triggers: "split commits", "atomic commits", "stage hunks", "stage lines",
  "git-stage", "selective staging", "split changes"
---

# git-stage

Hunk and line-level git staging via `git apply --cached -p0`, following magit's
plumbing patterns.

The script is at: `~/.cursor/skills/git-stage/scripts/git-stage`

## Commands

```bash
# Show unstaged changes as numbered hunks with line sub-IDs
git-stage diff

# Show staged changes
git-stage diff --cached

# Stage entire hunks
git-stage stage 1 3

# Stage individual lines within a hunk
git-stage stage 1.3,1.4

# Mix whole hunks and lines
git-stage stage 1.2,1.3 3

# Unstage everything
git-stage unstage

# Unstage specific hunks or lines
git-stage unstage 2 1.5,1.6

# Summary of staged/unstaged state
git-stage status
```

## Workflow

1. Ensure all changes are unstaged (`git-stage unstage` if needed).
2. Run `git-stage diff` to see all changes with hunk and line IDs.
3. For each group to stage:
   - `git-stage stage <specs>`
   - `git commit -m "<message>"`
4. Re-run `git-stage diff` after each commit — hunk IDs are reassigned from
   the fresh diff. Always work from the live diff state.

## Output format

`diff` output numbers each hunk and assigns sub-IDs to changed lines:

```
File: src/auth.py

  Hunk 1 @@ -45,5 +45,8 @@ def authenticate(user)
            |     if not user.token:
       1.2 -|         raise AuthError("no token")
       1.3 +|         raise AuthError("missing token")
       1.4 +|         log.warning("auth failed for %s", user.id)
            |     return validate(user.token)
```

Context lines have no ID. Only changed lines (`+`/`-`) are addressable.

## Spec format

- `3` — entire hunk 3
- `1.3,1.4` — lines 3 and 4 of hunk 1
- `1,3` — entire hunks 1 and 3
- `1.3,1.4,3` — lines from hunk 1 and all of hunk 3
