# Conformance-review proposal (issue #36)

Scope: check the merged step-1 implementation (PR #37,
`issue-36/implementation`, squashed to `main` as commit `b621082`)
against issue #36's 7 acceptance-criteria checkboxes plus the two
numbered 요구사항 that no checkbox covers, working from the artifact and
the issue text directly per this role's phase-2 mandate — deliberately
**not** from `docs/issue-36/reports/implementation.md`'s self-report of
what was done. That self-report and this role's own survey are read only
to orient where to look; see
`docs/issue-36/reports/conformance-review/survey.md`.

## Method

Phase 2 will produce `docs/issue-36/reports/conformance-review.md` as a
per-requirement verdict table using `review-traceability`'s
`finding-record` skill: one row per sub-requirement below, verdict ∈
{Present, Surface, Absent, Incorrect, Unverifiable}, an evidence pointer
(file:line, test name, command + output, live-URL fetch, or "no local
means to observe"), and a rationale. `review-severity`'s
`severity-classification` is applied only to findings that are not
Present, if any survive, and per its own trigger condition — not as a
blanket pass over every row.

No sampling is needed: the touched surface is small (~165 changed lines
across `dashboard.js`, `dashboard.css`, `test_model.py`, and two spec
files — see the survey's §1 file table) and every touched line is in
scope for a full check. The requirement list below is therefore a full
enumeration, not a derivation.

Each of the issue's 7 acceptance criteria is decomposed into its
independently-checkable sub-facts, following this repo's issue-23 /
issue-27 / issue-29 precedent rather than issue-34's 1:1 form, because
the survey found that three of them (AC1, AC2, AC3) each bundle more
than one verifiable claim, and because two numbered 요구사항 (#3 ↗
removal, #2's "새 토큰 추가 금지" clause) have no corresponding checkbox
and would otherwise go unchecked. **No verdicts are assigned here** —
only the verification method each requirement will use.

Three method choices are adopted from the scout brief
(`docs/issue-36/reports/conformance-review/scout-brief.md`), each with
its source:

- **Executed-evidence rule** — a skipped test is *blocked*, not passed
  (ISTQB glossary; pytest #3730), so phase 2 runs
  `npm install --prefix test` before the suite and reports skip counts
  before and after. Adopted because survey O3 found all four disclosure
  DOM tests currently skip for want of `test/node_modules`.
- **Colour checked by computation, not by eye** — G183 requires 3:1
  between link text and surrounding body text as well as 4.5:1 against
  the background (https://www.w3.org/WAI/WCAG22/Techniques/general/G183),
  so R1c computes both from the declared token values.
- **`aria-controls` judged on IDREF correctness, not presence** — APG
  makes the attribute optional and support is weak, but a resolving-to-
  the-wrong-element IDREF asserts a false relationship
  (https://www.w3.org/TR/wai-aria-1.2/#aria-controls). Adopted because
  survey O4 found the attribute fixed to `detail-panel-slot` in both
  layout branches.

Two are deliberately **skipped**: WCAG 2.5.5 (AAA, 44px) and SC 3.2.5
new-tab warning are not made pass/fail criteria — issue #36 asks for
neither and both are contested in the sources
(https://adrianroselli.com/2020/02/link-targets-and-3-2-5.html); they may
appear as observations only. Visual-regression tooling is not adopted —
it is outside this role's write-set and the sandbox's means, so the
honest output for an unobservable layout claim is `Unverifiable`, never a
proxy metric.

## Requirement list

**R1 — 이슈/PR 번호가 `#<n>` 파란 링크로 보이고 GitHub 으로 이동한다
(AC1; 요구사항 1, 2).**
- R1a: the helper renders the number itself as the anchor text
  (`#<n>`), not a sibling icon.
  - Method: read `src/rsb/web/dashboard.js:223-227` (`numberLinkHtml`)
    and `:218-221` (`buildGithubUrl`); confirm the emitted string's text
    node is `#<n>` and the `href` is `https://github.com/<owner>/<kind>/<n>`.
- R1b: all six enumerated columns use it — Decision-queue Issue and PR,
  Flows Issue and PRs, Sessions Issue, Accounting Issue.
  - Method: read `dashboard.js:243` and `:254` (the two direct call
    sites) and the six transitive sites `:266`, `:267`, `:300`, `:304`,
    `:316`, `:333`; confirm each column named in 요구사항 1 reaches one
    of them, and that none is left rendering a bare number.
- R1c: "파란색" is the existing `color-action-primary-background` token,
  and the resulting link is actually distinguishable.
  - Method: read `dashboard.css:248-251` for the `color:` declaration;
    resolve the token chain through `:23` → `:9`; compute the WCAG
    contrast of `#2563eb` on `--color-neutral-0` `#ffffff` (`:3`) and
    the G183 3:1 delta against `--color-text-primary` `#111827` (`:21`,
    `:8`); confirm the hover/focus non-colour cue at `:252-255`.
- R1d: the link navigates to GitHub for real.
  - Method: fetch `https://tokenmaxxxer.github.io/repo-status-board/`
    and grep the served `dashboard.js` for the `.number-link` anchor
    construction; fetch `api/board.json` and confirm
    `owner_name_by_repo` is present and non-null for at least one repo,
    so the deployed page produces real hrefs rather than the R4
    fallback. If the network is unavailable, R1d resolves as
    `Unverifiable` and says so, rather than inferring navigation from
    the source.
- R1e: `kind` is correct per column — `"issues"` for issue numbers,
  `"pull"` for PR numbers.
  - Method: `dashboard.js:243` vs `:254`; note that
    `test_model.py:313-336` covers only `kind="issues"`, so the `"pull"`
    path has no test evidence and is judged from source alone.

**R2 — Flows 표에서 줄바꿈 없이 한 줄에 표시된다 (AC2).**
- R2a (core reading — the Issue column, which the issue's 배경 §2 names
  as the observed defect): the toggle+link pair cannot break across
  lines.
  - Method: read `dashboard.css:237-242` (`.issue-cell`, `inline-flex` +
    `white-space: nowrap`) and confirm `dashboard.js:243` applies that
    wrapper to every Issue cell. Per the scout brief, CSS-rule
    inspection evidences the *mechanism*, not the rendered outcome —
    the verdict states which of the two it rests on.
- R2b (secondary reading — the AC says "Flows 표에서", and the Flows PRs
  column also holds numbers): whether the PRs column is likewise
  protected.
  - Method: read `dashboard.js:253-255` (`<span class="mono">` per PR,
    joined `", "`) and `dashboard.css:84` (`.mono` sets `font-family`
    only); check for any other rule constraining that column.
- R2c (likely Unverifiable-within-this-environment): the rendered Flows
  Issue cell does not in fact wrap at the deployed column width.
  - Method: no browser or layout engine exists here — jsdom implements
    no CSS layout. Phase 2 will attempt a live fetch of the deployed
    page for the served CSS, and will record explicitly that no rendered
    observation was possible, rather than reading the verdict off the
    rule.

**R3 — 상세 패널을 키보드만으로 열고 닫을 수 있다, 행 클릭 회귀 없음
(AC3; 요구사항 4).**
- R3a: the trigger is a real, focusable native control.
  - Method: read `dashboard.js:237-239` — confirm
    `<button type="button">`, not a `<div>`/`<span>`/`<a>` with a click
    handler, and that no `tabindex` is imposed.
- R3b: `aria-expanded` is present in **both** states and reflects the
  actual state after activation.
  - Method: read `dashboard.js:237-239` (interpolated from `expanded`)
    and `:200-207` (`isRowExpanded`); execute
    `test/rsb_tests/test_dashboard_dom.py::test_row_toggle_click_opens_detail_and_flips_aria_expanded`
    and `::test_row_toggle_click_only_affects_its_own_table` and report
    pass/skip.
- R3c: activating the already-expanded trigger closes it (toggle, not
  one-way open).
  - Method: read `dashboard.js:555-556`; execute
    `::test_row_toggle_reactivating_open_button_closes_it`.
- R3d: no regression to whole-row clicking (the issue's explicit
  prohibition).
  - Method: read `dashboard.js:178-182` and `:465` (no `data-*`, no
    listener on any `<tr>`) and `:549-573` (handler bound to
    `.row-toggle` only); execute
    `::test_row_toggle_click_on_non_button_cell_does_not_open_detail`.
- R3e: the accessible name survives the move to an icon-only glyph, and
  disambiguates per row.
  - Method: read `dashboard.js:238` — `aria-label="Toggle details for
    issue {n}"` on the button, `aria-hidden="true"` on the `<span>`
    holding ▸/▾. Note that no test asserts either attribute.
- R3f: `aria-controls` semantics are "maintained" per 요구사항 4 — the
  IDREF resolves, and resolves to the element actually shown.
  - Method: read `dashboard.js:238` (fixed `aria-controls="detail-panel-slot"`),
    `src/rsb/web/index.html:25` (the element exists), and
    `dashboard.js:485-526` (`applySelectionLayout`: below the 1200px
    breakpoint the slot is emptied and the panel is inserted as a
    sibling `<tr class="detail-row">` instead). Judge IDREF correctness
    per layout branch, per the adopted method above.
- R3g (likely Unverifiable-within-this-environment): a keyboard-only user
  can actually reach and operate the control in a browser.
  - Method: jsdom does not synthesise `click` from Enter/Space on a
    `<button>`, so the DOM harness cannot demonstrate key-driven
    activation; the claim rests on native-element semantics plus DOM
    order (button then link, two tab stops, `dashboard.js:243`). Phase 2
    states that basis explicitly instead of claiming an observed
    keyboard run.

**R4 — owner/name 없는 레코드가 깨진 링크를 만들지 않는다 (AC4;
요구사항 5).**
- R4a: absent owner/name yields plain `#<n>` text with no anchor.
  - Method: read `dashboard.js:219` (`buildGithubUrl` returns `null` for
    falsy/non-string) and `:225`; execute
    `test_model.py::test_dashboard_js_number_link_html_falls_back_to_plain_text_without_owner_name`.
- R4b: the fallback is reachable from real data, not only from a direct
  helper call.
  - Method: read `dashboard.js:589` (`data.owner_name_by_repo || {}`) and
    the six call sites' `ownerNameByRepo[...]` lookups — an unknown repo
    key yields `undefined`, which R4a's guard must catch.
- R4c: no *other* malformed href is produced by the same path.
  - Method: read `dashboard.js:220,226` — confirm the `href` is escaped
    at the attribute boundary, and record (as an observation, not a #36
    verdict) that no URL-scheme allow-list exists and that
    `dashboard.js:267` can pass a null PR number into the helper.

**R5 — 기존 테스트 전부 통과 (AC5).**
- R5a: the suite passes.
  - Method: run `npm install --prefix test` first, then
    `python3 -c "import sys; sys.path.insert(0, 'src'); import pytest; sys.exit(pytest.main(['test/', '-q']))"`
    from the repo root; record the full pass/fail/skip counts verbatim.
- R5b: no test was left *un-executed* in the area the change touches.
  - Method: compare skip counts before and after the npm install; per
    the adopted executed-evidence rule, a skipped disclosure test is
    reported as blocked, never folded into "all pass". If the install
    cannot complete, R5b is `Unverifiable` and R5a's verdict names the
    8 unexecuted tests explicitly.
- R5c: the two tests the change added actually exercise the change.
  - Method: read `test_model.py:313-336`; note the `kind="pull"` and
    `rowToggleButtonHtml`/`prCellHtml`/`issueToggleCell` coverage gaps.
- R5d: there is no CI signal being relied on.
  - Method: read `.github/workflows/deploy-board.yml` — confirm it has
    no `pull_request`/`push` trigger and runs no tests, so AC5 rests
    entirely on the local run above.

**R6 — 스펙 문서가 실제 구현과 일치 (AC6; 요구사항 6).**
- R6a (spec → code): every concrete claim the specs now make about the
  Issue/PR cell is true of the code.
  - Method: extract each claim from `docs/specs/screen-spec.md:60-69`,
    `:78-81`, `:89-92`, `:97`, `:115-124`, `:128`, `:222-227` and
    `docs/specs/design-system.md:179`, `:163-165`, `:183`, and name the
    proving `dashboard.js`/`dashboard.css` line for each. Includes the
    token-name exactness check: screen-spec.md:65 writes
    `color-action-primary-*` where design-system.md:179 and
    `dashboard.css:249` name `color-action-primary-background`, and
    `dashboard.css:257` uses the primitive `--color-blue-500` for the
    focus outline.
- R6b (code → spec): behaviour the code has that the specs do not
  describe.
  - Method: sweep the changed code for user-visible behaviour with no
    spec sentence — e.g. `target="_blank"` new-tab opening
    (`dashboard.js:226`), and the below-1200px `tr.detail-row` branch's
    interaction with `aria-controls` (`:522-525`).
- R6c (residual-mention sweep): no stale ↗ / `.external-link`
  description survives.
  - Method: grep both spec files for `↗` and `external-link`. Record the
    survey's O6 finding that neither file contained either token at
    `b621082^`, so this half of 요구사항 6 had no work to do — and say
    that plainly rather than scoring it as satisfied work.
- R6d (independence): the spec edit is not treated as its own evidence.
  - Method: since `b621082` changed spec and code together, every R6a
    claim is proved against code, never against the sibling spec text.

**R7 — PR 본문에 closing 키워드 금지 (AC7).**
- R7a: PR #37's body contains no GitHub closing keyword (`close`,
  `closes`, `closed`, `fix`, `fixes`, `fixed`, `resolve`, `resolves`,
  `resolved`) followed by an issue reference, including inside backticks.
  - Method: `gh pr view 37 --json body` and inspect the raw text.
- R7b: the same holds for the merged commit message body.
  - Method: `git log -1 --format=%B b621082`.

**R8 — ↗ 아이콘 제거, `.external-link` 앵커/스타일 정리 (요구사항 3; no
corresponding AC).**
- R8a: no `.external-link` anchor is emitted and no `.external-link`
  rule survives.
  - Method: grep `src/` for `external-link` and for the literal `↗`;
    confirm any remaining hit is a source comment, not emitted markup or
    a live selector.

**R9 — 새 토큰 추가 금지 (요구사항 2, second clause; no corresponding
AC).**
- R9a: no new design token was introduced by `b621082`.
  - Method: diff `dashboard.css`'s `:root` block across `b621082^..b621082`
    and cross-check `docs/specs/design-system.md` §2 for added rows;
    confirm `.number-link` consumes only pre-existing tokens.

## How this will be judged

Phase 2 is judged complete when, and only when, all of the following are
externally verifiable from the record file alone:

- Every one of R1a–R9a above has exactly one verdict row, with no
  requirement silently dropped and no verdict outside
  {Present, Surface, Absent, Incorrect, Unverifiable}.
- Every non-`Unverifiable` row carries a concrete evidence pointer that a
  third party can re-open — a `file:line`, a named test, or a command
  with its recorded output. Every `Unverifiable` row instead names what
  access or observation was missing.
- The recorded pytest invocation and its verbatim pass/fail/**skip**
  counts appear in the record, and no skipped test is described as
  passing.
- Requirements the issue placed out of scope (survey O1's five unlinked
  number renderings, O7's URL-scheme gap, O9's null-PR path) appear as
  named scope notes, not as silent omissions and not as #36 defects.
- Any non-Present finding is addressed to the owning role (the
  `implementation` role for `src/`, `test/`, and `docs/specs/`), with no
  patch made by this role.

## Out of scope for this role

- **Fixing anything found** — per contract, conformance-review records
  findings; it does not patch `src/`, `test/`, or `docs/`. Any
  non-Present verdict hands off to a follow-up issue or to the
  implementation role, matching this repo's
  `docs/issue-4/reports/conformance-review.md` and
  `docs/issue-23/reports/conformance-review.md` precedent.
- **Holistic code-quality judgment** — this role renders per-requirement
  fidelity verdicts only. Readability, structure, and design taste in
  `b621082` are not scored.
- **Re-deciding the design** — 요구사항 4 delegated the trigger's new
  position and form to the implementation proposal. This role checks that
  the shipped trigger keeps the semantics the issue required, not whether
  a leading ▸/▾ button was the best available choice.
- **Execution observation** — step 2's sibling role
  (`execution-observation`) covers whether the deployed board behaves
  correctly in use. Where this review hits an unobservable claim (R2c,
  R3g), it records `Unverifiable` and leaves the observation to that
  role rather than reaching for it.
- **The five number renderings outside 요구사항 1's enumerated columns**
  (survey O1), the missing URL-scheme allow-list (O7), and the
  Decision-queue null-PR path (O9) — noted as observations for a
  possible follow-up issue, not judged as #36 requirements.

## Deliverable

`docs/issue-36/reports/conformance-review.md`: one row per R1a–R9a above
(30 sub-requirements — R1a–e, R2a–c, R3a–g, R4a–c, R5a–d, R6a–d, R7a–b,
R8a, R9a), each with a verdict from
{Present, Surface, Absent, Incorrect, Unverifiable}, an evidence pointer,
and a rationale; plus a findings section, severity-classified where that
skill's trigger condition applies, for any non-Present row.

Gated behind a human approval per role-handoff contract v3 §19 — not
produced by this phase-1 PR. Phase 2 opens only via a PR review Approve
from a `docs/specs/approvers.md` account (JiwonJung94, jjongkwann) other
than this PR's author, or — in single-account mode — an issue-level
comment on issue #36 whose entire body is exactly
`APPROVE issue-36/conformance-review`, posted by one of those accounts.
