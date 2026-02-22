---
name: git-split atomic commits
overview: "Build a `git-split` skill: a Python CLI that reimplements magit's staging plumbing (file, hunk, and line-level staging via `git apply --cached -p0`) with a SKILL.md that teaches agents the iterative stage-commit workflow for producing clean atomic commit histories."
todos:
  - id: cli-core
    content: "Implement git-stage CLI: diff parsing with unidiff, patch construction (file/hunk/line granularity), git apply --cached -p0 plumbing, following magit's patterns from research-magit.md"
    status: pending
  - id: skill-md
    content: Write SKILL.md with agent workflow instructions and atomic commit guidance
    status: pending
  - id: tests
    content: "Tests: unit (diff parsing, partial-hunk patch construction, @@ header fixup) and integration (temp git repo staging at all three granularities)"
    status: pending
  - id: verify
    content: "End-to-end test: make multi-file changes, use git-stage to split into atomic commits with line-level precision"
    status: pending
isProject: false
---

# git-stage: File, Hunk, and Line-Level Staging for AI Agents

Based on exhaustive research of magit's internals: [research-magit.md](git-stage/docs/research-magit.md).

## Problem

AI agents produce changes and commit them as one blob. No existing tool lets agents reason
about their diff and split it into multiple atomic commits the way a developer would with
magit or `git add -p`.

## Design

**Reimplement magit's staging plumbing in Python.** Magit's five-layer architecture
(selection, dispatch, apply, patch, process) reduces to simple git commands at the bottom.
The agent replaces magit's interactive selection layer; a Python CLI replaces the rest.

The core git command (for all hunk/line operations) is:

```
git apply --cached -p0 -C3 --ignore-space-change -
```

with patch on stdin. This is exactly what magit calls (`magit-apply-patch` in
`magit-apply.el`). The `-p0` is because we use `--no-prefix` diffs (bare paths,
no `a/`/`b/`), matching magit's convention.

Three granularities, matching magit:

- **File**: `git add -- <files>` (trivial, but included for completeness)
- **Hunk**: construct patch = file header + hunk content, pipe to `git apply --cached`
- **Line**: construct partial-hunk patch using magit's region algorithm, fix `@@` counts,
pipe to `git apply --cached`

## CLI: `git-stage/scripts/git-stage`

uv-runnable Python script. Dependency: `unidiff`.

### Subcommands

`**git-stage diff`** -- Show all unstaged changes as numbered hunks with line sub-IDs.

Runs `git diff --no-prefix` and parses with `unidiff`. Output format:

```
File: src/auth.py

  Hunk 1 @@ -45,5 +45,8 @@ def authenticate(user)
       1.1  |      if not user.token:
       1.2  |          raise AuthError("no token")
       1.3 +|      if user.token.expired:
       1.4 +|          user.token = refresh_token(user)
       1.5  |      return validate(user.token)

  Hunk 2 @@ -78,3 +81,5 @@ def refresh_token(user)
       2.1  |      token = generate_token(user)
       2.2 +|      log.info("refreshed token for %s", user.id)
       2.3  |      return token

File: src/api/routes.py

  Hunk 3 @@ -12,3 +12,8 @@ from .handlers import ...
       3.1  |  ...
```

Each changed line (+ or -) gets a sub-ID like `1.3`. Context lines are shown but only
changed lines are addressable. This gives the agent enough information to reason about
what each line does and decide on groupings.

`**git-stage stage <spec> [<spec>...]**` -- Stage changes by ID.

Spec format:

- `3` -- stage entire hunk 3
- `1.3,1.4` -- stage lines 3 and 4 of hunk 1 (line-level)
- `1,3` -- stage entire hunks 1 and 3
- `1.3,1.4,3` -- stage lines 3-4 of hunk 1 and all of hunk 3

For each file touched by the selection, constructs a patch:

1. File header (`--- file\n+++ file\n`)
2. For whole-hunk specs: raw hunk content with new-start adjustment
3. For line-level specs: partial-hunk patch using magit's region algorithm

**Patch construction for line-level staging** (from `magit-diff-hunk-region-patch`):

