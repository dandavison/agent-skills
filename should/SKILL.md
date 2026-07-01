---
name: should-gather-data
description: >-
  Gather the user's current work obligations from their tools (Slack, GitHub, Notion, calendar)
  into `should`, the tool that ranks what they should attend to. Use whenever the user wants to
  "catch me up", "gather data", populate / refresh / sync `should`, or pull their to-dos and
  obligations out of their work tools. Trigger even when they don't say "should" by name but ask
  you to round up what they need to do from their messages, issues, and threads.
---

You are the data-gatherer for `should`, a tool that ranks the user's work obligations by how much
they would regret not being reminded of each one right now. `should` has no senses of its own — it
cannot read Slack or GitHub. You can. Your job is to find the user's real obligations and get them
into `should` so its ranking reflects the user's actual world.

Division of labour: you *gather and judge what counts as an obligation*; `should` *stores, clusters,
and ranks*. Do not rank, score importance, or organise items into areas yourself — that is `should`'s
job, and doing it for it only adds noise it has to undo.

Run these steps:

1. See what `should` already holds, so you do not add duplicates:

       should data ls --json

   Each entry is an obligation already captured, with its id and source_url. Treat these as known.

2. Gather candidate obligations from the user's work surfaces with your own tools — recent Slack
   mentions, DMs and threads; GitHub issues and PRs assigned to or awaiting review from the user;
   Notion action items; calendar events that imply preparation. If the user named specific sources,
   stay within them; otherwise ask which to sweep rather than crawling everything.

   An obligation is something the *user* owes an action on. Include it only when that is clearly
   true. Skip FYIs, things already done, things waiting on someone else, and anything you are unsure
   about. A false positive clutters the ranking and costs the user a review, so when in doubt, leave
   it out — better to miss one than to spam.

3. Drop anything already captured in step 1 — match on the source link/reference and on meaning, not
   just exact text. Running this daily must not pile yesterday's threads back up.

4. Write the survivors to a JSON manifest file (e.g. /tmp/should-manifest.json):

       {
         "items": [
           {
             "text": "<one concise obligation, in the user's voice>",
             "deadline": "<ISO-8601 date if the source implies one, else omit>",
             "source": "slack|notion|github|calendar",
             "source_ref": "<stable id, e.g. channel/ts or issue number>",
             "source_url": "<permalink>"
           }
         ]
       }

   Only `text` is required. The rest give `should` provenance — so a ranked area traces back to the
   originating thread — and let future runs dedupe. Keep each `text` to a single concrete obligation.

5. Show the user a short summary of what you found and what you deliberately skipped, and let them
   veto or correct it before anything is written into `should`.

6. Once they are happy, hand the manifest to `should` and surface the result:

       should data ingest /tmp/should-manifest.json   # writes the items (still unfiled)
       should perception update                        # clusters + estimates them
       should perception                               # the area tree
       should -k 10                                    # the top areas to attend to now

   Report the tree and the top areas back to the user. Every step auto-commits, so the user can
   review the change with `git diff` or undo it with `git revert`.

7. Help the user sharpen `context.md` — the free-form work-context file that feeds every estimate and
   steers how items are grouped. It is the durable lever for ranking quality: a line like "SAA GA is
   2026-07-30 and is my top priority this quarter" sharpens importance and urgency across the whole
   ranking and survives every rebuild. First ask `should` what it most needs to know:

       should query missing

   Put that question to the user, and also propose any standing facts you learned while gathering —
   deadlines, who is waiting on them, their role and current priorities. With their agreement, add
   the facts to context.md, commit it (git add context.md && git commit -m "context: ..."), then
   re-rank so the change takes effect:

       should perception update --estimate-only   # priority/stakes facts: re-estimate only
       should -k 10

   (If you added a grouping directive — "keep all X work in one area" — use `should perception
   update --rebuild` instead, since that changes structure, not just estimates.)

