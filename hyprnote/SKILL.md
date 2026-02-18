---
name: hyprnote
description: |
  Search and retrieve meeting transcripts from Hyprnote (local macOS app). Use when:
  - Looking up what was discussed in a meeting
  - Searching meeting transcripts by keyword
  - Retrieving a full meeting transcript
  - Finding meetings by date, title, or participant
  Triggers: "meeting transcript", "hyprnote", "what was discussed", "meeting notes transcript", "what did we talk about"
---

# Hyprnote meeting transcript search

Hyprnote stores transcripts in a local SQLite DB. Use the `hyprnote-search` script
to list, search, and retrieve them.

## Commands

```bash
# List recent sessions
hyprnote-search list --limit 20

# Search transcripts by keyword
hyprnote-search search "COGS" --after 2026-01-01 --before 2026-03-01 --limit 10

# Get full transcript (by UUID, partial UUID, or title substring)
hyprnote-search get "8d190e4d"
hyprnote-search get "oncall handoff"
```

The script is at: `~/.cursor/skills/hyprnote/scripts/hyprnote-search`

## Output format

- `list`: markdown with session id, title, date, participants, has-transcript flag
- `search`: matching sessions with keyword-in-context excerpts (up to 3 per session)
- `get`: full transcript with speaker labels (`**Speaker N**:` or `**Name**:`)

## Tips

- Transcripts can be very long (100K+ words). Pipe `get` output through summarization
  or grep for specific topics rather than reading the whole thing.
- Speaker labels are often `Speaker 1`, `Speaker 2` etc. unless assigned in Hyprnote.
- Search is case-insensitive substring matching over the word-level transcript text.
