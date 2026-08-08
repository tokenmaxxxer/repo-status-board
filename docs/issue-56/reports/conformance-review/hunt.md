---
proposal: docs/issue-56/proposals/conformance-review.md
---

# Hunt record — conformance-review

## after-proposal — stance 0: assume the gate just touched is bypassable; find the bypass

Verdict: FINDING — the "two-account mode" self-approval protection the proposal states (PR-review Approve "from an account other than this PR's author") is unconditionally bypassable by the PR author simply not filing a formal GitHub PR review, which routes the gate into "single-account mode" and lets the same account that authored the PR post the exact-string issue comment and approve its own phase 2.
Kind: composition
Seed: docs/issue-56/proposals/conformance-review.md "Phase-2 deliverable" section: "Phase 2 opens only on an Approve from a docs/specs/approvers.md account -- a PR review Approve from an account other than this PR's author, or, in single-account mode, an issue-level comment whose entire body is exactly `APPROVE issue-56/conformance-review`."
cap_seconds: 60
tier: size:docs-only
diff_stat_lines: n/a (docs-only proposal file, no diff stat given)
started_at: 2026-08-08T02:52:08Z
ended_at: 2026-08-08T02:54:10Z

### Reproduce
```
cat docs/specs/approvers.md
gh pr view 57 --json author --jq '.author.login'
gh pr view 57 --json reviews
gh issue view 56 --json comments --jq '.comments[] | {author: .author.login, body: .body}'
```
Also grep the repo's prior phase-2 records for the literal phrase
"single-account mode" to see how the project has resolved the branch
choice in every prior instance.

### Observed
- approvers.md lists two accounts: JiwonJung94, jjongkwann -- the roster
  is not single-account by construction.
- `gh pr view 57 --json author` returns jjongkwann -- PR #57
  (issue-56/implementation, the delivery this proposal reviews) is
  authored by jjongkwann, one of the two listed approvers.
- `gh pr view 57 --json reviews` returns `{"reviews":[]}` -- no formal
  GitHub PR review exists on PR #57 at all, from either account.
- `gh issue view 56 --json comments` shows both prior phase-2 gates on
  this same issue were opened by issue-level comments whose author is
  jjongkwann -- the PR's own author: "APPROVE issue-56/implementation"
  and "APPROVE issue-56/execution-observation". Neither came from
  JiwonJung94, and no PR review from JiwonJung94 appears anywhere on
  PR #57.
- A prior role's execution-observation record for a different issue
  explains the project's own rule for the branch choice: reviews:[]
  (empty) plus "PR's author is the same account as the approvers-list
  entry" resolves to single-account mode, which then only requires the
  same-account issue comment. The same reasoning recurs across several
  other issues' phase-2 records in this repo. So "mode" is not a fixed
  property of the roster (two accounts are registered) -- it is inferred
  after the fact from whether a PR review happens to exist, and that fact
  is entirely within the PR author's control (simply don't request/file
  one).

### Expected
The two-account roster in docs/specs/approvers.md should force the
"account other than this PR's author" branch whenever a second account is
actually registered -- i.e. JiwonJung94 should be required to gate
jjongkwann-authored PRs. Instead, because "single-account mode"
activation depends only on the absence of a PR review (a fact the PR
author fully controls by choice), jjongkwann -- who is simultaneously
PR #57's author and a listed approver -- already opened phase 2 for this
issue's sibling roles ("APPROVE issue-56/implementation",
"APPROVE issue-56/execution-observation") by self-posting the exact-string
issue comment, with zero involvement from the second account. The same
self-approval path is available, unblocked, to open this proposal's own
"APPROVE issue-56/conformance-review" gate: nothing in the proposal, in
docs/specs/approvers.md, or anywhere else pins down which mode applies
independently of the author's choice to skip a PR review, so the
"different from PR author" protection the two-account branch exists to
provide is bypassed by construction whenever the author declines to file
a review.
