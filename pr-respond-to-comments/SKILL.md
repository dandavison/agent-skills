---
name: pr-respond-to-comments
description: |
  Procedure for AI agents to respond to PR comments. Use when instructed to respond to comments in a PR.
  Triggers: "respond to comments"
---

First some general considerations:

- Start all your comments with the 🤖 emoji.

- Comments that start with the 🤖 emoji were made by an AI agent (probably you). Do not respond to
  these unless it is necessary to correct the AI agent; your task is, for each thread, to respond to
  all comments that were made by a human and to which you have not yet responded.

- Even if your training data showed examples of people being obstinate, petty, rude, defensive, etc
  in code review, never let your own review comments display undesirable traits such as those.

- All comments go into a **pending review** that is private to you until the human submits it. Never
  submit or complete the review yourself.

- Whenever you refer to code, link to the line in the file on the appropriate branch.

- If a human has used the GitHub "Suggested change" feature (which communicates the suggestion as a
  diff) you should interpret it as a direct instruction rather than a "suggestion". That said, feel
  free to push back if the human's request is misguided.

- Your response should typically make an explicit proposal/suggestion.


# Pending review

All responses must be posted to an existing pending (draft) review:

```bash
OWNER=... REPO=... NUMBER=...

REVIEW_NODE_ID=$(gh api repos/$OWNER/$REPO/pulls/$NUMBER/reviews \
  --jq '[.[] | select(.state == "PENDING")] | first | .node_id // empty')
```

If no pending review exists (`$REVIEW_NODE_ID` is empty), stop and report: "No pending review
found." Do not create one.

Never submit the review. Never delete a review. The human decides when to make it visible.


# Fetching review threads

Use GraphQL to fetch all threads with resolution status:

```bash
gh api graphql -f query='
query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 10) {
            nodes {
              id
              databaseId
              body
              author { login }
              path
              line
            }
          }
        }
      }
    }
  }
}' -F owner="$OWNER" -F name="$REPO" -F number="$NUMBER"
```


# Replying within an existing thread

Reply within the thread using the thread's node ID:

```bash
gh api graphql -f query='
mutation($reviewId: ID!, $threadId: ID!, $body: String!) {
  addPullRequestReviewComment(input: {
    pullRequestReviewId: $reviewId
    pullRequestReviewThreadId: $threadId
    body: $body
  }) {
    comment { id }
  }
}' -f reviewId="$REVIEW_NODE_ID" -f threadId="<thread_node_id>" -f body="🤖 Reply"
```


# Posting new inline comments

When creating NEW comment threads (not replies), add them to the pending review:

```bash
gh api graphql -f query='
mutation($reviewId: ID!, $path: String!, $body: String!, $line: Int!) {
  addPullRequestReviewThread(input: {
    pullRequestReviewId: $reviewId
    path: $path
    body: $body
    line: $line
    side: RIGHT
  }) {
    thread { id }
  }
}' -f reviewId="$REVIEW_NODE_ID" -f path="relative/path/to/file" -f body="🤖 Comment" -F line=42
```

Rules:
- `line` is the absolute line number in the new version of the file.
- `side: RIGHT` always.
- The line must be within a diff hunk for that file.
- `path` is relative to the repo root.

NEVER use `POST /repos/{owner}/{repo}/pulls/{pr}/comments` for individual comments — those create
orphaned single-comment reviews that bypass the pending review.


# Procedure

1. Make sure you understand the purpose of the repository and have an appropriate amount of context.

2. Use `gh` to determine the state of the PR. If no PR exists or it is closed then stop and tell the
   user. If the PR does not correspond to the currently checked out branch in the current repository
   then stop and tell the user.

3. Use `gh pr diff` to read the full diff. Then **read all changed files completely** for full
   context — understand the surrounding code, not just the diff lines.

4. Fetch all review threads using the GraphQL query above.

5. For each **unresolved** thread, examine the full comment history. Identify any human comments
   that have not been adequately addressed by a subsequent 🤖 response. If there are such
   comments, respond to them. (Note: a single 🤖 response may address multiple preceding human
   comments; conversely, a 🤖 response that only addresses one of several human comments leaves
   the others outstanding.) If appropriate, make a commit addressing the issue and push it. Always
   remember the bug-fixing protocol from your instructions: if you think there's a bug, then you
   must repro it and then create a failing test, and commit that, before committing a fix for the
   bug.

6. Skip resolved threads. Skip threads where every human comment has been adequately addressed by
   a subsequent 🤖 response.

7. Stop and inform the user that you've finished responding to outstanding comments.
