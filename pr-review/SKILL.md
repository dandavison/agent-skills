---
name: pr-review
description: |
  PR review procedure for AI agents. Use when instructed to review a PR.
  Triggers: "review", "pr", "code review"
---

First some general considerations:

- Start all your comments with the 🤖 emoji.

- All comments go into a **pending review** that is private to you until the human submits it. Never
  submit or complete the review yourself.


# Pending review

All comments must be posted to a pending (draft) review that you create. First, check that no
pending review already exists:

```bash
OWNER=... REPO=... NUMBER=...

EXISTING=$(gh api repos/$OWNER/$REPO/pulls/$NUMBER/reviews \
  --jq '[.[] | select(.state == "PENDING")] | first | .node_id // empty')
```

If `$EXISTING` is non-empty, stop and inform the user: "A pending review already exists." Do not
proceed.

Otherwise, create a new pending review:

```bash
REVIEW_NODE_ID=$(gh api -X POST repos/$OWNER/$REPO/pulls/$NUMBER/reviews --jq '.node_id')
```

Never submit the review. Never delete a review. The human decides when to make it visible.


# Posting comments

Add each comment as a new thread on the pending review via GraphQL:

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
- `side: RIGHT` always (commenting on the new version).
- The line must be within a diff hunk for that file.
- `path` is relative to the repo root.

To set or update the review body (overall summary):

```bash
gh api graphql -f query='
mutation($reviewId: ID!, $body: String!) {
  updatePullRequestReview(input: {
    pullRequestReviewId: $reviewId
    body: $body
  }) {
    pullRequestReview { id }
  }
}' -f reviewId="$REVIEW_NODE_ID" -f body="🤖 Overall summary"
```

NEVER use `POST /repos/{owner}/{repo}/pulls/{pr}/comments` for individual comments — those create
orphaned single-comment reviews that bypass the pending review.


# Preconditions

Use `gh` to determine the state of the PR. If no PR exists or it is closed, stop and tell the user.

The PR MUST correspond to the currently checked out branch in the current local repository, because
you are going to use the local repository to gather context for the PR review. If it does not, STOP
and tell the user. Do NOT proceed with the review under any circumstances, even if you think you
would be able to do the review task adequately.


# Review procedure

1. Make sure you understand the purpose of the repository and have an appropriate amount of context.

2. Try to create a pending Review using the instructions above.

3. Use `gh pr diff` to read the full diff. Then **read all changed files completely** for full
   context — understand the surrounding code, not just the diff lines.

4. Do you understand the intent of the PR? Is the intent what it should be? Is it basically doing
   what it intends?

5. Review the parts of the diff that change documentation and docstrings. Comment on individual
   lines as you see fit.

6. Review the parts of the diff that change test coverage, commenting on individual lines as you see
   fit. In general, a test suite should be passing if and only if the implementation defines correct
   behavior of the feature. Consider the following as possible reasons to comment:
   - Are there any important ways that the behavior of the feature could be incorrect without
     resulting in a failing test? If so then there is missing test coverage.
   - Could some essential lines of code be removed from the implementation without resulting in a
     failing test? If so then there is missing test coverage.
   - Are all tests really testing what they purport to? Or are they in fact testing fake/mock code
     that was put in place for the purposes of testing?
   - In general, prefer "end-to-end" / "integration" / "functional" tests. "Unit" tests are
     sometimes appropriate for testing detailed logic, but be skeptical of them, especially when they
     employ mocking techniques.

7. Review error messages, commenting on individual lines as you see fit. These should be concise,
   well-written, and should instruct the user both what went wrong and how to address it, while
   avoiding verbosity. Consider the following as possible reasons to comment:
   - Are there any ways in which the feature could be used wrongly without resulting in an
     appropriate error message?

8. Review the actual implementation. Consider the following as possible reasons to comment:
   - For each area implemented, can you find related implementation in the repository? If so, are
     the two consistent? Can the implementation being reviewed benefit from the existing code? Or are
     you aware of canonical or well-respected implementations of something very similar outside the
     current repository? If it's a very helpful comparison, make it.
   - Is the code being reviewed appropriately benefiting from/using existing code?
   - The code should be clean, and should use more or less the minimal lines of code possible while
     remaining clear and idiomatic.
   - Function/variable/class names should be essentially perfect: tastefully chosen to maximize
     comprehension while conforming to convention. Where possible, explanation of code should be done
     via well-chosen function/variable/class names, rather than comments.
   - Any performance or security concerns?
   - Is the code in the right place?

9. Set the review body to an overall comment regarding the PR. Comment on whether you think what it
   is trying to do is what it should be trying to do. Comment on the extent to which it has achieved
   those two things: what more is needed? If there are any serious problems with the PR, or it
   appears to be going in an inappropriate direction then say so. If there is anything unusually
   good about the PR then say so, but do this only in exceptional cases.
