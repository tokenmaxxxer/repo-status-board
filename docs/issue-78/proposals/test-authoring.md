---
status: proposed
files:
  - test/rsb_tests/test_dashboard_dom.py
---

## What was asked

Issue #78: implement the tests specified by
`docs/issue-72/reports/requirements-engineering.md` (REQ-72-1..3 — the
non-visual, selector-scoped DOM/CSS-declaration formulation of the
mobile-overflow requirement). Each test must trace to its REQ id;
`python3 -m pytest test/ -q` must pass with the new tests executed, not
skipped; no pre-existing test may be modified or removed.

## Survey pointer

`docs/issue-78/reports/test-authoring/survey.md` — traces the fix
mechanism the requirements cite (`src/rsb/web/dashboard.js:205`,
`src/rsb/web/dashboard.css:219,412-414`, all matching the requirements
doc's line numbers with no drift), inventories the reusable test
machinery already in `test/rsb_tests/test_dashboard_dom.py`
(`_run_dom_js`, `_dashboard_html_with_css`, `_board_payload`), and weighs
the one open implementation choice (CSSOM rule lookup vs.
`getComputedStyle`) for REQ-72-2/3's selector-scoping constraint.

## Adopted methodology

Scout: **skipped**. Skip condition 2 applies — the spec leaves no
product-facing or exemplar-comparable design decision open.
`docs/issue-72/reports/requirements-engineering.md` already fixes each
requirement's statement, EARS pattern, verification method, and
Given/When/Then, including an explicit selector-scoping constraint that
dictates the verification *technique* (inspect the specific rule block,
never a whole-file substring search). The only decision left was an
internal test-implementation choice, resolved by the survey rather than
by scouting an external field.

Test-design technique: Equivalence Partitioning / Boundary-Value Analysis
at the REQ level — REQ-72-1's partition is "table count" (covered by
exercising all four dashboard tables in one payload, the boundary the
requirement's own text sets: "present for all four dashboard tables");
REQ-72-2/3's partition is "declaration present on the correct selector vs.
present-but-on-the-wrong-selector vs. absent" (the CSSOM technique
distinguishes all three; a substring search collapses the first two).

## Rationale

REQ-72-2/3's Given/When/Then reads "the ... block specifically is
inspected (not a whole-file substring search)." CSSOM rule lookup
(`document.styleSheets[0].cssRules`, filtered by `rule.selectorText`,
then `rule.style.getPropertyValue(...)`) is the literal implementation of
that sentence: it can only match a declaration that lives inside the
named selector's own parsed rule, so a declaration relocated to an
unrelated selector — the exact regression the after-proposal hunt finding
that shaped REQ-72-2/3 was guarding against — fails the assertion instead
of passing on a text-substring coincidence. `getComputedStyle` (already
used elsewhere in the file for the 24px-min-box tests) was considered and
rejected for these two REQs specifically because it asserts a strictly
stronger claim than the requirement text makes (cascade-winning value,
not "declared on this rule"); reusing it here would pass the letter of
the AC without matching the Given/When/Then's stated technique.
REQ-72-1 has no comparable alternative to weigh — a DOM parent-check
against `renderTable`'s output is the direct, unambiguous read of its
Given/When/Then.

## Plugin reflection plan

Per role directive's required record fields (issue-7 composing plugins):
phase-2's `docs/issue-78/reports/test-authoring.md` record will include
a suite-architecture note (why these three tests live in the existing
`test_dashboard_dom.py` module rather than a new file — reuse of its
jsdom/subprocess convention, per xunit-suite-patterns), the fixture
strategy already surveyed above (`_run_dom_js`/`_board_payload`/
`_dashboard_html_with_css`, no new fixtures needed), an explicit
EP/BVA citation matching the Adopted methodology section above
(ep-bva-technique), and one traceability line per test linking it to its
REQ id (traceability-line) — satisfied structurally by each test's name
and in-body comment citing `REQ-72-1`/`REQ-72-2`/`REQ-72-3`, verifiable
via `grep -r "REQ-72-" test/`.

## Deliberately out of scope

- No visual/layout assertion (`offsetWidth`/`scrollWidth`/screenshot) —
  the requirements record already excludes this technique on purpose,
  and jsdom cannot compute real layout regardless.
- No change to any existing test in the file, or to `src/**`.
- The requirements record's named residual gap (a future regression from
  a *new* wide element whose intrinsic width `min-width: 0` doesn't
  shrink) stays unaddressed — out of scope by that record's own
  disposition, not this role's to reopen.
- No new test file and no new fixture — reuses
  `test/rsb_tests/test_dashboard_dom.py`'s existing machinery per the
  traceability matrix's named downstream file.

## How it will be known to work

- `grep -r "REQ-72-" test/` matches all three IDs.
- `python3 -m pytest test/rsb_tests/test_dashboard_dom.py -q` passes, all
  three new tests executed (not skipped — the `node`/jsdom skip guards
  are environment-conditional; confirmed present-and-working in this
  checkout during the survey).
- `git show --stat` on the phase-2 commit(s) shows only additive hunks
  under `test/`.
- Sanity check during phase 2: temporarily revert each fix line (the
  `.table-scroll` wrapper, each CSS declaration) one at a time and
  confirm only the matching new test fails, then restore.

## What did not work

(none yet — appended live during phase 2 if anything breaks)

## Sources

Sources: `docs/issue-72/reports/requirements-engineering.md`,
`test/rsb_tests/test_dashboard_dom.py`,
`src/rsb/web/dashboard.js:205`, `src/rsb/web/dashboard.css:219,412-414`.
