---
name: pr-review-simple
description: |
  PR review procedure for AI agents.
---

Output a review of this PR as described below.
Where you are instructed to output text, output a small number of bulletpoints, each comprising one sentence.
When you exit due to a problem, explain the problem.

- Ensure that you are in a directory containing a clone of the PR's repo, with the commit corresponding to the PR checked out. Exit if not.

- Check the relevant tests are passing.

- Describe what the author is trying to achieve. If you are not confident about this, exit.

- If their intention is not appropriate, exit.

- If there is a major flaw in their implementation that is preventing them from achieving their intention, exit.

- Study the test coverage added.
  Describe any important aspects of the PR's intention that are not tested.
  Describe any test that is not achieving what it intends to.
  Describe any test that is a false negative in the sense that, were the corresponding part of the implementation to be reverted, the test would nevertheless continue to pass.

- Describe all correctness bugs.

- Describe any other major flaws you perceive in the PR.
