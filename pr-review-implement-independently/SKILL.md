---
name: pr-review-implement-independently
description: |
  Procedure for AI agents to review a PR by first implementing the change themselves independently of the PR
---

You have been provided with a PR URL. You're going to review the PR by
first implementing the change yourself, independently of the PR. To do
this, first use the gh CLI to fetch the PR body. At this stage you
MUST NOT look at their diff. If you have seen their diff, stop.

Read the PR body in its entirety, and any linked issues. Study the
codebase prior to the PR. Now:

- Describe what the author is trying to achieve. If you are not confident about this, stop.

- If their intention is not appropriate, stop.

Next, implement the change yourself in a worktree on the PR's merge
base commit, following all the authorship rules that you normally
would. Commit.

Now, finally, study their implementation. If this is not the first
time you have seen their implementation, stop.

Our aim now is to identify the best change that we are able to that
addresses the problem that the PR is trying to address. It doesn't
matter whether any of their code persists into the final version or
not; be objective.

Is there anything they did that is better than what you did and thus worth retaining?

Create a worktree containing their PR and apply commits on top of it
making it precisely equivalent to your implementation. Now, if there
is anything of their's worth retaining, apply one more commit making
those changes. Set up the worktree so that `git push contributor`
pushes to their PR branch: use `git config --worktree` (enabling
`extensions.worktreeConfig`) to set `remote.contributor.url` to their
fork and `remote.contributor.push` to `HEAD:refs/heads/<their
branch>`. Check with `git push --dry-run contributor`. Do not push;
stop and give me a summary.