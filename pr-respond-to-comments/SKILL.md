---
name: pr-respond-to-comments
description: |
  Procedure for AI agents to respond to PR comments. Use when instructed to respond to comments in a PR.
  Triggers: "respond to comments"
---

Use the `gh` CLI tool to interact with GitHub.

If the current branch has no associated PR, then stop and inform the user.

Otherwise, use `gh` to determine the state of the PR.

You may only continue if the PR is open and in Draft mode and there are no comments by anyone other
than me (@dandavison).

Otherwise (e.g. PR merged or closed, comments by others, or you were unable to determine state) stop and inform the user.

The instructions below assume that you have determined that it's OK to proceed. First some general considerations:

- Comments may be associated with specific lines, or not. If a comment is associated with a specific
  line then any response you make must be made in response to that comment such that it appears as part of that discussion thread.

- Comments may be associated with a formal Review, or not.

- The PR may have a pending "Review". It is OK to respond to comments in this situation. Never delete a review, pending or otherwise.

- Start all your comments with the 🤖 emoji.

- Comments that start with the 🤖 emoji were made by an AI agent (probably you). Do not respond to these unless it is necessary to correct the AI agent; your task is to respond to comments made by humans.


Now follow these steps sequentially:

1. Make sure you understand the purpose of the repository and have an appropriate amount of context.

2. Use gh to read the PR diff. Study it until you understand what it thinks it is trying to do, what you think it should be doing, and the extents to which it has achieved those two things.

3. Fetch all comments from the PR.

4. For each comment thread, determine whether it requires a response from you (e.g. last comment is a human saying something that requires a response from you, or you perceive something in the thread that needs correcting or addressing). If it does, formulate and post that response as a new message in the thread. If appropriate, make a commit addressing the issue and push it.

5. For each comment not in a comment thread, determine whether it requires a response from you (was made by a human and requires a response and has not been responded to, or you perceive something in it that needs correcting). If it does, formulate and post that response as a new message outside any thread. If appropriate, make a commit addressing the issue and push it.

6. Stop and inform the user that you've finished responding to outstanding comments.


# Commands

List comments: `gh api repos/{{repo}}/pulls/{{pr}}/comments`

Reply to a comment: `gh api repos/{{repo}}/pulls/{{pr}}/comments/{comment_id}/replies -f body="your reply"`
