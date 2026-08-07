---
code_under_review:
  - src/rsb/cli.py
  - test/rsb_tests/test_cli.py
  - src/rsb/web/dashboard.js
  - test/rsb_tests/test_model.py
  - .github/workflows/deploy-board.yml
  - docs/handbooks/rsb.md
loop_state: delivered
---

# Implementation record — issue #58

Phase-2 build against `docs/issue-58/proposals/2026-08-07-staleness-and-partial-failure-visibility.md`
(approved via `APPROVE issue-58/implementation` issue comment).

## What was done, and why

The board could not tell a reader it was stale, partially failed, or
structurally missing sessions/ledger data (issue #58, D1-D4). Per the
approved proposal:

1. `src/rsb/cli.py` — `_run_once` now returns `1` whenever `model.errors`
   is non-empty (was: only when *every* configured repo failed), so a
   1-of-N-repo fetch failure fails the CI build step instead of
   deploying a complete-looking board (D1). Added `--allow-partial`:
   when set, a partial failure still exits `0`; an all-repos failure
   exits `1` regardless of the flag (nothing to publish either way).
2. `test/rsb_tests/test_cli.py` — added
   `test_main_partial_failure_returns_1_without_allow_partial` and
   `test_main_partial_failure_with_allow_partial_returns_0`, both
   exercised at `cli.main()` level per the issue's acceptance criterion.
3. `src/rsb/web/dashboard.js` — added exported pure function
   `staleness(generatedAt, nowIso, thresholdMs = 45min)`, returning
   `null` when fresh (age <= threshold) or `{ ageMs, label }` when
   stale (D3). Rendered into the existing `PARTIAL_BANNER` element
   (reusing its `.partial-banner` style, `.staleness-banner` added)
   above the partial-failure banner in `renderData()`, naming the
   actual age (e.g. "last updated 3h12m ago") — this single change
   makes every silent-staleness cause (runner outage, disabled cron,
   failed deploy) visible without catching each cause separately.
   Sessions/Accounting `<section>`s are now omitted from
   `renderData()`'s output entirely when both `data.sessions` and
   `data.ledger` are empty (D2), instead of rendering
   permanently-empty tables that misread as "nothing is running".
4. `test/rsb_tests/test_model.py` — added three `staleness()` tests
   (fresh, exactly-at-threshold, past-threshold with age label),
   driven through the existing `_run_dashboard_js`/`require()` pattern.
5. `.github/workflows/deploy-board.yml` — added an `if: failure()` step
   to both the `build` and `deploy` jobs that POSTs to
   `${{ secrets.RSB_ALERT_WEBHOOK }}` via `curl`, so a red scheduled
   run notifies a human-read channel instead of only the Actions tab.
   A missing secret logs and exits `0` (documented no-op, not a second
   failure mode).
6. `docs/handbooks/rsb.md` — documented `--allow-partial`, the
   `RSB_ALERT_WEBHOOK` secret and its no-op-when-unset behavior, the
   45-min staleness threshold and its relation to the 30-min cron, the
   sessions/ledger CI-empty decision (hide the panels), and D4's
   ~2026-10-03 cron re-arm deadline with an owner note.

## Observed output

**Fresh vs. stale (`dashboard.staleness`, run directly against the
shipped `dashboard.js` via `node`):**
```
fresh: null
stale: {"ageMs":34200000,"label":"9h30m"}
```
(fresh case: `generated_at` 20min before `now`; stale case: `generated_at`
9.5h before `now`, matching the issue's own reproduced runner-outage gap.)

**1-of-2-repo-failing config, run through `cli.main()` with `fetch_board`
stubbed to one success + one `boom` error:**
```
--- without --allow-partial ---
exit code: 1
--- with --allow-partial ---
exit code: 0
```

**Full test suite** (`pytest test/`, run against this working tree's
`src/`): `62 passed, 8 skipped` (skips are pre-existing jsdom-absent
DOM-suite skips, unrelated to this change).

## Doctrine-ladder placement (completed)

- [x] New env var/secret (`RSB_ALERT_WEBHOOK`) documented in
      `docs/handbooks/rsb.md` (same turn as the workflow change).
- [x] New CLI flag (`--allow-partial`) documented in
      `docs/handbooks/rsb.md`.
- [x] Operational fact (D4 cron 60-day auto-disable, ~2026-10-03
      deadline) documented in `docs/handbooks/rsb.md` with an owner
      note, per the proposal's "Out of scope" (no keepalive workflow
      built — the issue frames D4 as an operational reminder, not a
      code defect).
- [x] The staleness-computation-location and sessions/ledger-panel
      decisions are recorded in the phase-1 proposal's own Rationale
      section, not duplicated as a separate ADR.

## What did not work

None — no attempt was undone or replaced, and no expected-to-hold
assumption failed during the build. One friction point, not a build
failure: a globally pip-installed editable `rsb` package (a different
checkout of this repo elsewhere on this machine) shadows `import rsb`
unless this working tree's `src/` is put first on `sys.path` — worked
around at test-run time (`sys.path.insert(0, "src")`), noted here for
the next session running `pytest` directly in this tree.

## Warrant hunt

Before-landing hunt dispatched
(`docs/reports/2026-08-07-hunt-staleness-and-partial-failure-visibility.md`),
stance 0 (gate-bypass), cap 180s (diff >200 lines / 6 files touched).
Verdict: **NO FINDING** — checked GH Actions' default shell propagates
`rsb`'s exit code through the `>` redirect, `.github/boards.ci.toml`/the
workflow never pass `--allow-partial`, the new `if: failure()` steps
cannot flip a job's conclusion back to success, and `model.errors` is
always a `list` (no falsy-check type bug).

## Open findings

None outstanding.

## Scope

No file outside the frozen write set
(`src/rsb/cli.py`, `test/rsb_tests/test_cli.py`, `src/rsb/web/dashboard.js`,
`test/rsb_tests/test_model.py`, `.github/workflows/deploy-board.yml`,
`docs/handbooks/rsb.md`) was edited. `src/rsb/web/index.html` was
tried once (a dedicated `#staleness-banner` element) and reverted in
favor of reusing the existing `#partial-banner` element, staying
inside the frozen write set — see the proposal's "reusing the existing
`.partial-banner`-style block" instruction.
