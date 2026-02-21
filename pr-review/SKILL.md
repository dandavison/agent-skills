---
name: pr-review
description: |
  PR review procedure for AI agents. Use when instructed to review a PR.
  Triggers: "review", "pr", "code review"
---

Use the `gh` CLI tool to interact with GitHub.

If the current branch has no associated PR, then stop and inform the user.

Otherwise, use `gh` to determine the state of the PR.

You may only continue if the PR is open and in Draft mode and there are no comments by anyone other
than me (@dandavison).

Otherwise (e.g. PR merged or closed, comments by others, or you were unable to determine state) stop and inform the user.

The instructions below assume that you have determined that it's OK to proceed. First some general considerations:

- Create your review using GitHub's formal "Review" feature as opposed to as a collection of ad-hoc
  comments. Accumulate all comments, write them to a JSON file, then submit as a single review:

  ```bash
  # Build /tmp/review.json:
  {
    "event": "COMMENT",
    "body": "Overall review summary",
    "comments": [
      {"path": "file.go", "line": 42, "side": "RIGHT", "body": "Comment text"},
      ...
    ]
  }
  # Submit:
  gh api repos/{owner}/{repo}/pulls/{number}/reviews --input /tmp/review.json
  ```

  NEVER use `POST /repos/{owner}/{repo}/pulls/{pr}/comments` for individual comments — those create
  orphaned single-comment reviews that don't display inline in the "Files changed" view. The `line`
  is the absolute line number in the new version of the file. Use `side: "RIGHT"` for new/changed
  lines. Comments can only be placed on lines within the PR diff.

- Start all your comments with the 🤖 emoji.



Now follow these steps sequentially:

1. Make sure you understand the purpose of the repository and have an appropriate amount of context.

2. Use gh to read the PR diff. Study it until you understand what it thinks it is trying to do, what you think it should be doing, and the extents to which it has achieved those two things.

3. Review the parts of the diff that change documentation and docstrings. Comment on individual lines as you see fit.

4. Review the parts of the diff that change test coverage, commenting on individual lines as you see fit. In general, a test suite should be passing if and only if the implementation defines correct behavior of the feature. Consider the following as possible reasons to comment:
  - Are there any important ways that the behavior of the feature could be incorrect without resulting in a failing test? If so then there is missing test coverage.
  - Could some essential lines of code be removed from the implementation without resulting in a failing test? If so then there is missing test coverage.
  - Are all tests really testing what they purport to? Or are they in fact testing fake/mock code that was put in place for the purposes of testing?
  - In general, prefer "end-to-end" / "integration" / "functional" tests. "Unit" tests are sometimes appropriate for testing detailed logic, but be skeptical of them, especially when they employ mocking techniques.

5. Review error messages, commenting on individual lines as you see fit. These should be concise, well-written, and should instruct the user both what went wrong and how to address it, while avoiding verbosity. Consider the following as possible reasons to comment:
  - Are there any ways in which the feature could be used wrongly without resulting in an appropriate error message?

6. Review the actual implementation. Consider the following as possible reasons to comment:
  - For each area implemented, can you find related implementation in the repository? If so, are the two consistent? Can the implementation being reviewed benefit from the existing code? Or are you aware of canonical or well-respected implementations of something very similar outside the current repository? If it's a very helpful comparison, make it.
  - Is the code being reviewed appropriately benefiting from/using existing code?
  - The code should be clean, and should use more or less the minimal lines of code possible while remaining clear and idiomatic.
  - Function/variable/class names should be essentially perfect: tastefully chosen to maximize comprehension while conforming to convention. Where possible, explanation of code should be done via well-chosen function/vaiable/class names, rather than comments.
  - Any performance or security concerns?
  - Is the code in the right place?

7. Formulate and post an overall comment regarding the PR. Comment on whether you think what it is trying to do is what it should be trying to do. Comment on the extent to which it has achieved those two things: what more is needed? If there are any serious problems with the PR, or it appears to be going in an inappropriate direction then say so. If there is anything unusually good about the PR then say so, but do this only in exceptional cases.
