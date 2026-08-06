---
name: agent-sessions
description: >-
  Find and resume past work done with coding agents. Use when the user refers to
  something they did before — "the conversation where we…", "what did I decide
  about…", "pick up where I left off on…" — or asks how much context a piece of
  work used, where it branched, or what they said in it.
---

# agent-sessions

Finds past sessions with coding agents — Claude Code and others — and resumes
them.

Output adapts to the caller: you will get TSV with nothing truncated, and full
ids and timestamps. Add `--json` for a structured payload, `-q` for bare ids to
pipe. Hints and errors go to stderr; only data goes to stdout.

Exit codes: 0 found something, 1 found nothing, 2 you called it wrong.

## Typical use

    agent-sessions search "worktree relocation" -p wormhole   # find it
    agent-sessions show <id> --turns                          # read what was said
    agent-sessions resume <id>                                # pick it back up

Ids round-trip: whatever `search` prints is accepted by every other command,
and any unambiguous prefix will do — `agent-sessions show 7daeb` is enough.

## Worth knowing

- Every command prints the next one to run, with the id filled in. Follow it
  rather than spending a call on `--help`.
- Matching is case-insensitive and stemmed: `relocate` finds "relocating".
- Tool calls and their output are not indexed, so `search` matches what was
  said, not what was run. Use `agent-sessions cat <id> --tools` to see commands.
- Context size is the peak the session reached, not a sum of its turns.
- The index is a cache over transcript files, refreshed by `agent-sessions sync`.
  Do not sync unprompted: it is the user's call, and results are usually fine
  without it.

## Commands

### `agent-sessions agent [PROMPT]`

Start a coding agent that already knows this tool.

- `--with` — Which coding agent to start.
- `--model` — Which model it should run, named as that agent names it.

```
$ agent-sessions agent                                    # pi, knowing this tool
$ agent-sessions agent --with qwen
$ agent-sessions agent --model anthropic/claude-opus-5
$ agent-sessions agent "pick up the compaction work"      # your own first task
```

### `agent-sessions cat ID`

Print a session as markdown, read from the transcript itself.

- `--tools` — Include tool calls and their output.
- `--whole` — Include branches that were abandoned.

### `agent-sessions ls`

List sessions, most recent first. No text matching; use `search` for that.

- `-p, --project` — Only this wormhole project, tasks included.
- `--agent` — Only this agent.
- `--since` — Only agent-sessions touched within e.g. 36h, 10d, 2w.
- `--min-context` — Only agent-sessions whose context reached e.g. 500k.
- `-n, --limit` — How many at most.
- `--sort` — Order by recency, peak context, or number of turns.

### `agent-sessions resume ID`

Pick a session back up, in the worktree it belongs to.

- `--fork` — Branch into a new session, leaving this one as it is.

### `agent-sessions search QUERY`

Find agent-sessions whose text matches QUERY. Best match first, one per line.

- `-p, --project` — Only this wormhole project, tasks included.
- `--agent` — Only this agent.
- `--since` — Only agent-sessions touched within e.g. 36h, 10d, 2w.
- `--min-context` — Only agent-sessions whose context reached e.g. 500k.
- `-n, --limit` — How many at most.

```
$ agent-sessions search compaction                    # case-insensitive, and stemmed:
                                                # matches Compaction, compacted
$ agent-sessions search "worktree relocation"         # both words, in any order
$ agent-sessions search '"worktree relocation"'       # the exact phrase
$ agent-sessions search 'nexus OR chasm'              # either
$ agent-sessions search 'activity NOT workflow'       # one but not the other
$ agent-sessions search 'reloc*'                      # prefix of the STEM: relocat*
                                                # would find nothing
$ agent-sessions search compaction -p temporal --since 2w
$ agent-sessions search compaction --min-context 500k -n 5
$ agent-sessions search compaction -q | head -1       # bare id, to pipe
```

### `agent-sessions show ID`

Show one session and the history of my turns in it.

- `--turns` — Just my turns, without the header.

### `agent-sessions skills`

Manage the agent-sessions skill, so an agent knows this tool from turn one.

### `agent-sessions status`

Report index health: session counts, and whether a sync is due.

### `agent-sessions sync`

Bring the index into line with the transcript files. Safe to re-run.

- `--agent` — Only read this agent's transcripts. Repeatable. Defaults to all.

### `agent-sessions tree ID`

Show where a session branched, where it was compacted, and what forked off it.
