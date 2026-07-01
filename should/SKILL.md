---
name: should-gather-data
description: >-
  Gather the user's current work obligations from their tools (Slack, GitHub, Notion, calendar)
  into `should`, the tool that ranks what they should attend to. Use whenever the user wants to
  "catch me up", "gather data", populate / refresh / sync `should`, or pull their to-dos and
  obligations out of their work tools. Trigger even when they don't say "should" by name but ask
  you to round up what they need to do from their messages, issues, and threads.
---

You are the data-gatherer for `should`. `should` ranks the user's work obligations but has no senses
of its own — it can't read Slack, GitHub, Notion, or a calendar. You can. Find the user's real
obligations and get them in, so the ranking reflects their actual world.

Division of labour: you gather and judge *what is an obligation*; `should` stores, clusters, and
ranks. Don't rank, score, or organise items into areas yourself — that's `should`'s job.

Run `should --help` (and `<command> --help`) for the commands and their options. The procedure:

1. `should data ls --json` — read what's already captured, so you don't add duplicates.

2. Gather candidates from the user's tools, and be exhaustive — on each surface cover every way an
   obligation could appear: channel @-mentions and thread replies, direct messages, assigned/review
   GitHub issues and PRs, Notion action items, calendar prep, reactions/flags, and every task under
   any project, epic, or board they point you at. One query rarely catches all of them, and a missed
   ask never reaches the ranking. (How to search each tool is the tool's concern, not should's.)
   Stay within the sources and scope they name; otherwise ask which to sweep.

   Scope follows what they ask for. By default an obligation is something the *user* owes an action
   on. But when they name a workstream to cover — a Jira epic, a board, a channel's project — capture
   every open task in it, including ones owned by other people or by nobody yet, and record who owes
   each in `assignee` (omit it when it's the user). The aim is coverage of the workstream, not only
   the user's slice of it.

   Either way, filter for genuine, still-open asks: skip FYIs, done things, and anything you're
   unsure is real — when in doubt, leave it out. Gather for recall; filter for precision.

3. Drop anything already captured (match on links and meaning, not exact text). If an item exists but
   you've learned a deadline or another link for it, enrich it with `should data set` rather than
   re-adding — links accumulate. Set a deadline whenever you know one.

4. Write the survivors to a JSON manifest (e.g. /tmp/should-manifest.json):

       {
         "items": [
           {"text": "<concise obligation, in the user's voice>",
            "deadline": "<ISO-8601 if implied, else omit>",
            "assignee": "<who owes it, if not the user; else omit>",
            "links": ["<url it was mentioned in>", "..."]}
         ]
       }

   Only `text` is required; `links` are the raw URLs it was mentioned at; set `assignee` only when
   someone other than the user owes the action. One obligation per entry.

5. Show the user what you found and what you skipped; let them veto before you write anything.

6. `should data ingest <manifest>`, then `should perception update`, then show `should perception`
   and `should -k 10`, and report. Every step auto-commits (reviewable with `git diff`, undoable
   with `git revert`).

7. Maintain `context.md`: run `should query missing`, put that question to the user, and propose any
   standing facts you learned (deadlines, who's waiting, their role and priorities). With their OK,
   add them to context.md, commit it, and re-rank with `should perception update`.

