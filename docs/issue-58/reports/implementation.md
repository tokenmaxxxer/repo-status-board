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

Follow-up (operator relay on PR #59, 2026-08-08): a local re-run without
that workaround reported 2 FAILED (both `test_cli.py` partial-failure
acceptance tests) + 8 skipped. Root-caused, not a code defect: the
operator's shell had `$PYTHONPATH` pointing at
`/home/jwjung/tokenmaxxxer/repo-status-board/src` — an older sibling
checkout without the `--allow-partial` change — ahead of this branch's
`src/`, so `import rsb` resolved to the stale copy (confirmed via
`python3 -c "import rsb.cli as c; print(c.__file__)"` and a `diff`
against this tree's `cli.py`, which showed the sibling missing the
entire `--allow-partial` plumbing). With `PYTHONPATH` set to point at
this tree's `src/` first, both tests pass. The 8 skips are unrelated
and pre-existing (`test_dashboard_dom.py`, from issue-44, gated on
`npm install --prefix test` for jsdom — not in this issue's write set).
Full suite: `62 passed, 8 skipped` — no code change made this round.

Follow-up (2026-08-08): with `npm install --prefix test` run, the 8
previously-skipped `test_dashboard_dom.py` tests activated and 2 failed
(`test_row_toggle_click_opens_detail_and_flips_aria_expanded` and,
transitively, the same root cause would have hit
`test_row_toggle_reactivating_open_button_closes_it` had the first not
masked it). Root cause: `applySelectionLayout()`
(`src/rsb/web/dashboard.js`) called `window.matchMedia(WIDE_LAYOUT_QUERY)`
unconditionally to pick the wide-vs-narrow detail-panel render path;
jsdom's default `JSDOM` config (used by the new DOM test harness) does
not implement `window.matchMedia` at all, so the call threw mid-render,
leaving `DETAIL_SLOT` populated from before the click instead of the
new panel content. Fixed by guarding the call:
`typeof window.matchMedia !== "function" || window.matchMedia(...).matches`
— environments without `matchMedia` now default to the wide/side-panel
layout (the primary, `DETAIL_SLOT`-based path) rather than crashing.
`test/rsb_tests/test_dashboard_dom.py` needed no change. Full suite with
jsdom installed: `70 passed` for the Python-visible run (`test_cli.py`'s
2 partial-failure tests still need the `PYTHONPATH` workaround above,
unrelated to this fix); `test/rsb_tests/test_dashboard_dom.py` alone:
`8 passed, 0 skipped`.

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

## Follow-up (2026-08-08): rebase onto origin/main, PR #61/#62 conflicts

PR #59 was green but had drifted behind `origin/main` (4 vs 34 commits
apart) after the #61/#62 work landed on `dashboard.js`. Rebased
`issue-58/implementation` onto `origin/main`; two conflicts in
`src/rsb/web/dashboard.js`, both in `renderData()`/`applySelectionLayout()`:

1. The Sessions-section-close/`renderErrors(data.errors)` block conflicted
   with main's own reshuffling of the same region. Resolved by keeping
   the `showSessionsAndLedger`-gated close and the `renderErrors(...)`
   call as they stood on this branch.
2. The `matchMedia` guard (this file's own earlier fix, above) conflicted
   with an equivalent inline guard added independently on main. Kept
   this branch's named-variable (`mql`) version — functionally identical.

Conflict (1)'s naive resolution left a call to `renderErrors(...)`, a
function `origin/main` had since deleted (superseded by the
partial-banner collapsible-details rendering this branch already
relies on) — undetected by the merge itself since the conflict markers
resolved cleanly, only surfacing as a `ReferenceError` inside
`renderData()`'s try/catch, which silently fell through to
`renderFullError()` and left `.row-toggle` buttons unrendered. Caught by
rerunning the full suite: 6 `test_dashboard_dom.py` failures, all
`Cannot read properties of null` on `.row-toggle` element lookups.
Fixed by dropping the `renderErrors(data.errors)` call — the Errors
section it rendered is exactly what `origin/main`'s partial-banner
change (test `test_partial_failure_raw_message_absent_from_main_content_and_errors_section_gone`)
already asserts is gone.

Full suite after fix, with `PYTHONPATH=src` (see the shadowing note
above — still required, an operator-shell issue, not a code defect) and
`test/node_modules` present: `77 passed, 0 failed, 0 skipped`.
