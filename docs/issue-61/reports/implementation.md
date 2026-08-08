---
code_under_review: src/rsb/web/dashboard.js, test/rsb_tests/test_dashboard_dom.py, docs/specs/screen-spec.md
loop_state: landed
---

# issue-61 phase 2 — implementation record

Approved proposal: `docs/issue-61/proposals/implementation.md` (PR #66).
Approval: issue-level comment `APPROVE issue-61/implementation` by
`jjongkwann` (approvers.md-listed, single-account mode — PR #66's author
and the approving comment are the same account).

## What was done

Executed `docs/issue-61/proposals/implementation.md`'s "What will be
done" items 1-6, exactly as approved:

1. `dashboard.js:508` (`applySelectionLayout`) — unguarded
   `window.matchMedia(WIDE_LAYOUT_QUERY).matches` replaced with:
   `const mql = typeof window.matchMedia === "function" ?
   window.matchMedia(WIDE_LAYOUT_QUERY) : null; const isWideLayout = mql
   && typeof mql.matches === "boolean" ? mql.matches : true;`, and the
   branch condition now reads `if (!selectedRow || isWideLayout)`.
   Fallback is `true` (wide) per the proposal's Rationale.
2. `detailRowHtml` (`dashboard.js:453`) now emits
   `<tr class="detail-row" id="detail-row">...` (stable id, singleton
   pattern like `#detail-panel-slot`).
3. `applySelectionLayout`'s narrow branch, after inserting the detail
   row, finds the selected button via
   `selectedRow.querySelector(".row-toggle")` and overwrites its
   `aria-controls` to `"detail-row"`. Wide branch and unselected buttons
   keep the default `"detail-panel-slot"` from `rowToggleButtonHtml`
   (unchanged).
4. `test/rsb_tests/test_dashboard_dom.py` gained
   `test_row_toggle_narrow_layout_aria_controls_resolves_to_detail_row`:
   forces narrow layout by reassigning `window.matchMedia = () => ({
   matches: false })` inside the jsdom script (same technique as
   issue-36 conformance-review Appendix A4's instrumented probe, no
   harness change), clicks the toggle, and asserts `#detail-panel-slot`
   is empty, `#detail-row` exists, the button's `aria-controls` reads
   `"detail-row"`, and — the IDREF-resolution assertion F2 requires —
   `document.getElementById(button.getAttribute("aria-controls"))`
   actually resolves to the `#detail-row` element (not just a string
   comparison).
5. `docs/specs/screen-spec.md` §1.3 now states the default
   `aria-controls="detail-panel-slot"` value is narrow-layout-overridden
   to `"detail-row"` and cross-references §1.6; §1.6 gained a symmetric
   bullet stating the inserted `<tr class="detail-row">` carries
   `id="detail-row"` and cross-references §1.3.
6. Requirement 3 (§20 audit) verdict, carried from the approved
   proposal's Rationale: module-scope `document.getElementById` (7
   occurrences, `dashboard.js:3-9`) stays out of scope for this issue —
   no code change made to that class of call. `fetch` (`:638`, already
   try/catch-guarded) and the 3 in-context `document.getElementById`
   calls (`:169/556/595`) carry no independent risk per the same audit.
   No code change.

Stale comment fixed as a byproduct of item 3: the comment above
`rowToggleButtonHtml` previously claimed `aria-controls` was
unconditionally fixed to `"detail-panel-slot"` — no longer true once the
narrow branch overrides it, so the comment was corrected to describe
both values.

## Scope

Frozen write set (per approved proposal, unchanged during execution):
`src/rsb/web/dashboard.js`, `test/rsb_tests/test_dashboard_dom.py`,
`docs/specs/screen-spec.md`.

## Why / upstream basis

