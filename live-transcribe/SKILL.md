---
name: live-transcribe
description: |
  Live meeting transcription with speaker diarization. Start/stop transcription,
  monitor what's being said in real-time, identify speakers, and search past
  transcripts. Use when:
  - Starting or stopping a live transcription session
  - Monitoring what's being said in a meeting
  - Identifying or labeling speakers in a transcript
  - Searching past meeting transcripts
  Triggers: "transcribe meeting", "start transcription", "live transcript", "meeting audio",
  "what's being said", "monitor meeting", "identify speakers", "label speakers",
  "search transcripts", "past meetings", "what was said"
---

# Live Transcribe

Tools live at `~/src/audio-filter`. All commands use `uv run` from that directory.

## Start transcription

```bash
cd ~/src/audio-filter
uv run transcribe --title "Session Name" --listen
```

- `--listen`: pass audio through to speakers (omit for silent capture)
- `--input "blackhole+speakers"`: use a specific aggregate device
- Requires BlackHole as system audio output (or an aggregate device containing it)
- Requires `HF_TOKEN` env var for pyannote diarization models

Only one transcription can run at a time (enforced via PID file at
`~/meetings/.transcribe.pid`).

## Monitor (read live transcript)

During a session, the live transcript is at `~/meetings/live.txt`:

```bash
cat ~/meetings/live.txt        # Full transcript so far
tail -20 ~/meetings/live.txt   # Last 20 lines
```

Or read the file directly using the Read tool. Format:
```
[00:01:23] Speaker 1: Good morning everyone...
[00:01:35] Speaker 2: Hey, so the main issue was...
```

To track incrementally, note the last line number read and read from there next time.

## Stop transcription

Send Ctrl+C to the terminal, or:

```bash
kill $(cat ~/meetings/.transcribe.pid)
```

On stop, a full-meeting diarization pass runs and the final transcript is saved to
SQLite at `~/meetings/transcripts.db`.

## Identify speakers

After some audio has been captured (or after the session ends):

```bash
cd ~/src/audio-filter
uv run transcript-search speakers <session-id-or-title>
```

This shows each speaker with sample utterances. Then label them:

```bash
uv run transcript-search label <session> "Speaker 1" "Alice"
uv run transcript-search label <session> "Speaker 2" "Bob"
```

Labels apply retroactively to the stored transcript.

## Search past transcripts

```bash
cd ~/src/audio-filter
uv run transcript-search list                           # Recent sessions
uv run transcript-search search "OOM" --after 2026-01-01  # Keyword search
uv run transcript-search get <session-id-or-title>      # Full transcript
```

## Integration with assemble-context

`transcript-search` can serve as a source for context assembly. To search meeting
transcripts for a topic:

```bash
cd ~/src/audio-filter && uv run transcript-search search "topic keywords"
```

Then fetch the full transcript of relevant sessions with `transcript-search get`.