For each line in the hunk:


| Line type     | Selected? | Action                                   |
| ------------- | --------- | ---------------------------------------- |
| `@@` header   | --        | Keep                                     |
| Context ( ``) | --        | Keep                                     |
| `+` line      | Yes       | Keep                                     |
| `+` line      | No        | Drop entirely                            |
| `-` line      | Yes       | Keep                                     |
| `-` line      | No        | Convert to context (replace `-` with ``) |


Then recalculate `@@` header counts:

```
old_count = lines starting with ' ' or '-'
new_count = lines starting with ' ' or '+'
```

Then apply new-start adjustment if this isn't the first hunk in the file (magit's
`magit-apply--adjust-hunk-new-starts` algorithm):

```
offset = first_selected_hunk.new_start - first_selected_hunk.old_start
each hunk: adjusted_new_start = hunk.new_start - offset
```

`**git-stage unstage [<spec>...]**` -- Unstage changes.

Without args: `git reset HEAD` (unstage everything).
With specs: construct patch from `git diff --cached --no-prefix` and apply with
`--reverse --cached` (magit's unstage-hunk/region pattern).

`**git-stage status**` -- Summary of current state.

Shows count of unstaged hunks/files and staged hunks/files. Helps the agent track
progress through the splitting workflow.

### Internal architecture

```
parse_diff(diff_text) -> list[FileDiff]
  FileDiff: path, header, hunks: list[Hunk]
  Hunk: id, header, lines: list[Line]
  Line: sub_id, type (+/-/ ), content

build_patch(file_header, hunk_content) -> str
build_partial_patch(hunk, selected_line_ids) -> str   # magit region algorithm
adjust_new_starts(hunks) -> list[str]                  # magit offset algorithm
fixup_counts(hunk_text) -> str                         # diff-fixup-modifs equivalent

apply_to_index(patch_text, reverse=False) -> None
  # subprocess: git apply [--reverse] --cached -p0 -C3 --ignore-space-change -
```

## Skill: `git-stage/SKILL.md`

Operational instructions for the tool, not commit policy (that belongs in the user's
AGENTS.md):

1. Ensure all changes are unstaged (`git-stage unstage` if needed)
2. Run `git-stage diff` to see all changes with hunk and line IDs
3. For each group to stage:
  - `git-stage stage <specs>`
  - `git commit -m "<message>"`
4. **Re-run `git-stage diff` after each commit** -- hunk IDs are reassigned from the
  fresh diff. Always work from the live diff state.

## Edge cases

- **New untracked files**: `git add -N <file>` first (intent-to-add), then hunks appear in
`git diff`. Matches magit's `magit-stage-untracked` with `--intent-to-add`.
- **Deleted files**: Entire file is one hunk (all `-` lines).
- **Binary files**: Skip with a note (magit also skips binary for hunk operations).
- **Renamed files**: Preserve rename header in patch. Use `--no-renames` or detect and handle.
- **Combined/merge hunks**: Reject with error (magit does: "Cannot un-/stage resolution
hunks. Stage the whole file").
- **Empty diff**: Exit cleanly.
- **Staging failure**: Report git apply's stderr. Consider `--reject` fallback for partial
application (magit uses this for discard of staged changes with unstaged conflicts).

## Testing

Unit tests:

- Diff parsing: feed known diffs, verify hunk/line extraction
- Partial-hunk patch construction: select specific lines, verify output matches expected patch
- `@@` header fixup: verify line counts are recalculated correctly
- New-start adjustment: verify offset calculation for non-first hunks

Integration tests (temp git repo):

- Stage single hunk, verify `git diff --cached` matches
- Stage multiple hunks from same file, verify
- Stage individual lines from a hunk, verify
- Stage mix of whole hunks and lines, verify
- Unstage specific hunks/lines, verify
- Full workflow: stage group A, commit, stage group B, commit, verify git log

## File structure

```
git-stage/
  SKILL.md
  docs/
    research-magit.md   # (already written)
  scripts/
    git-stage            # uv-runnable Python script
  tests/
    test_git_stage.py    # pytest tests
```

