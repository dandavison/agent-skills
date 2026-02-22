# Magit Staging Internals

Research document covering magit's complete API surface for staging operations
and the precise git commands used to implement each one.

Source: [magit](https://github.com/magit/magit) at `~/tmp/3p/magit`.

## Architecture overview

Magit's staging is layered:

1. **Selection layer** — determines what to operate on from the buffer state
   (point position, active region, section tree)
2. **Dispatch layer** — `magit-stage`/`magit-unstage` dispatch by `(diff-type, diff-scope)`
   to the appropriate apply function
3. **Apply layer** — `magit-apply-{region,hunk,hunks,diff,diffs}` construct a patch string
4. **Patch layer** — `magit-apply-patch` pipes the patch to `git apply` via stdin
5. **Process layer** — `magit-run-git-with-input` sends buffer contents to git via
   `call-process-region`

All patch-based operations ultimately execute:

```
git apply [--cached] [--reverse] [--index] [--3way] [--reject] \
    -p0 -C<N> --ignore-space-change -
```

where `-` means "read patch from stdin", `-p0` because magit uses `--no-prefix` in its diffs
(so paths have no `a/`/`b/` prefix), and `-C<N>` is the context level (default 3, from
`diff.context` or `-U<N>` in diff args).


## Selection layer

### `magit-diff-type` → how the diff was produced

Determines whether the current section shows staged, unstaged, or committed changes.

| Buffer mode | Section context | Return value |
|---|---|---|
| `magit-status-mode` | Under `staged` heading | `staged` |
| `magit-status-mode` | Under `unstaged` heading | `unstaged` |
| `magit-status-mode` | Under `untracked` heading | `untracked` |
| `magit-diff-mode` | `--cached` in typearg | `staged` |
| `magit-diff-mode` | No `--cached`, HEAD-like range | `unstaged` |
| `magit-diff-mode` | Range contains `..` | `committed` |
| `magit-revision-mode` | Any | `committed` |

For hunks, the type comes from the grandparent section (hunk → file → staged/unstaged).

### `magit-diff-scope` → granularity of the selection

| Section type | Region active? | Siblings selected? | Return value |
|---|---|---|---|
| `hunk` | Yes, inside body | No | `region` |
| `hunk` | No | No | `hunk` |
| `hunk` | — | Yes | `hunks` |
| `file` | — | No | `file` |
| `file` | — | Yes | `files` |
| `staged`/`unstaged` | — | — | `list` |

### `magit-apply--get-selection` → section objects to operate on

Returns `magit-section` object(s) from point/region. Uses `magit-region-sections`
(multiple siblings selected) or `magit-current-section` (single section at point).
For `staged`/`unstaged` parent sections, returns all children.


## Staging operations

### Stage file(s)

**Entry**: `magit-stage` (interactive), `magit-stage-files` (interactive),
`magit-stage-modified` (interactive), `magit-file-stage` (from file buffer).

**Implementation**: `magit-stage-1 (arg &optional files)`

**Git command**:
```
git add <arg> -- <files>
# or, if no files:
git add <arg> .
```

Where `<arg>` is one of:
- (empty) — stage specific files
- `-u` — stage all tracked modified files
- `--all` — stage all files including untracked
- `--force` — stage ignored files

### Stage hunk

**Entry**: `magit-stage` when scope is `hunk` and type is `unstaged`.

**Implementation**: `magit-apply-hunk (hunk "--cached")`

**Patch construction**:
```
<file-header>
<hunk-content, possibly with adjusted @@ new-start>
```

`file-header` = the `--- file\n+++ file\n` header stored on the parent file section.
For renames, uses the original (pre-rename) path.

`hunk-content` = raw text of the hunk from the magit buffer (`buffer-substring-no-properties`
from section `start` to section `end`).

**New-start adjustment** (`magit-apply--adjust-hunk-new-start`): When applying a hunk that
isn't the first hunk in the file, the `+N` in the `@@ -M,L +N,L @@` header reflects
preceding hunks that may not be staged. The adjustment computes:
```
offset = new_start - old_start   (from the first hunk being applied)
adjusted_new_start = original_new_start - offset
```
This makes the hunk apply correctly against the current index regardless of what other
hunks exist.

**Git command**:
```
git apply --cached -p0 -C3 --ignore-space-change -
```
Patch on stdin.

### Stage multiple hunks

**Entry**: `magit-stage` when scope is `hunks` (region spans sibling hunks in same file).

**Implementation**: `magit-apply-hunks (hunks "--cached")`

**Patch construction**:
```
<file-header>
<hunk-1-content>
<hunk-2-content>
...
```

All hunks are from the same file. `magit-apply--adjust-hunk-new-starts` adjusts all
hunk headers relative to the first selected hunk.

**Git command**: Same as single hunk.

### Stage region (individual lines within a hunk)

**Entry**: `magit-stage` when scope is `region` and type is `unstaged`.

**Implementation**: `magit-apply-region (hunk "--cached")`

**Patch construction**: `magit-diff-hunk-region-patch` builds a modified hunk containing
only the selected lines.

**Algorithm** (forward staging, `op = "-"`):

For each line in the hunk (including the `@@` header):
| Line starts with | Line in region? | Action |
|---|---|---|
| `@@` | — | Keep (header) |
| ` ` (space) | — | Keep (context) |
| `+` | Yes | Keep (addition to stage) |
| `+` | No | **Drop** (addition not selected) |
| `-` | Yes | Keep (deletion to stage) |
| `-` | No | **Convert to context** (replace `-` with ` `) |

For reverse operations (unstaging), `op = "+"` and the roles of `+`/`-` are swapped:
| Line starts with | Line in region? | Action |
|---|---|---|
| `@@` | — | Keep |
| ` ` (space) | — | Keep |
| `-` | Yes | Keep |
| `-` | No | **Drop** |
| `+` | Yes | Keep |
| `+` | No | **Convert to context** |

After constructing the line list, magit calls Emacs's `diff-fixup-modifs` to recalculate
the `@@ -M,L +N,L @@` header line counts. Then `magit-apply--adjust-hunk-new-start`
adjusts the new-start as for whole hunks.

**Git command**: Same as single hunk.

### Stage untracked files

**Entry**: `magit-stage` when type is `untracked`, or `magit-stage-untracked`.

**Implementation**: `magit-stage-untracked`

**Git command**:
```
git add [--intent-to-add] -- <files>
```

For submodule directories, may instead call `magit-submodule-add-1` (which runs
`git submodule add`).


## Unstaging operations

### Unstage file(s)

**Entry**: `magit-unstage` (interactive), `magit-unstage-files` (interactive),
`magit-unstage-all` (interactive), `magit-file-unstage` (from file buffer).

**Implementation**: `magit-unstage-1 (files)`

**Git command**:
```
# Normal (HEAD exists):
git reset HEAD -- <files>

# Initial commit (no HEAD):
git rm --cached -- <files>
```

### Unstage hunk / hunks / region

**Entry**: `magit-unstage` when scope is `hunk`/`hunks`/`region` and type is `staged`.

**Implementation**: Same apply functions as staging, but with `"--reverse" "--cached"`:
- `magit-apply-region (hunk "--reverse" "--cached")`
- `magit-apply-hunk (hunk "--reverse" "--cached")`
- `magit-apply-hunks (hunks "--reverse" "--cached")`

**Git command**:
```
git apply --reverse --cached -p0 -C3 --ignore-space-change -
```

The `--reverse` flag inverts the patch, effectively removing changes from the index.
Region patch construction uses `op = "+"` (swapped roles, see region staging above).


## Discard operations

### Discard region / hunk / hunks

**Entry**: `magit-discard` when scope is `region`/`hunk`/`hunks`.

**Implementation**: `magit-discard-apply` calls the appropriate apply function.

**Git commands** depend on whether changes are staged or unstaged:

| State | Git commands |
|---|---|
| Unstaged only | `git apply --reverse -p0 -C<N> --ignore-space-change -` |
| Staged, no unstaged in file | `git apply --reverse --index -p0 -C<N> --ignore-space-change -` |
| Staged, with unstaged in file | `git apply --reverse --cached ...` then `git apply --reverse --reject ...` |

The `--index` flag applies to both index and working tree atomically.
The two-step cached+reject approach unstages first, then discards from the working tree
(with `--reject` to handle potential conflicts with unstaged changes).

### Discard file(s)

**Entry**: `magit-discard` when scope is `file`/`files`/`list`.

**Git commands** depend on file state:

| File state | Git command |
|---|---|
| Untracked | `delete-file` (or trash) |
| Modified (unstaged) | `git checkout -- <file>` |
| Deleted | `git checkout -- <file>` |
| Staged, no unstaged | `git checkout HEAD -- <file>` or `git apply --reverse --index` |
| Staged, with unstaged | `git apply --reverse --cached` + `git apply --reverse --reject` then `git checkout -- <file>` |
| Renamed | `git mv <new> <old>` to undo rename |
| Conflict | `git checkout --ours\|--theirs\|--merge -- <file>` |


## Reverse operations

Reverse applies a committed or staged change in reverse to the working tree.

**Entry**: `magit-reverse` (interactive, with optional `--3way` prefix).

**Implementation**: `magit-reverse-apply` calls the appropriate apply function with
`"--reverse"` and optionally `"--reject"` (when not atomic and not `--3way`).

**Git command**:
```
git apply --reverse [--reject] [--3way] -p0 -C<N> --ignore-space-change -
```

Can only reverse staged or committed changes. Cannot reverse untracked or unstaged.


## Patch construction details

### File header

`magit-diff-file-header (section)` returns the stored `header` slot from the file section.
This is the raw git diff header captured during `magit-diff-wash-diff`:

```
diff --git file file
--- file
+++ file
```

Note: paths have no `a/`/`b/` prefix because magit always passes `--no-prefix` to
`git diff`. This is why `magit-apply-patch` uses `-p0` (strip zero path components).

For renames, the header includes `rename from`/`rename to` lines. The `no-rename`
parameter to `magit-diff-file-header` replaces the original path with the current path
when the rename header should not be preserved.

### Hunk new-start adjustment

When applying a subset of hunks from a file, the `+N` (new-file start line) in each
hunk's `@@` header is based on the assumption that all preceding hunks are also applied.
If preceding hunks are skipped, the new-start must be adjusted.

`magit-apply--adjust-hunk-new-starts` computes:
```
offset = first_hunk.new_start - first_hunk.old_start
```
Then for each hunk:
```
adjusted_new_start = hunk.new_start - offset
```

This works because the offset represents the cumulative line count change from all
preceding (skipped) hunks.

### Region patch line counts

After constructing a partial-hunk patch (with some lines dropped or converted to context),
the `@@ -M,L +N,L @@` header's line counts are wrong. Magit delegates to Emacs's
`diff-fixup-modifs` to recalculate them. This function counts the actual `-`, `+`, and
` ` lines in the patch and updates the header accordingly.

Equivalent logic for a Python implementation:
```
old_count = count of lines starting with ' ' or '-'
new_count = count of lines starting with ' ' or '+'
```
Then update `@@ -M,<old_count> +N,<new_count> @@`.


## Process layer

### `magit-run-git-with-input`

The workhorse for all patch application. Uses the current buffer's content as stdin:

```elisp
(with-temp-buffer
  (insert patch)
  (magit-run-git-with-input "apply" args "-p0" ...))
```

Internally calls:
```elisp
(call-process-region (point-min) (point-max)
                     git-executable nil process-buf nil flat-args)
```

This sends the buffer content to git's stdin and captures output in the process buffer.

### Working directory

All git commands run in `default-directory`. Magit uses `magit-with-toplevel` to
ensure this is the repository root. `magit-toplevel` finds the root via
`git rev-parse --show-toplevel` (with caching).

### Error handling

`magit-apply-patch` does not raise on failure. `magit-run-git-with-input` returns
the exit code, which `magit-process-finish` logs to the process buffer.
Non-zero exits show a message in the echo area and set `magit-this-error`.

When `--reject` is used, `git apply` writes `.rej` files for failed hunks rather
than failing entirely.


## Summary: git commands by operation

| Operation | Scope | Git command |
|---|---|---|
| Stage | file | `git add -- <files>` |
| Stage | hunk/hunks/region | `git apply --cached -p0 -C<N> --ignore-space-change -` |
| Stage | all modified | `git add -u .` |
| Stage | untracked | `git add -- <files>` |
| Unstage | file | `git reset HEAD -- <files>` |
| Unstage | file (no HEAD) | `git rm --cached -- <files>` |
| Unstage | hunk/hunks/region | `git apply --reverse --cached -p0 -C<N> --ignore-space-change -` |
| Unstage | all | `git reset HEAD -- .` |
| Discard | file (unstaged) | `git checkout -- <files>` |
| Discard | file (staged only) | `git apply --reverse --index ...` or `git checkout HEAD -- <files>` |
| Discard | file (staged+unstaged) | `git apply --reverse --cached ...` then `--reverse --reject ...` |
| Discard | hunk/region (unstaged) | `git apply --reverse -p0 ...` |
| Discard | hunk/region (staged only) | `git apply --reverse --index -p0 ...` |
| Discard | untracked | `rm` / `trash` |
| Discard | conflict | `git checkout --ours\|--theirs\|--merge -- <file>` |
| Reverse | hunk/hunks/region | `git apply --reverse [--reject] -p0 ...` |
| Reverse | file | `git apply --reverse [--reject] -p0 ...` |


## Implications for a Python reimplementation

The core staging plumbing is simple:
1. Parse `git diff [--cached] --no-prefix` output into file headers and hunks
2. For hunk staging: concatenate file header + hunk content, pipe to
   `git apply --cached -p0 -C3 --ignore-space-change -`
3. For line staging: edit the hunk to drop/convert unselected lines,
   fix the `@@` header counts, then apply as above
4. For multi-hunk staging: adjust new-start offsets, concatenate, apply
5. For unstaging: same patches with `--reverse --cached`

Key details to preserve:
- **`-p0`**: Use `--no-prefix` when running `git diff` so paths are bare
- **`-C<N>`**: Default to `-C3`; can reduce to `-C0` if whitespace-insensitive
- **`--ignore-space-change`**: Always include for robustness
- **New-start adjustment**: Required when applying non-first hunks from a file
- **`diff-fixup-modifs` equivalent**: Required when constructing partial-hunk patches
  (recalculate line counts from actual patch content)
