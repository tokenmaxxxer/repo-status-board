# Conformance-review survey (issue #56, phase 1)

Subject: issue #56. Branch: `issue-56/conformance-review`. Current-state
survey only — no verdicts, no pass/fail, no quality judgment. Everything
below is a located fact or a named unknown; the verdicts it feeds wait
for the approved proposal and phase 2.

## Artifact under review

- PR #57 (`issue-56/implementation`), **MERGED** 2026-08-04, merge commit
  `93a60b3`, delivery commit **`21c2359`** ("issue-56 phase 2:
  renderErrors 제거 + .number-link 24px 최소 크기 + 문서 편입").
- PR #57 carried phase 1 and phase 2 in one PR: `71a0dff` is the phase-1
  proposal commit, `21c2359` the phase-2 delivery. Phase 2 opened on the
  issue-level comment whose entire body is `APPROVE issue-56/implementation`
  (author `jjongkwann`, an `docs/specs/approvers.md` account) — single-
  account mode per contract v3 s19. The provenance is recorded here as
  located, not endorsed.
- `git show --stat 21c2359`: 6 files, +261 / −20.

| File | ± | Surface it belongs to |
|---|---|---|
| `docs/issue-56/reports/implementation.md` | +209 | the building role's own record (not an acceptance surface) |
| `docs/specs/design-system.md` | +7/−4 (net +3) | acceptance check 4, second half |
| `docs/specs/screen-spec.md` | +10/−5 (net +5) | acceptance check 4, first half |
| `src/rsb/web/dashboard.css` | +9 | acceptance check 3 |
| `src/rsb/web/dashboard.js` | −13 | acceptance check 2 |
| `test/rsb_tests/test_dashboard_dom.py` | +33 | acceptance check 1 |

The mapping is 1:1 onto issue #56's four acceptance checkboxes with no
file left over, so the requirement list can be a full census rather than
a sample.

## The specification side

Issue #56 states three 요구사항, one 제약, and four `check:` acceptance
lines. The acceptance lines are the checkbox set the R-rows will follow
in order; the 요구사항/제약 sentences carry obligations the checkboxes do
not fully restate (notably 요구사항 2's "**실측**해 기록으로 보고" and the
제약's "PR #43 이 랜딩한 나머지 8개 AC 구현은 무변경"), so they need their
own row group.

Upstream basis for the issue itself: `docs/issue-38/reports/execution-observation.md`
F1 (`:247-261`, the third always-visible error surface) and F3
(`:320-334`, the `.number-link` measurement promised by
`docs/issue-38/proposals/implementation.md:310-312` and never reported).
Both are quoted by the issue's 배경 section; they are the yardstick's
provenance, not a second yardstick.

## What the delivered commit changed, per surface

**`dashboard.js` (−13).** `renderErrors(errors)` (formerly `:355-365`)
deleted in full, and its interpolation `${renderErrors(data.errors)}`
removed from `renderData`'s `MAIN.innerHTML` template between the
Sessions and Hygiene sections (formerly `:632`). Nothing else in the
template moved. `renderErrors` now appears nowhere under `src/` — the
only surviving occurrence anywhere in code is a prose mention in the new
test's comment (`test/rsb_tests/test_dashboard_dom.py:252`).

**`dashboard.css` (+9).** `.number-link` (`:248-260`) gained a 4-line
comment plus `min-width: 24px`, `min-height: 24px`, `display: inline-flex`,
`align-items: center`, `justify-content: center`. `.row-toggle`
(`:212-228`), the pattern the acceptance line names, carries the same
five declarations plus `background: none`, `border: none`, `font: inherit`,
`color: inherit`, `cursor: pointer`, `padding: 0`, `text-align: left`.
Untouched: `.error-list` still has rules at `:347-349`, under a comment
that still reads `/* HygieneListItem / ErrorListItem */`.

**`screen-spec.md` (net +5).** `### 1.9 Errors panel — ErrorListItem`
and its two bullets deleted; §2.5 gained a five-line bullet naming the
partial-failure banner as "the only surface that displays partial-failure
repo errors (issue #56 F1)". Section numbering elsewhere is unaffected —
§1.9 was the last `###` under §1, and a repo-wide grep for `§1.9` returns
zero hits, so no cross-reference dangles. §3 Traceability table refers to
H1/H2/H3 hypotheses only.

**`design-system.md` (net +3).** §5's closing paragraph gained a sentence
stating issue #56 extends the 24×24px minimum to `.number-link`; the §6
`DataTable` inventory row gained ", 24×24px minimum size per issue #56 F3".
Untouched: §5's parenthetical enumeration still reads "every interactive
control (`row-toggle`, `repo-filter`, `refresh-button`)", and §6 still
carries a standalone `| ErrorListItem | status-error |` row (`:189`)
whose only screen-spec home was the §1.9 that this commit deleted.

**`test_dashboard_dom.py` (+33).** One new test,
`test_partial_failure_raw_message_absent_from_main_content_and_errors_section_gone`,
plus an 8-line comment block tracing it to issue #38 F1. It drives the
real `dashboard.js` under jsdom with an errors payload whose message
embeds the sentinel `internal-path-should-not-leak: /srv/provider/internal.py refused`
and asserts four things: `mainContentHasRawMessage is False`,
`errorsHeadingExists is False`, `errorListExists is False`,
`bannerHasCollapsedMessage is True`.

## Verification surfaces available today

- **Source reading** at `21c2359` / current `main` — available for every
  file above.
- **Grep/`node --check`** — available.
- **Test execution** — the suite is runnable, but `test/node_modules/` is
  **absent** in this worktree, and `test/rsb_tests/test_dashboard_dom.py`
  skips its whole module without jsdom (the same condition
  `docs/issue-38/reports/conformance-review.md:89-94` hit, reported as
  "57 passed, 8 skipped"). `npm install --prefix test` is what
  `docs/issue-36/reports/conformance-review.md` Appendix A1 did to make
  the DOM rows executable; without it every acceptance-check-1 row would
  be Unverifiable for want of a harness rather than for want of a browser.
- **Rendering engine** — none. No Chrome/Chromium, no Playwright/Selenium/
  Puppeteer (`docs/issue-38/reports/implementation.md:104-123`;
  `docs/issue-56/reports/implementation.md` restates it). Any row whose
  claim is *rendered pixel geometry* cannot be settled here.

## Evidence gaps and unknowns

1. **Assertion scope vs. the checkbox's wording.** The acceptance line
   says "**문서-범위** 단언". The new test scopes its raw-message assertion
   to `document.getElementById("main-content")`. `src/rsb/web/index.html`
   puts `<div id="partial-banner">` at `:20` and `<main id="main-content">`
   at `:24` — **siblings**, so the banner's contents are outside
   `mainContent.textContent` by construction. Whether "문서-범위" is met by
   a `#main-content`-scoped assertion, and whether the assertion could
   fail if `renderErrors` were restored, are two distinct questions and
   both are open. The test's own comment claims the scope is "document-
   scoped to `#main-content` itself (not to any one child element within
   it)"; that claim is on the record and is checkable.
2. **`실측` vs. determination.** Issue #56 요구사항 2 asks for a
   measurement ("실측해 기록으로 보고"). The delivered CSS comment
   (`dashboard.css:251-254`) and the record argue from the WCAG exception
   *text* and the DOM context, not from a measured box. Whether the
   substitution is disclosed per-criterion — the exact deficiency issue
   #38 F3 was raised about — is open.
3. **Pattern fidelity.** `.number-link` copies five of `.row-toggle`'s
   declarations and omits seven. Whether any omission weakens the 24×24
   guarantee (e.g. `padding: 0` absent, inherited padding unknown) is
   unread; and `.number-link` renders in two different parents —
   `.issue-cell` (`dashboard.js:243`), itself `display: inline-flex`, and
   `<span class="mono">` (`:254`) — so the flex-item-vs-inline question
   differs per context.
4. **Removal residue.** Three artifacts of the removed feature survive:
   `.error-list` CSS (`dashboard.css:347-349`), its comment header, and
   the `ErrorListItem` row in `design-system.md:189`. Whether any of them
   falls inside issue #56's four checkboxes (or only inside 요구사항 1's
   "통합/제거") is a decomposition decision the proposal must make, not a
   verdict.
5. **제약 (no-change to PR #43's other 8 ACs).** The diff is small enough
   to check exhaustively, but "unchanged" needs an operational reading:
   byte-identical for the other AC surfaces, or behaviourally unchanged.
   The `renderData` template edit and the `.number-link` box-model change
   both sit *inside* files that other ACs also own.
6. **Regression baseline.** `main` currently fails 2 tests in
   `test_dashboard_dom.py`. Per this session's instruction these are the
   pre-existing unguarded-`matchMedia` defect introduced by `f353910`,
   attribution already settled in
   `docs/issue-36/reports/conformance-review.md` Appendix A4 (`:441-471`)
   and finding F1 (`:196-221`). This survey cites that attribution and
   does not re-derive it; what remains open is only whether `21c2359`
   changed the count.

## Adjacent role records already on main

- `docs/issue-38/reports/execution-observation.md` — source of F1/F3, the
  two gaps issue #56 exists to close.
- `docs/issue-36/reports/conformance-review.md` — the `matchMedia`
  attribution (F1, Appendix A4) and the house Appendix convention.
- `docs/issue-38/reports/conformance-review.md` — 60-row precedent,
  evidence classes A/B/C, `## Unverifiable rows and what would settle each`.
- `docs/issue-56/reports/implementation.md` — the building role's own
  record. Read for **claims to re-verify**, never as evidence of its own
  conformance (yardstick independence).
- The sibling `execution-observation` role runs on issue #56 in parallel
  (실행 계획 step 2, `‖`). Trajectory/process judgment is that role's
  territory; this survey stays on artifact-vs-spec.

## Open unknowns for the scout pass to aim at

- How strong audits judge a **regression test's power**, not its presence
  — the gap in unknown 1.
- What a **removal-class** conformance audit is expected to sweep — the
  gap in unknown 4.
- The **primary** WCAG 2.5.8 exception wording, so unknown 2 is judged
  against the standard rather than against the record's paraphrase.

## Write-set for this role

Phase 1 (this commit, three files):

- `docs/issue-56/reports/conformance-review/survey.md` — this file.
- `docs/issue-56/reports/conformance-review/scout-brief.md`
- `docs/issue-56/proposals/conformance-review.md`

Phase 2 (after an approvers.md Approve, one file):

- `docs/issue-56/reports/conformance-review.md`

No `src/`, `test/`, or `docs/specs/` file is touched by this role in
either phase — it reports verdicts and does not fix.

## Warrant hunt

After-proposal dispatch, stance 0 (bypassability of the gate just
touched), 60s tier (docs-only write set). Outcome: FINDING — see
`hunt.md` in this directory and the proposal's closing section. Docs-only
fast path applies: **no before-landing dispatch** for this phase-1
landing, per the directive's docs-only rule.

Approval state at the time of this survey, checked and recorded rather
than assumed: `gh issue view 56 --json comments` returns exactly two
comments, `APPROVE issue-56/implementation` (2026-08-04) and
`APPROVE issue-56/execution-observation` (2026-08-08), both by
`jjongkwann`. **Neither names this role.** No
`APPROVE issue-56/conformance-review` exists and no PR review exists on
any conformance-review PR, so phase 2 is closed and this commit is the
whole of phase 1.