Issue #61 (F1/F2, carrying forward #36 conformance-review F1/F2 and #38
R2f). Root cause and fix direction are both settled upstream: #36's
conformance-review Appendix A4 instrumented probe confirmed the crash
mechanism and that both layout branches render correctly once
`matchMedia` is supplied; this issue's own phase-1 survey
(`docs/issue-61/reports/implementation/survey.md` §1) spiked the exact
fix and measured 9/9, 66/66 green before the proposal was written. The
phase-1 warrant hunt (survey.md "Warrant hunt (phase 1)", stance 0)
found the `typeof`-only guard still crashes when `matchMedia` is
callable but returns a value with no usable `.matches` — the approved
proposal's step 1 already folded in a return-value check to close that
gap, and this delivery implements that exact, already-hardened guard
(reproduced clean in this session: `node --check
src/rsb/web/dashboard.js` exits 0).

## Red-green (F1 — `test_dashboard_dom.py`)

- **Red** (before edits, `HEAD` at session start):
  `python3 -m pytest test/rsb_tests/test_dashboard_dom.py -v` →
  **2 failed, 7 passed**. Failures:
  `test_row_toggle_click_opens_detail_and_flips_aria_expanded`,
  `test_row_toggle_reactivating_open_button_closes_it` — both crash
  because this repo's jsdom (v30.0.1, `test/node_modules/jsdom`)
  implements no `window.matchMedia` at all, so the unguarded call at
  `dashboard.js:508` threw inside the click listener before
  `attachRowToggleHandlers` could re-wire the re-rendered buttons.
- **Green** (after all 5 code/test/doc edits):
  `python3 -m pytest test/rsb_tests/test_dashboard_dom.py -v` →
  **10 passed**, 0 skipped (9 pre-existing + 1 new
  `test_row_toggle_narrow_layout_aria_controls_resolves_to_detail_row`).
  Matches the issue's Acceptance bullet
  ("`test_dashboard_dom.py` 전건 통과... 0 skipped") and the proposal's
  "How you'll know it worked" exactly.
- `node --check src/rsb/web/dashboard.js` → clean (exit 0), both before
  and after.
- `grep -n "detail-row" docs/specs/screen-spec.md` → hits in both §1.3
  (line 63) and §1.6 (lines 115-116) — confirms both layout branches are
  now described, per the issue's third Acceptance bullet.

## What did not work

- Expected: the full test suite (`python3 -c "import sys;
  sys.path.insert(0,'src'); import pytest;
  sys.exit(pytest.main(['test/','-q']))"`) would go green at 67/67 (66
  pre-existing + the 1 new `test_dashboard_dom.py` case), per the
  approved proposal's "How you'll know it worked".
  Actual: **66 passed, 1 failed** —
  `test/rsb_tests/test_model.py::test_dashboard_js_detail_row_html_wraps_content_in_a_tr_with_colspan`
  asserts `detailRowHtml(5, "<div>x</div>")` returns the exact string
  `'<tr class="detail-row"><td colspan="5"><div>x</div></td></tr>'`
  (no `id`) — this delivery's required step 2 change
  (`detailRowHtml` now emits `id="detail-row"`, needed so the narrow
  branch's `aria-controls` override in step 3 has a real element to
  resolve to) breaks that assertion's exact-string match. See "Open
  findings" below — `test_model.py` is outside the frozen write set, so
  per the scope-exceeded rule this was left unfixed rather than widening
  the write set mid-build.

## Rationale for deviations

