---
name: log
description: |
  Work with my log repo (temporalio/dandavison-log issues cloned at ~/src/temporalio-etc/log)
  Triggers: "log", "exfiltrate", "gather-context"
---

# Log

I store notes / AI agent discussions / plans etc in the github issues of temporalio/dandavison-log.
I sync the issues to markdown files stored in the repo; my local clone is ~/src/temporalio-etc/log.

## Exfiltrate

Exfiltrate means to extract from agent conversations their knowledge/understanding/beliefs/wisdom
etc regarding a certain topic and post it to issue(s) in my log repo.

There are two forms of "exfiltrate": either I will ask you to exfiltrate to a certain target issue
number, or I will ask you to exfiltrate without specifying an issue number.

You will be using the /agent-sessions skill to find sessions and interact with them.

Run agent-sessions sync before you start.

### Exfiltrate without a target issue number

When I ask you to "exfiltrate" agent discussion on a certain topic, do the following:

1. Use /agent-sessions to find relevant agent sessions.
2. Determine which log issues those agents have been posting comments to by studying the transcript
   or asking the agents. If they have not posted to any log issue then open a new issue, and post a
   terse description of the topic in question to the body, and consider the set of issues to be this
   one issue.
3. Use gh-issue-to-md to dump to disk the full markdown content of each issue.
4. For each agent session, use /agent-sessions to ask that agent session to determine whether it has
   any valuable knowledge/understanding/wisdom/belief that is not already reflected in the log issue
   comments. If it does, then it should post a new comment to the appropriate issue(s) containing
   this knowledge/understanding/wisdom/belief. To do this step, provide the appropriate subset of
   the issue markdown files dumped at step 3 inline in the prompt you deliver to the agent session.
   I would like you to provide these inline in your prompt, not merely as file references, so that
   the agent is forced to read it in its entirety. However, avoid triggering compaction in the agent
   sessions.
5. Return to me the issue numbers.

If you created a new issue at step 2 then at the end, read all comments via gh-issue-to-md and
update the body to contain a terse executive summary.


### Exfiltrate to a target issue number

In this case, your task is to extract all knowledge/understanding/beliefs/wisdom etc on the topic to
a _new_ issue.

Formally, the procedure is as above but you disregard any log issues they may have already posted
to. I.e. at step 2 you _assume_ that they have posted to no log issue and open a new one, and then
proceed, so that the end result is that each agent session is asked to post a comment to the new
issue.


## Gather-context

When I ask you to gather-context on a topic, do the following:

1. Exfiltrate the topic
2. Open a new issue and write a placeholder topic summary in the body.
3. Use Slack MCP and /agent-slack to perform exhaustive slack searches on the topic.
4. Use Notion MCP to search Notion on the topic.
5. If there are google docs, fetch them as markdown if you can, or if not ask me to help.
6. Perform codebase research
7. Fetch to disk the full content of every log issue written to by the exfiltrate using gh-issue-to-md.
8. Read all slack, notion, google doc, and exfiltrated agent session / log issue content in its
   entirety and write a synthesis as a comment(s) in the new issue

At any point, if slack/notion etc are unavailable, stop and ask me; do not skip/fallback -- this
will result in inferior results.
