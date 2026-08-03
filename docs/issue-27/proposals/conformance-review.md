# Conformance-review proposal (issue #27)

Scope: check PR #28 (`issue-27/implementation`, **open, unmerged**)
against issue #27's 6 acceptance-criteria items, working from the
artifact (`gh pr diff 28`) and issue #27's body directly per this
role's phase-2 mandate — not from
`docs/issue-27/reports/implementation.md`'s self-report of what was
done. `docs/specs/flows-schema.md` is checked only for relevance (see
survey.md's "Schema-relevance check"): PR #28 does not touch it and
does not change the `board.json` payload shape, so no schema-copy-sync
sub-requirement is decomposed here, unlike issue-23's AC1.

## Method

Phase 2 will produce `docs/issue-27/reports/conformance-review.md` as a
per-requirement verdict table using `review-traceability`'s
`finding-record` skill: one row per requirement below, verdict ∈
{Present, Surface, Absent, Incorrect, Unverifiable}, an evidence
pointer (file:line, workflow-YAML field, test run output, or "no
live-runner/Pages access from this repo"), and a rationale.
`review-severity`'s `severity-classification` is applied only to
findings that are not Present, if any survive — per its own trigger
condition, not a blanket pass over every row. No sampling is needed:
the touched surface is small (2 new files, 1 changed line, 1 doc
section — see survey.md's file-by-file listing) and every touched
line is in scope for a full check.

Each of the 6 acceptance criteria (5 checkboxes + the 6th non-checkbox
process-constraint item) is decomposed below into its
independently-checkable sub-facts, per the survey's observation that
several ACs bundle more than one verifiable claim, and per the
scout's confirmation that a live-only outcome-claim should be split
from its locally-checkable mechanism-claim rather than collapsed into
one row. This decomposition is the discrete requirement list itself —
no verdicts are assigned here.

## Requirement list

**R1 — merged 3-repo board renders at the Pages URL, including
Flows/Decision queue/Hygiene and plan rendering (AC1).**
- R1a: the static-deploy mechanism (dashboard.js's relative
  `fetch("api/board.json")`, the workflow's `_site/api/board.json`
  placement) is structurally correct for resolving under a GitHub
  Pages *project* subpath (not just at a site root).
- R1b: `.github/boards.ci.toml` wires all 3 board repos
  (on-the-record, repo-status-board, tokenmaxxxer-core) into the
  `rsb --json` generation call, so the produced `board.json` is a
  genuinely merged 3-repo payload, not a subset.
- R1c: the Flows table, Decision queue table, and Hygiene panel render
  functions are reused unmodified by this diff (no new/altered
  rendering code for these three sections) — a diff-content fact.
- R1d: plan rendering (issue #23's feature: step order, roles, `done`
  state) is unbroken by this diff — the one changed line
  (`dashboard.js:406`) is unrelated to `buildPlanSteps()`/
  `renderPlanSection()`, so this is a non-regression check.
- R1e (likely Unverifiable-within-this-repo): actually opening the
  live Pages URL and visually confirming all of Flows/Decision
  queue/Hygiene/plan render correctly — requires a live deployed
  Pages site, unreachable from this sandbox (matches PR #28's own
  admitted limitation).

**R2 — `board.json` refreshes on each cron tick, confirmed via as-of
timestamp (AC2).**
- R2a: the `schedule` trigger's cron expression (`*/30 * * * *`) is
  syntactically a recurring 30-minute-interval trigger.
- R2b: each triggered run regenerates `board.json` with a fresh
  timestamp — `_run_once()` (`src/rsb/cli.py`) calls `_now_iso()` anew
  per invocation, a fact about unchanged code this diff relies on but
  does not itself modify.
- R2c: the as-of timestamp is surfaced in the dashboard's rendered UI
  (`dashboard.js`'s `HEADER_META` line), unchanged by this diff, so an
  operator can observe freshness without inspecting raw JSON.
- R2d (likely Unverifiable-within-this-repo): two real consecutive
  scheduled runs on the live workflow actually producing two
  different published `generated_at` values — requires observing
  GitHub's actual cron scheduler fire twice in production, unreachable
  from this sandbox.

**R3 — empty `sessions`/`ledger` render cleanly, reusing existing
empty handling (AC3).**
- R3a: PR #28's diff adds no new empty-state handling code — the
  diff's only `dashboard.js` change (line 406) is unrelated to
  `sessionRows()`/`renderAccounting()`/`renderTable()`'s
  `emptyMessage` branch/the page-level all-empty guard — confirming
  "reuses existing handling" is literally true of the diff, not
  merely asserted.
- R3b: the `runs/`-absent-on-a-fresh-runner code path (on-the-record's
  `spawn.py`/`gates/flows.py`, outside this repo's own write set) is
  the thing that must actually degrade to empty `sessions[]`/
  `ledger[]` without error for R3a's reused handling to have anything
  clean to render — checkable by source reading (as PR #28's own
  survey did) but not by anything inside this repo's own test suite,
  since that upstream code isn't part of this repo.
- R3c (likely Unverifiable-within-this-repo): the live Pages output
  actually *looking* clean (no error banner, no broken layout) for a
  real all-empty `sessions`/`ledger` case — requires a live deployed
  Pages site, unreachable from this sandbox.

**R4 — local `rsb serve` has zero regression; full test suite passes
(AC4).**
- R4a: `src/rsb/webserver.py` (the local-serve live `/api/board.json`
  handler) is untouched by PR #28's diff.
- R4b: the changed fetch path (`dashboard.js:406`) resolves
  identically under local `rsb serve` (page served at root — absolute
  and relative paths are equivalent there), so the fix is safe by
  construction for the local-serve case, not merely believed safe.
- R4c: the existing test suite passes with PR #28's diff applied —
  independently re-run by phase 2 against a checkout of PR #28 (not
  accepted from `implementation.md`'s "41 passed" claim as-is; this
  survey independently confirmed 41 passed on pre-PR-28 `main` as the
  baseline).
- R4d: whether the one-line client-side change itself has direct test
  coverage (the diff adds no test file) — a fact distinct from R4c,
  since a passing suite with no new coverage for the changed line is
  not the same claim as "this line is regression-tested."

**R5 — a failed workflow run leaves the prior deployment untouched
(AC5).**
- R5a: the job graph structurally gates `deploy` on `build`'s success
  via `needs: build` with no `if:` weakening it (the workflow file has
  no `if:` key anywhere, despite PR #28's own prose describing
  "`if:`/`needs:` gating" in places — phase 2 should verify the
  mechanism as-built, not the prose description).
- R5b: within the `build` job, no step suppresses failure
  (`continue-on-error: true`, `|| true`, etc.) between the
  failure-prone generation step (`rsb --config ... --json > board.json`)
  and the artifact-upload steps, so a nonzero `rsb` exit genuinely
  stops the job before `configure-pages`/`upload-pages-artifact` run.
- R5c (likely Unverifiable-within-this-repo, and structurally more
  constrained than R1e/R2d/R3c): actually triggering a
  deliberately-broken-config run against the live workflow and
  confirming the live Pages URL still serves the prior `board.json` —
  requires both a live Actions run *and* pre-existing Pages deployment
  history (at least one prior successful deploy to have something to
  "leave untouched"), neither of which can exist in this sandbox.

**R6 — PR-body closing-keyword prohibition (issue #27's 6th item;
process constraint on this issue's own PRs, not a feature of the built
artifact).**
- R6a: PR #28's current body text (fetched via `gh pr view 28
  --json body`) contains no GitHub closing-keyword pattern
  (close/closes/closed, fix/fixes/fixed, resolve/resolves/resolved)
  immediately followed by `#27`, in plain text, quotes, or backticks.
- R6b: this conformance-review role's own PR body (opened at the end
  of this phase-1 pass) independently satisfies the same constraint —
  self-applicable, checked by this role against its own output, not
  just an inspection target on PR #28.

## Out of scope for this role

- Re-litigating whether `boards.ci.toml`'s design (single shared
  `spawn.py` checkout serving all 3 board entries) was the right
  architectural choice — that decision is recorded in PR #28's own
  proposal Rationale; phase 2 checks whether the artifact matches
  issue #27's 6 ACs, not whether every design alternative was
  correctly weighed.
- Fixing anything found — per contract, conformance-review records
  findings; it does not patch `.github/`, `src/`, or `test/`. Any
  non-Present verdict hands off to a follow-up issue, matching this
  repo's `docs/issue-4/reports/conformance-review.md` and
  `docs/issue-23/reports/conformance-review.md` precedent.
- Actually flipping this repo's Pages source setting to "GitHub
  Actions," or triggering a real workflow run — both require repo-admin
  access and a live GitHub Actions/Pages environment this role does not
  have; the R1e/R2d/R3c/R5c live-only sub-facts above are the
  documented boundary of that gap, not something this role can close by
  itself.
- Flows fully-remote optimization (API-only, no `actions/checkout`
  clone) — issue #27's own body explicitly punts this to a separate
  issue ("클론 없이 API만으로 가는 최적화는 별도 이슈"), so it is not
  one of the 6 ACs and not decomposed above.
- on-the-record's own `spawn.py`/`gates/flows.py` internals beyond
  what R3b needs to cite — this repo's write set does not include that
  repo, and issue #27's requirement 4 text itself says a genuine
  problem there would be "환류"'d (fed back) to on-the-record as a
  separate item, not fixed here.

## Deliverable

`docs/issue-27/reports/conformance-review.md`: one row per R1a-R6b
above (19 sub-requirements), verdict
(Present/Surface/Absent/Incorrect/Unverifiable), evidence pointer,
rationale; a findings section, severity-classified, for any
non-Present row. Phase 2 opens only after an `approvers.md` account
(JiwonJung94, jjongkwann) posts the issue-level comment `APPROVE
issue-27/conformance-review` on issue #27.
