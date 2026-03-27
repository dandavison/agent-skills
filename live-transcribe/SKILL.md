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
uv run transcribe --title "Session Name"
```

- `--listen`: pass audio through to speakers. **Only use this if the user is NOT
  already hearing the meeting audio** (e.g. via headphones or speakers). If they
  are, `--listen` causes echo/reverb. Omit it by default.
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

## Live meeting companion mode

When the user asks you to follow a meeting in real-time and give running summaries,
use this procedure:

### Setup
1. Start transcription (see above). Do NOT use `--listen` sicne the user will be
   hearing the meeting audio through headphones/speakers and it would cause echo.
2. Note the initial line count of `~/meetings/live.txt` (may be 0).

### Polling loop
1. Launch a background Bash command: `sleep 60 && wc -l ~/meetings/live.txt`
   (use `run_in_background: true`). This is your timer.
2. When the timer completes, use the Read tool to read `~/meetings/live.txt`
   from your last-read offset to the end.
3. Output a **concise text summary** of the new content to the user. Focus on:
   - Who is speaking and what topic they're on
   - Key decisions, announcements, or questions raised
   - Notable transitions (new presenter, new topic)
4. Update your offset to the new line count.
5. Go to step 1 (launch the next timer).

### UX principles
- **Minimize visible tool calls.** The user does not want to see a stream of
  tool invocations. Use one background timer + one Read per cycle.
- **Stay responsive.** If the user asks a question between polls, do a fresh
  Read to catch up, answer their question, then resume the polling loop.
- **Summaries, not transcripts.** Output 3-6 sentences per minute of content.
  Lead with the speaker and topic. Skip filler, false starts, and "um/uh".
- The transcription process may outlive background command timeouts — that's
  fine. Check `ps -p $(cat ~/meetings/.transcribe.pid)` to verify it's alive
  if you suspect it stopped.

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
