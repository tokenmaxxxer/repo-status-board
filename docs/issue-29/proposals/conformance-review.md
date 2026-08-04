# Conformance-review proposal (issue #29)

Scope: check the merged implementation (PR #30 `issue-29/implementation`
phase 2, PR #33 fast-follow, both on `main` at `b621082`) against issue
#29's 8 acceptance-criteria checkboxes, working from the artifact and
the issue text directly per this role's phase-2 mandate — not from
`docs/issue-29/reports/implementation.md`'s self-report. Also
independently confirms (or refutes) the two defects logged as issue #29
comments after PR #30 merged (repo-filter wiring; row-toggle wiring/
aria), since the task explicitly names both as confirmation targets.

## Method

Phase 2 will produce `docs/issue-29/reports/conformance-review.md` as a
per-requirement verdict table using `review-traceability`'s
`finding-record` skill: one row per requirement below, verdict ∈
{Present, Surface, Absent, Incorrect, Unverifiable}, an evidence pointer
(file:line or test name), and a rationale. `review-severity`'s
`severity-classification` is applied only to findings that are not
Present, if any survive. No sampling is needed: the touched surface is
small (~500-line combined diff across `fetch.py`/`cli.py`/`dashboard.js`/
`dashboard.css`/`index.html`) and every touched line is in scope for a
full check.

Each of the 8 acceptance criteria is decomposed below into its
independently-checkable sub-facts, per the survey's observation that
several ACs bundle more than one verifiable claim (and, for AC3/AC6,
per the issue comments' own enumerated defect items) — this
decomposition is the discrete requirement list itself; no verdicts are
assigned here.

## Requirement list

**R1 — parallel collection + timeout headroom (AC1).**
- R1a: `fetch_board()` fetches repos concurrently
  (`ThreadPoolExecutor`/`.map()`), not serially.
- R1b: `DEFAULT_TIMEOUT_SECONDS` raised from the pre-#29 15s to a value
  with a documented margin over the issue's own 26.7s measurement.
- R1c: an automated test demonstrates parallel wall-clock is
  meaningfully shorter than serial (not just that the code *looks*
  concurrent).
- R1d: a CLI/config mechanism exists to adjust the timeout without a
  code change.
- R1e (likely Unverifiable-within-this-repo): the documented margin
  still holds against real, present-day `flows --json` timings — no
  `on-the-record`/`tokenmaxxxer-core` checkout or live `spawn.py` exists
  in this repo/environment to re-measure.

**R2 — one repo failing doesn't drop the others (AC2).**
- R2a: per-repo fetch/normalize failures are caught and turned into a
  `RepoError`, never raised past `fetch_and_normalize_one`.
- R2b: this isolation is proven against the *new* `ThreadPoolExecutor`
  path specifically (not just inherited from the old serial code by
  assumption).

**R3 — `All repos` ↔ per-repo switch recomputes table + chips together (AC3, = Defect A).**
- R3a: the repo-filter `<select>`'s options are populated from live
  fetched data (not hardcoded to just "All repos").
- R3b: a `change` listener is attached and calls the filter/render path
  with no refetch.
- R3c: the *table* rows narrow to the selected repo.
- R3d: the *summary chips* recompute for the selected repo, not just the
  table (the AC's "함께" clause — checked as a fact distinct from R3c
  since a bug could desync them).
- R3e: switching back to "All repos" restores the full unfiltered view.

**R4 — Repo-first columns + per-table-only scroll (AC4).**
- R4a: all four dashboard tables (Decision queue, Flows, Sessions,
  Accounting) render `Repo` as the first header *and* the first cell in
  every row (header/cell order match, not just header text).
- R4b: each table is wrapped in its own horizontally-scrolling
  container, independent of the others.
- R4c: no page-level horizontal scroll is structurally possible at
  narrow widths (no element outside the per-table scroll containers is
  wider than the viewport) — code/CSS inspection only, no narrow-viewport
  render available in this sandbox.

**R5 — failure banner: summary + collapsed detail (AC5).**
- R5a: an always-visible `"{M} of {N} repos failed to load"` summary
  line renders when 1+ repos fail but not all.
- R5b: the per-repo `"{repo}: {message}"` detail is actually collapsed
  behind a `<details>/<summary>` disclosure, not inlined into the
  always-visible line (survey.md flags this as a likely non-Present
  sub-fact, self-disclosed by `docs/issue-29/reports/implementation.md`
  "Open findings" #4 and both re-synced spec docs, but not named in
  either issue comment — phase 2 independently re-derives the verdict
  from the current code, not from that self-report).

**R6 — keyboard-only row-detail opening (AC6, = Defect B items 1-4).**
- R6a: the disclosure trigger is a real `<button>`, not a clickable
  `<tr>`.
- R6b: the click handler binds to the button itself (`.row-toggle`), not
  the row.
- R6c: `aria-expanded` reflects the actual open/closed state (requires
  tracking which table's row is selected, not just issue+repo).
- R6d: `aria-controls` references an id that actually exists in the
  rendered DOM.

**R7 — narrow-screen inline expansion (요구사항 5, = Defect B item 5; not itself an AC checkbox but explicitly named by the defect comment as a separate unmet requirement, and the task asks this review to confirm both defects).**
- R7a: a `matchMedia`-driven branch exists selecting side-panel vs.
  inline-row rendering at the documented `breakpoint-lg` (1200px).
- R7b: the narrow-screen path actually inserts the detail as a row
  immediately below the triggering row in the same table (not just
  matching CSS existing for an unreachable code path).

**R8 — existing tests pass, no local-serve regression (AC7).**
- R8a: full pytest suite passes at the current `main` tip (fresh run
  this session, not a carried-over count from either PR's self-report).
- R8b: `webserver.py`/`serve`-path tests specifically are included in
  that green run (the AC's explicit "로컬 serve 회귀 없음" clause).

**R9 — PR body has no closing keyword (AC8, PR #30 and PR #33 only — PR #35/#37 belong to issues #34/#36, out of this AC's scope).**
- R9a: PR #30's body contains no GitHub closing-keyword phrase
  (close/closes/closed/fix/fixes/fixed/resolve/resolves/resolved
  immediately adjacent to `#29`), including inside backticks (issue #23
  T2's warning that backtick-quoted mentions still parse).
- R9b: same check for PR #33's body.

## Out of scope for this role

- Fixing anything found — per contract, conformance-review records
  findings; it does not patch `src/`/`test/`. Any non-Present verdict
  hands off to a follow-up issue, matching this repo's
  `docs/issue-4/reports/conformance-review.md` and
  `docs/issue-23/reports/conformance-review.md` precedent.
- `src/rsb/render.py` (CLI text renderer)'s column order — issue #29's
  Rationale section explicitly scopes the Repo-first requirement to the
  dashboard only; not part of R1-R9.
- Re-litigating the implementation role's own "Open findings"/"What did
  not work" sections as a narrative — R5b and R7 independently re-derive
  their verdicts from the current code/spec, but do not re-summarize
  that record's prose.
- New JS test harness / browser automation — both already explicitly
  out-of-scope calls made by the approved implementation proposal
  (`docs/issue-29/proposals/implementation.md` "Out of scope"), not
  reopened here. R1e, R4c, R6's keyboard-operability inference, and R7
  are constrained accordingly (code-inspection-only or
  Unverifiable-within-this-repo where no local means exists).

## Deliverable

`docs/issue-29/reports/conformance-review.md`: one row per R1a-R9b above
(23 sub-requirements), verdict (Present/Surface/Absent/Incorrect/
Unverifiable), evidence pointer, rationale; a findings section,
severity-classified, for any non-Present row.