Execution diverged from the approved proposal's "How you'll know it
worked" (full-suite 67/67 green) — see "What did not work" above. This
is a scope-exceeded stop, not a design change: the proposal's own survey
(`docs/issue-61/reports/implementation/survey.md`) discussed
`detailRowHtml` at length but did not surface `test_model.py`'s exact-
string assertion on its output, so the frozen write set (which
deliberately excludes `test_model.py`) turned out to be one file short
of what "full suite green" requires. Per the scope-exceeded rule
("finish what the proposal covers, STOP, and report — never widen
mid-build, never pause to ask mid-build"), `test_model.py` was not
touched. The three in-scope files (`dashboard.js`,
`test_dashboard_dom.py`, `screen-spec.md`) were completed exactly as
specified, and all three of the issue's own Acceptance bullets are met
(`test_dashboard_dom.py` full pass/0-skipped, new narrow-layout
IDREF-resolution case, `screen-spec.md` §1.3/§1.6 both describing the
branch). The full-suite-green target was the proposal's own stricter
self-check, not one of the issue's Acceptance bullets. The remainder
(updating `test_model.py`'s expected string to include `id="detail-row"`)
is the next proposal's write set.

## Open findings

1. **`test_model.py` exact-string regression** (see "What did not
   work"/"Rationale for deviations" above). Kind: test-coupling, not a
   product defect — `detailRowHtml`'s actual behavior is correct and
   intended (proposal step 2); the test's literal string just predates
   the `id` attribute. Not blocking this delivery's own Acceptance
   bullets; blocking full-suite green.
   - **Resolution path**: a follow-up proposal with write set
     `test/rsb_tests/test_model.py` (single-line expected-string update
     to include `id="detail-row"`) — no design decision involved, purely
     mechanical.

## Warrant hunt (before phase-2 completion)

Verdict: NO FINDING.
Kind: n/a.
Stance: 1 — assume this change and another rule/part of the codebase
cancel each other out — find the pair (before-landing, issue-61,
rotated from phase-1's stance 0).
Seed: `src/rsb/web/dashboard.js`, `test/rsb_tests/test_dashboard_dom.py`,
`docs/specs/screen-spec.md` (working-tree diff, ~44 lines across 3
files, tier: default, cap_seconds: 120).
Checked: (1) `dashboard.css` has no rule assuming
`#detail-panel-slot`/`.detail-row` mutual exclusivity that the JS
change could violate — the only CSS keyed on `#detail-panel-slot` is a
`min-width: 1200px` media rule requiring non-empty content, consistent
with the JS; the JS constant `WIDE_LAYOUT_QUERY` matches that breakpoint
exactly. (2) `rowToggleButtonHtml` (`dashboard.js:239`) is the only
literal `aria-controls="detail-panel-slot"` call site in the file — no
other site can go stale against the new override. (3) no test file
besides `test_model.py` (already known/excluded from this hunt's scope)
and `test_dashboard_dom.py` itself asserts exact strings involving
`detail-row`/`aria-controls`. No reproducible "wrong output" pair found.

## Closed checks

- `node --check src/rsb/web/dashboard.js` clean, before and after edits
  — code_under_review: `src/rsb/web/dashboard.js`,
  `test/rsb_tests/test_dashboard_dom.py`, `docs/specs/screen-spec.md`.
- `test/rsb_tests/test_dashboard_dom.py` 10/10 green, 0 skipped —
  code_under_review as above.
- `grep -n "detail-row" docs/specs/screen-spec.md` hits in both §1.3 and
  §1.6 — code_under_review as above.
- Phase-1 warrant hunt finding (matchMedia return-value validation gap,
  survey.md stance 0) — closed by this delivery's exact implementation
  of the proposal's hardened guard (see "Why / upstream basis").
- Phase-2 warrant hunt (stance 1, before-landing) — NO FINDING (see
  section above).

## Doc placement ladder

- Env var/config key/new dep/migration/setup step: none introduced —
  n/a.
- Library-or-format choice / changed public signature or wire format:
  `detailRowHtml`'s output format changed (added `id="detail-row"`) —
  this decision was already recorded at proposal time in
  `docs/issue-61/proposals/implementation.md` ("What will be done" item
  2), approved before this delivery; no separate `docs/issue-61/decisions/`
  entry needed since no new decision was made during execution (built
  exactly as approved, no alternative swapped mid-build).
- Benchmark or investigation numbers: this record's own "Red-green"
  section above is their home (`docs/issue-61/reports/implementation.md`).
