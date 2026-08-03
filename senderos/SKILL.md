---
name: senderos
description: >-
  Find and resume past work done with coding agents. Use when the user refers to
  something they did before — "the conversation where we…", "what did I decide
  about…", "pick up where I left off on…" — or asks how much context a piece of
  work used, where it branched, or what they said in it.
---

# senderos

A *sendero* is one unit of work done with a coding agent: durable, branching,
resumable. `senderos` indexes them and finds them again.

Output adapts to the caller: you will get TSV with nothing truncated, and full
ids and timestamps. Add `--json` for a structured payload, `-q` for bare ids to
pipe. Hints and errors go to stderr; only data goes to stdout.

Exit codes: 0 found something, 1 found nothing, 2 you called it wrong.

## Typical use

    senderos search "worktree relocation" -p wormhole   # find it
    senderos show <id> --turns                          # read what was said
    senderos resume <id>                                # pick it back up

Ids round-trip: whatever `search` prints is accepted by every other command,
and any unambiguous prefix will do — `senderos show 7daeb` is enough.

## Worth knowing

- Every command prints the next one to run, with the id filled in. Follow it
  rather than spending a call on `--help`.
- Matching is case-insensitive and stemmed: `relocate` finds "relocating".
- Tool calls and their output are not indexed, so `search` matches what was
  said, not what was run. Use `senderos cat <id> --tools` to see commands.
- Context size is the peak the sendero reached, not a sum of its turns.
- The index is a cache over transcript files, refreshed by `senderos sync`.
  Do not sync unprompted: it is the user's call, and results are usually fine
  without it.

## Commands

### `senderos agent [PROMPT]`

Start a coding agent with the senderos skill loaded.

- `--with` — Which coding agent to start.

```
$ senderos agent                                    # pi, knowing this tool
$ senderos agent --with opencode
$ senderos agent "pick up the compaction work"      # with a first message
```

### `senderos cat ID`

Print a sendero as markdown, read from the transcript itself.

- `--tools` — Include tool calls and their output.
- `--whole` — Include branches that were abandoned.

### `senderos ls`

List senderos, most recent first. No text matching; use `search` for that.

- `-p, --project` — Only this wormhole project, tasks included.
- `--agent` — Only this agent.
- `--since` — Only senderos touched within e.g. 36h, 10d, 2w.
- `--min-context` — Only senderos whose context reached e.g. 500k.
- `-n, --limit` — How many at most.
- `--sort` — Order by recency, peak context, or number of turns.

### `senderos resume ID`

Pick a sendero back up, in the worktree it belongs to.

- `--fork` — Branch into a new session, leaving this one as it is.

### `senderos search QUERY`

Find senderos whose text matches QUERY. Best match first, one per line.

- `-p, --project` — Only this wormhole project, tasks included.
- `--agent` — Only this agent.
- `--since` — Only senderos touched within e.g. 36h, 10d, 2w.
- `--min-context` — Only senderos whose context reached e.g. 500k.
- `-n, --limit` — How many at most.

```
$ senderos search compaction                    # case-insensitive, and stemmed:
                                                # matches Compaction, compacted
$ senderos search "worktree relocation"         # both words, in any order
$ senderos search '"worktree relocation"'       # the exact phrase
$ senderos search 'nexus OR chasm'              # either
$ senderos search 'activity NOT workflow'       # one but not the other
$ senderos search 'reloc*'                      # prefix of the STEM: relocat*
                                                # would find nothing
$ senderos search compaction -p temporal --since 2w
$ senderos search compaction --min-context 500k -n 5
$ senderos search compaction -q | head -1       # bare id, to pipe
```

### `senderos show ID`

Show one sendero and the history of my turns in it.

- `--turns` — Just my turns, without the header.

### `senderos skills`

Manage the senderos skill, so an agent knows this tool from turn one.

### `senderos status`

Report index health: sendero counts, and whether a sync is due.

### `senderos sync`

Bring the index into line with the transcript files. Safe to re-run.

- `--agent` — Only read this agent's transcripts. Repeatable. Defaults to all.

### `senderos tree ID`

Show where a sendero branched, where it was compacted, and what forked off it.
