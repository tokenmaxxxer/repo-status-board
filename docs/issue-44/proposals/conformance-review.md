# Conformance-review proposal (issue #44)

Phase-1 output: the requirement list this role will score in phase 2, and the
method it will score it by. No verdicts are rendered here.

Subject of review: **PR #45** (`b2f6b63`, merged 2026-08-03), issue #44's
`step 1 test-authoring`, which landed `test/rsb_tests/test_dashboard_dom.py`,
`test/package.json` + `test/package-lock.json`, the `## Tests` section of
`docs/handbooks/rsb.md`, and `docs/issue-44/reports/test-authoring.md`.
Current-state detail: `docs/issue-44/reports/conformance-review/survey.md`.
Direction inputs: `docs/issue-44/reports/conformance-review/scout-brief.md`.

## Method

- One verdict per requirement, from the enum used by this repo's four prior
  conformance-review records (`review-traceability`'s `finding-record` skill):
  **Present / Surface / Absent / Incorrect / Unverifiable**. Recorded as
  `| Requirement | Verdict | Evidence | Rationale |`, matching
  `docs/issue-29/reports/conformance-review.md`.
- **No sampling.** The touched surface is small — one new 270-line test module,
  a 8-line `package.json` (+ lockfile), a 16-line handbook section, and two
  documents — so every requirement below is checked in full. This matches the
  no-sampling statements in the issue-23/27/29 proposals.
- **Verified against the artifact and the spec only.** Issue #44's text is the
  spec; the shipped files are the artifact. The test-authoring role's record
  and proposal are read as *claims to re-derive*, never as evidence for a
  verdict — where the record asserts a result (e.g. "failed as expected"), phase
  2 reproduces it or marks the requirement Unverifiable. This is the role's
  phase-2 mandate (contract v3 §19) and follows the precedent set in
  `docs/issue-29/reports/conformance-review.md:106`.
- **Evidence pointers** are one of: `path:line`; a command with its actual
  output; a git revision/range; or an explicit "could not be run here, and why".
  Per the scout brief, execution evidence distinguishes *executed* from
  *collected* — a `skipped` count is never scored as coverage.
- **Unverifiable is a real verdict**, used whenever evidence cannot be located
  or produced. It is never softened into a favorable guess.
- **Severity banding is not applied** unless the review's scope is explicitly
  extended; this role decides fidelity, not risk weighting.

### Environment preconditions for phase 2

This checkout cannot currently run the suite: `pytest test/` aborts with
`ModuleNotFoundError: No module named 'rsb'`, and `test/node_modules` does not
exist, so all 8 DOM tests would skip. Phase 2 will therefore first run
`pip install -e .` (or `PYTHONPATH=src`) and `npm install --prefix test` — both
reviewer-sandbox setup, neither committed, and `test/node_modules/` is left
untracked (see R10c). `npm view jsdom version` succeeds from here, so the
install is expected to work; if it does not, R1e/R2c/R3c/R4b/R6 become
Unverifiable with the failure output quoted.

## Requirement list

Spine: issue #44's six 수용 기준 (AC1–AC6), extended with the two 요구사항 that
no checkbox covers (요구사항 4 → R9; 범위 밖 → R10) and with record-chain
integrity (R12), the latter precedented by
`docs/issue-4/reports/conformance-review.md`. 12 groups, 31 sub-requirements.

**R1 — a DOM-layer harness exists and actually drives the DOM (요구사항 1, AC1).**
- R1a: the shipped `src/rsb/web/dashboard.js` is loaded against a *real* DOM
  implementation, not a stub like `test_model.py`'s `{ getElementById: () => null }`.
  - Method: read `test/rsb_tests/test_dashboard_dom.py:51-95`; confirm the module
    under test is the shipped path, not a copy.
- R1b: tests dispatch real events rather than calling handlers directly.
  - Method: read each test body for `.click()`/`dispatchEvent` on elements
    obtained from the jsdom document.
- R1c: assertions are on resulting DOM state, not on the return value of a
  helper.
  - Method: read the `console.log(JSON.stringify(...))` payloads and the Python
    asserts consuming them.
- R1d: the harness choice (jsdom) and the entry point (`python -m pytest test/`,
  no second runner) were decided in the proposal and the landed code matches
  that decision — issue #44 requires the decision, and requires it in the
  proposal.
  - Method: `docs/issue-44/proposals/test-authoring.md:61-63,123-127` vs. the
    absence of any new runner/script in the tree.
- R1e: the harness runs — at least one DOM test *executes and passes*, not skips.
  - Method: `python -m pytest test/rsb_tests/test_dashboard_dom.py -v` after the
    preconditions above; quote the per-test outcome line, not just the summary.

**R2 — minimum coverage: repo-filter `<select>` population (요구사항 2 bullet 1; 배경 defect 1, issue #29).**
- R2a: a test exists for it. Method: `test/rsb_tests/test_dashboard_dom.py:128,137,146`.
- R2b: it asserts the options are actually *populated with repo values*, not
  merely that the element exists. Method: read the asserted option lists.
- R2c: it fails against the pre-fix `dashboard.js` (`c94e12d^`).
  - Method: `git show c94e12d^:src/rsb/web/dashboard.js` into a scratch path,
    re-point the harness at it, re-run these three tests, quote the failure.
    Scratch files are deleted, never committed.

**R3 — minimum coverage: `.row-toggle` wiring (요구사항 2 bullet 2; 배경 defect 2, issue #29).**
- R3a: clicking `.row-toggle` flips `aria-expanded` to `true`.
  Method: `test/rsb_tests/test_dashboard_dom.py:177`.
- R3b: clicking an empty/plain cell of the row does **not** open the detail —
  the negative half of the bullet. Method: line 197.
- R3c: both fail against the pre-fix revision (`b621082^`). Method: as R2c.
  The record also states the BVA re-click test (line 231) was not separately
  pre-fix-verified; phase 2 scores that test's own status, not the record's
  explanation of it.

**R4 — minimum coverage: `load()` fetches the relative `api/board.json` (요구사항 2 bullet 3; the issue #27 **Absent** ruling).**
- R4a: a test asserts the fetched URL is exactly `api/board.json`.
  Method: `test/rsb_tests/test_dashboard_dom.py:254`.
- R4b: it fails against the pre-fix revision (`3ebecae^`, when the path was
  absolute). Method: as R2c. Note `c94e12d^` and `3ebecae` are the same commit —
  phase 2 states which tree each run used by SHA, not by shorthand.

**R5 — AC2's fourth item: the mobile-overflow defect (배경 defect 3, issue #38 P1-1).**
- R5a: whether a test corresponds to it, and if not, whether the omission is
  within spec. AC2's text says "배경의 결함 3건 + Absent 1건에 **각각** 대응하는
  테스트" (four), while 요구사항 2 enumerates three bullets and 범위 밖 excludes
  visual/screenshot regression. The artifact declares the omission deliberate
  (`docs/issue-44/reports/test-authoring.md:251-259`).
  - Method: adjudicate by quoting all three spec passages side by side and
    scoring the artifact against the spec as written. This requirement is
    listed precisely because the spec is in tension with itself; it is **not**
    pre-judged here, and the approved test-authoring proposal's own
    reconciliation is a claim to weigh against the issue text, not a settled
    answer.

**R6 — the existing pytest suite still passes (AC3).**
- R6a: a full `python -m pytest test/` run passes with the new module present.
  Method: run it, quote the summary line and the counts.
- R6b: the pass is not a disguised skip — the pre-existing tests and the new
  DOM tests are counted as executed.
  Method: `-rs` / `-v`; report `passed`/`skipped` separately, per the scout
  brief's executed≠collected must-be.
- R6c: no pre-existing test was modified or removed to achieve it.
  Method: `git show --stat b2f6b63` and a diff over `test/rsb_tests/test_*.py`
  other than the new file.

**R7 — the run method is documented (요구사항 3, AC4).**
- R7a: how to run the harness, including the one-time prerequisite, is recorded
  in the handbook or README. Method: `docs/handbooks/rsb.md:48-63`.
- R7b: the documentation actually instructs future sessions to extend this
  harness instead of writing throwaway scripts — 요구사항 3's stated purpose.
  Method: same lines, read for that instruction.
- R7c: the documented commands work as written.
  Method: run `npm install --prefix test` and `python -m pytest test/` exactly
  as documented and report whether the documented sequence alone suffices
  (note: the handbook's `pip install -e .` prerequisite lives in a different
  section — phase 2 reports whether a reader following `## Tests` alone gets a
  working run).

**R8 — the new runtime dependency's rationale is in the record (AC5).**
- R8a: the record states that a new runtime dependency was introduced.
  Method: `docs/issue-44/reports/test-authoring.md:180-189`.
- R8b: the *선택 근거* is in the record. The record routes it to the phase-1
  proposal and says it is "not re-litigated here" — phase 2 decides whether a
  pointer discharges "record 에 남는다".
  Method: read both files; score the record against AC5's wording.
- R8c: the declared scope matches the documented scope — `jsdom` sits under
  `"dependencies"` (`test/package.json:6`, no `devDependencies` key) while the
  record describes it as "dev/test-only". Method: read both; the npm convention
  for a test-only package is `devDependencies` (see scout brief).

**R9 — the relationship to the existing pytest suite is settled (요구사항 4).**
- R9a: a decision on `test_model.py`'s `_run_dashboard_js` (keep vs. absorb) is
  made and recorded. Method: `docs/issue-44/proposals/test-authoring.md:84-90`,
  `docs/issue-44/reports/test-authoring.md` §`_run_dashboard_js disposition`.
- R9b: the landed code matches that decision. Method: `test/rsb_tests/test_model.py:170`
  and its 9 calling tests, unchanged.

**R10 — the declared scope was respected (범위 밖).**
- R10a: no visual/screenshot-regression test was added. Method: read the new
  module for any pixel/screenshot/viewport assertion.
- R10b: no CI test gate was added. Method: `git show --stat b2f6b63` over
  `.github/workflows/**`.
- R10c: no `src/**` change, and any production change the harness needed is
  recorded as a hand-off rather than made. Method: `git show --stat b2f6b63`;
  and check the `.gitignore` `node_modules/` hand-off
  (`docs/issue-44/reports/test-authoring.md:243-250`) is genuinely still open —
  confirmed absent from `.gitignore` at survey time.

**R11 — PR body carries no closing keyword (AC6, issue #23 T2).**
- R11a: PR #45's body contains no closing keyword in any form, including inside
  backticks. Method: `gh pr view 45 --json body` piped through a
  case-insensitive match for `close[sd]?|fix(e[sd])?|resolve[sd]?` adjacent to
  `#44`, quoting any hit.

**R12 — record-chain integrity, bounded to spec-mandated record content.**
- R12a: the record's own AC crosswalk claims match the artifact (this is the
  document AC5 makes load-bearing, so its accuracy is in scope).
  Method: read `docs/issue-44/reports/test-authoring.md:223-240` against R1–R11.
- R12b: citations the record and the test module make about the code resolve.
  Survey found the auto-init seam cited as `dashboard.js:584-591`
  (`docs/issue-44/proposals/test-authoring.md:41-43`,
  `test/rsb_tests/test_dashboard_dom.py:9-10`) while it sits at
  `src/rsb/web/dashboard.js:671`, and "8 pure functions" against a 10-name
  `module.exports` (`src/rsb/web/dashboard.js:680-682`).
  Method: re-resolve each citation against the shipped file.
- R12c: items the record leaves open are actually open, and nothing closed is
  reported as open (or vice versa). Method: check each Open findings bullet.

## Out of scope for this role

- Fixing anything. Findings are recorded and addressed to the owning role
  (test-authoring for `test/**`, implementation for `src/**`/repo-root config);
  this role never edits the artifact it reviews.
- Re-litigating the *approved* methodology choice (jsdom vs. browser
  automation, pytest entry point vs. separate runner). A human approved that
  proposal; conformance is measured against issue #44, not against alternative
  harness designs. R1d checks only that the decision was made and honored.
- Holistic code-quality or style judgment on the new test module, and severity
  banding (see Method).
- Runtime/behavioral observation of the deployed dashboard — that is the
  parallel `execution-observation` role in issue #44's step 2. Overlap is
  limited to the fact that both may run the suite; this role's output is a
  per-requirement verdict, not an execution log.
- Any change under `src/**`, `test/**`, or `.gitignore`.

## Deliverable

`docs/issue-44/reports/conformance-review.md` — one table row per
sub-requirement above (R1a…R12c), each with a verdict, an evidence pointer, and
a rationale, plus an Open findings section addressing each non-Present verdict
to its owning role. Phase-2 output only: not written until a human approver
listed in `docs/specs/approvers.md` approves, per contract v3 §19.
