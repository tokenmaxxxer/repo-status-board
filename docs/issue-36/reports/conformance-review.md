# Conformance-review record (issue #36)

loop_state: reported

## What was done

Checked the merged step-1 implementation of issue #36 against the issue's
7 acceptance-criteria checkboxes plus the two numbered 요구사항 that no
checkbox covers, decomposed per the approved phase-1 proposal into the 30
sub-requirements R1a–R9a. Verdicts were derived from direct inspection of
`src/`, `docs/specs/`, the PR body and the merged commit message, from a
fresh local test run this session (including a `npm install --prefix test`
that the phase-1 survey had found missing), and from live fetches of the
deployed board — **not** from `docs/issue-36/reports/implementation.md`'s
self-report of what was done. That self-report was not read for verdict
purposes.

Headline: **26 Present, 3 Surface, 1 Absent, 2 Unverifiable** — that is 32
verdicts across 30 sub-requirements, because R3c and R3f each carry two
verdicts (one for the artifact under review, one for current `main`; see
"Subject artifact" below). Every #36 acceptance criterion is met by the
change that delivered it. Six findings are recorded, **none of which is a
defect in the #36 change itself**: two are regressions that later commits
introduced into surfaces #36 established, and four are gaps of degree.

## Upstream basis and approval provenance

Rests on `docs/issue-36/proposals/conformance-review.md` (this role's
approved phase-1 proposal, requirement list R1–R9),
`docs/issue-36/reports/conformance-review/survey.md`, and
`docs/issue-36/reports/conformance-review/scout-brief.md`, all committed in
phase 1 as `41d894f` and opened as PR #55.

Phase 2 was opened by an issue-level comment on issue #36 whose entire body
is exactly `APPROVE issue-36/conformance-review`, posted by `jjongkwann`
(association `member`), which is one of the two accounts listed in
`docs/specs/approvers.md` (`JiwonJung94`, `jjongkwann`). This is the
single-account path of role-handoff contract v3 §19: PR #55's author and
the approver are the same account, so the issue-comment string-equality
path — not a PR-review Approve — is the applicable one. String equality was
checked, not prose interpretation. No near-miss or affirmative-sounding
non-matching comment was found on the issue; the two other comments present
are the exact-string approvals for the sibling roles
(`APPROVE issue-36/implementation`, `APPROVE issue-36/execution-observation`),
which are not this role's gate and were not treated as such.

No `src/`, `test/`, or `docs/specs/` file is modified by this record. This
role reports; it does not fix.

## Subject artifact — and why two commits are cited

The #36 implementation is PR #37 (`issue-36/implementation`), squash-merged
to `main` as **`b621082`** ("issue-36 phase 1: link-as-text proposal +
row-toggle relocation (#37)"; the squash folded that PR's phase-1 and
phase-2 commits into one, so its message carries both `Subject: issue-36`
trailers). That commit is the artifact under review.

Two commits merged to `main` **after** `b621082` touch the same surface,
and the phase-1 survey — written against the working tree, i.e. `main`'s
tip — did not separate them out:

| Commit | Issue | What it changed on this surface |
|---|---|---|
| `f353910` | #38 | Added `applySelectionLayout()`, the `WIDE_LAYOUT_QUERY`/`window.matchMedia` breakpoint branch, the `tr.detail-row` narrow-layout path, and the P1-4 focus moves to `dashboard.js` |
| `b2f6b63` | #44 | Created `test/rsb_tests/test_dashboard_dom.py` (+259 lines) and `test/package.json`, i.e. the entire jsdom DOM harness |

Neither existed at `b621082`. Every verdict below is therefore rendered
against `b621082` — the code that actually delivered #36 — and, wherever
current `main` diverges in a way that bears on a #36 acceptance criterion,
the row says so and attributes the divergence to the commit responsible.
Line references are to `main`'s tip unless suffixed `@b621082`. Attribution
was established experimentally, not inferred: the #44 harness was copied
into a detached worktree at `b621082` and run there (see Appendix A3).

## Method

`review-traceability`'s `finding-record` verdict set (Present / Surface /
Absent / Incorrect / Unverifiable), one verdict per sub-requirement, each
with an evidence pointer a third party can re-open and a one-line
rationale. `review-severity`'s `severity-classification` is applied to the
six non-Present findings only — not as a blanket pass over every row —
using this repo's own precedent adaptation
(`docs/issue-4/reports/conformance-review.md`,
`docs/issue-29/reports/conformance-review.md`) of a deterministic
four-band lookup for this non-security context, in the Microsoft bug-bar
shape (fixed lookup over observable characteristics of the finding) rather
than a DREAD-style averaged score: **Blocking** (defeats the requirement's
purpose or misleads the operator), **Major** (spec violation,
user-visible, does not defeat the requirement's core purpose), **Minor**
(spec violation, cosmetic/non-blocking), **Note** (not itself a proven
spec violation — an observation worth flagging).

Three method choices carried over from the approved proposal and its scout
brief, each honoured here:

- **Executed-evidence rule** — a skipped test is *blocked*, not passed. The
  suite was run before and after `npm install --prefix test`, and both skip
  counts are recorded verbatim (Appendix A1). The install succeeded this
  session, so nothing in the touched area remained unexecuted.
- **Colour checked by computation, not by eye** — WCAG contrast computed
  from the declared token values, against both the 4.5:1 text floor and
  G183's 3:1 link-vs-body-text delta.
- **`aria-controls` judged on IDREF correctness, not presence** — the
  attribute is optional per APG, but an IDREF resolving to the wrong
  element asserts a false relationship.

Two checks were deliberately **skipped** and are not pass/fail criteria
here, as the proposal stated: WCAG 2.5.5 (AAA, 44px) and SC 3.2.5's
new-tab warning. Visual-regression tooling was not adopted; where a claim
required rendered layout, the verdict is `Unverifiable`, never a proxy
metric.

## R1 — 번호가 `#<n>` 파란 링크로 보이고 GitHub 으로 이동한다 (AC1; 요구사항 1, 2)

| Requirement | spec_ref | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R1a: the number itself is the anchor text (`#<n>`), not a sibling icon | issue #36, 요구사항 1 ("번호를 링크로") | Present | `src/rsb/web/dashboard.js:223-227` (`numberLinkHtml`), `:218-221` (`buildGithubUrl`) | The emitted string is `<a class="number-link" href="…">#<n></a>`: the text node is the number, and no sibling element is emitted alongside it |
| R1b: all six enumerated columns use it | issue #36, 요구사항 1 (enumeration: Decision queue Issue+PR, Flows Issue+PRs, Sessions Issue, Accounting Issue) | Present | `dashboard.js:266` (Decision Issue), `:267` (Decision PR), `:300` (Flows Issue), `:304` (Flows PRs), `:316` (Sessions Issue), `:333` (Accounting Issue) — all reaching `numberLinkHtml` via `:243` or `:254` | All six enumerated columns route through the helper; none is left rendering a bare number |
| R1c: "파란색" is the existing `color-action-primary-background` token and the link is actually distinguishable | issue #36, 요구사항 2 | Present | `dashboard.css:249` (`color: var(--color-action-primary-background)`) → `:23` → `:9` (`#2563eb`); hover/focus underline `:252-255`; focus outline `:256-259` | Computed: `#2563eb` on `--color-neutral-0` `#ffffff` = **5.17:1** (≥4.5:1); G183 delta against `--color-text-primary` `#111827` = **3.43:1** (≥3:1), and an underline appears on `:hover`/`:focus`, so colour is not the sole distinguisher |
| R1d: the link navigates to GitHub for real | issue #36, AC1 ("GitHub 으로 이동한다") | Present | Live fetch, HTTP 200: deployed `dashboard.js:226` serves the `.number-link` anchor; deployed `api/board.json` carries `owner_name_by_repo` with 3 entries, all non-null (`on-the-record`, `repo-status-board`, `tokenmaxxxer-core` → `tokenmaxxxer/…`) | The deployed page runs the new helper and the deployed payload supplies real owner/name values, so hrefs on the live board resolve to real GitHub URLs rather than the R4 fallback |
| R1e: `kind` is correct per column | issue #36, 요구사항 1 | Present | `dashboard.js:243` passes `"issues"`; `:254` passes `"pull"` | Matches GitHub's canonical paths (`/issues/<n>`, `/pull/<n>`). Judged from source alone: `test_model.py:313-336` exercises only `kind="issues"` — see F6 |

## R2 — Flows 표에서 줄바꿈 없이 한 줄에 표시된다 (AC2)

| Requirement | spec_ref | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R2a: the toggle+link pair in the Issue column cannot break across lines | issue #36, AC2 + 배경 §2 (the observed defect: ↗ dropping below the number in Flows) | Present | `dashboard.css:237-242` (`.issue-cell { display: inline-flex; … white-space: nowrap; }`), applied at `dashboard.js:243` to every Issue cell including Flows (`:300`) | The mechanism that prevents the reported break is present and reaches the column the issue named. This evidences the *rule*, not the rendered result — the rendered claim is R2c |
| R2b: the Flows PRs column is likewise protected | issue #36, AC2 ("Flows 표에서", unrestricted as to column) | **Absent** | `dashboard.js:304` → `prCellHtml` `:251-256` emits `<span class="mono">…</span>` per PR joined by `", "`; `dashboard.css:84` defines `.mono` as `font-family` only; no `white-space`/`inline-flex` rule covers that column | Nothing addresses wrapping in the Flows PRs column. A multi-PR cell can still break between comma-separated numbers. See F3 |
| R2c: the rendered Flows Issue cell does not in fact wrap at the deployed column width | issue #36, AC2 | **Unverifiable** | No browser or layout engine is available in this sandbox; jsdom implements no CSS layout, so the DOM harness cannot measure a line box. The deployed page and stylesheet were fetched as text (HTTP 200) but not rendered | Missing access is a rendering engine, named here rather than substituted with a proxy metric. Left to the sibling `execution-observation` role |

## R3 — 상세 패널을 키보드만으로 열고 닫을 수 있다, 행 클릭 회귀 없음 (AC3; 요구사항 4)

| Requirement | spec_ref | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R3a: the trigger is a real, focusable native control | issue #36, 요구사항 4 ("키보드로 도달·조작 가능한 실제 컨트롤") | Present | `dashboard.js:237-239` — `<button type="button" class="row-toggle" …>`, no `tabindex` imposed | A native `<button>`, not a `<div>`/`<span>`/`<a>` with a click handler; focusable and activatable by keyboard by element semantics |
| R3b: `aria-expanded` is present in both states and reflects state after activation | issue #36, 요구사항 4 ("기존 `aria-expanded`… 유지") | Present | `dashboard.js:238` (interpolated from `expanded`), `:199-207` (`isRowExpanded`); `test_dashboard_dom.py::test_row_toggle_click_opens_detail_and_flips_aria_expanded` **passes at `b621082`** (Appendix A3) and, at `main`, passes its `before == "false"` and `afterExpanded == "true"` assertions before failing on a later, unrelated assertion (Appendix A2) | The attribute is rendered in both states and observed flipping false→true on activation in both code states |
| R3c: activating the already-expanded trigger closes it | issue #36, AC3 ("열고 닫을 수 있다") | Present **@b621082** · see F1 for current `main` | `dashboard.js:555-556`; `::test_row_toggle_reactivating_open_button_closes_it` **passes at `b621082`** (Appendix A3). At `main` the same test fails, but an instrumented run with `window.matchMedia` supplied returns `aria-expanded="false"` after the second activation in **both** layout branches (Appendix A4) | Toggle-to-close is implemented and observed. The `main` failure is an environment-dependent throw introduced later, not a missing close path — see F1 |
| R3d: no regression to whole-row clicking | issue #36, 주의 ("행 전체 클릭으로 되돌리는 것은 금지") | Present | `dashboard.js:178-182` (dead `<tr>` data attributes removed), `:549-551` (listener bound to `.row-toggle` only; no `<tr>` listener anywhere); `::test_row_toggle_click_on_non_button_cell_does_not_open_detail` **passes at both `b621082` and `main`** | The prohibited pattern is absent in source and disproved by an executed test in both code states |
| R3e: the accessible name survives the move to an icon-only glyph and disambiguates per row | issue #36, 요구사항 4 (트리거 재배치, semantics 유지) | **Surface** | `dashboard.js:238` — `aria-label="Toggle details for issue ${issue}"` on the button, `aria-hidden="true"` on the ▸/▾ `<span>` | A name exists and survives the glyph-only move, so the shape is there; but the same issue number renders a button in up to four tables (`:266`, `:300`, `:316`, `:333`), producing up to four controls with the identical accessible name and no table qualifier. See F4 |
| R3f: `aria-controls` resolves, and resolves to the element actually shown | issue #36, 요구사항 4 ("기존 … `aria-controls` 시맨틱 … 유지") | Present **@b621082** · **Incorrect** at current `main` · see F2 | `dashboard.js:237-238` (fixed `aria-controls="detail-panel-slot"`), `src/rsb/web/index.html:25` (the element exists). At `b621082` the panel was always written to that element (`dashboard.js:559@b621082`). At `main`, `applySelectionLayout` `:519-525` empties `#detail-panel-slot` and inserts the panel as a sibling `tr.detail-row` below the 1200px breakpoint | At the artifact under review the IDREF pointed at the one container that ever held the panel. `f353910` added a branch in which it points at a deliberately-emptied element while the panel lives elsewhere — a false relationship |
| R3g: a keyboard-only user can actually reach and operate the control in a browser | issue #36, AC3 ("키보드만으로") | **Unverifiable** | jsdom does not synthesise a `click` from Enter/Space on a `<button>`, so the DOM harness cannot demonstrate key-driven activation; no browser is available. The supporting basis is native `<button>` semantics plus DOM order — button then link, two tab stops, `dashboard.js:243` | Missing access is a real user agent. Stated as a basis, not claimed as an observed keyboard run. Left to `execution-observation` |

## R4 — owner/name 없는 레코드가 깨진 링크를 만들지 않는다 (AC4; 요구사항 5)

| Requirement | spec_ref | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R4a: absent owner/name yields plain `#<n>` text with no anchor | issue #36, 요구사항 5 | Present | `dashboard.js:218-219` (`buildGithubUrl` returns `null` for falsy/non-string), `:225` (fallback returns escaped `#<n>`); `test_model.py::test_dashboard_js_number_link_html_falls_back_to_plain_text_without_owner_name` → **PASSED** (`1 passed in 0.08s`) | Guard and fallback are present and covered by an executed test; no `<a>` is emitted on that path, so no link can be broken |
| R4b: the fallback is reachable from real data, not only from a direct helper call | issue #36, 요구사항 5 | Present | `dashboard.js:589` (`data.owner_name_by_repo \|\| {}`) and the six `ownerNameByRepo[…]` lookups at `:266`, `:267`, `:300`, `:304`, `:316`, `:333` | An absent key yields `undefined`, which R4a's falsy guard catches; an absent payload key yields `{}`, so every repo takes the fallback rather than throwing |
| R4c: no other malformed href is produced by the same path | issue #36, 요구사항 5 ("깨진 링크 금지") | Present | `dashboard.js:220` (scheme/host are a fixed `https://github.com/` literal, not caller-supplied), `:226` (`href="${escapeHtml(url)}"` — escaped at the attribute boundary) | The URL's scheme and host cannot be influenced by payload data, and the attribute boundary is escaped. Two adjacent gaps are observations, not #36 defects — see Observations O2 and O3 |

## R5 — 기존 테스트 전부 통과 (AC5)

| Requirement | spec_ref | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R5a: the suite passes | issue #36, AC5 | Present | At `b621082` (the artifact under review), pristine worktree: **`55 passed in 2.89s`** — 0 failed, 0 skipped (Appendix A3). At current `main`: **`2 failed, 63 passed in 6.81s`** (Appendix A2) | The change under review left the suite fully green. Both `main` failures are in a test file that did not exist at `b621082` and are attributed to `f353910` — see F1 |
| R5b: no test was left un-executed in the area the change touches | issue #36, AC5, read under the executed-evidence rule | Present | Before `npm install --prefix test`: `57 passed, 8 skipped`, all 8 skipping with `SKIPPED [8] test/rsb_tests/test_dashboard_dom.py:65: jsdom is not installed; run 'npm install --prefix test' first`. After the install (`added 38 packages … found 0 vulnerabilities`): 0 skipped, all 65 executed (Appendix A1) | The survey's O3 blockage was cleared this session rather than reported as a pass. At `b621082` the question is moot: 0 tests skipped there |
| R5c: the two tests the change added actually exercise the change | issue #36, AC5 | **Surface** | `test_model.py:313-336` adds `…number_link_html_renders_blue_link_when_owner_name_present` and `…falls_back_to_plain_text_without_owner_name`, both `kind="issues"`; `dashboard.js:681` exports only `buildGithubUrl`/`numberLinkHtml` of the new helpers | Tests exist and pass, but cover one of the change's four new/rewritten helpers. `rowToggleButtonHtml` `:237`, `issueToggleCell` `:241`, and `prCellHtml` `:251` are unexported and therefore unreachable from this harness, and `kind="pull"` is untested. See F6 |
| R5d: there is no CI signal being relied on | issue #36, AC5 | Present | `.github/workflows/deploy-board.yml` is the only workflow; `on:` is `schedule: cron "*/30 * * * *"` + `workflow_dispatch`; no step invokes pytest, npm, or npm test | No `pull_request`/`push` trigger and no test step exists, so AC5 rests entirely on a local run — which is why R5a records one at both commits |

## R6 — 스펙 문서가 실제 구현과 일치 (AC6; 요구사항 6)

| Requirement | spec_ref | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R6a (spec → code): every concrete claim the specs make about the Issue/PR cell is true of the code | `docs/specs/screen-spec.md` §1.3 (Issue cell para), §1.4, §1.5, §1.7; `docs/specs/design-system.md` §5 `DataTable` row | Present | Claim-by-claim: screen-spec `:60-64` (leading icon-only `row-toggle`, ▸/▾, `aria-expanded`, `aria-controls="detail-panel-slot"`, `aria-label="Toggle details for issue {n}"`) ↔ `dashboard.js:237-239`; `:65-66` (number as `#<n>` link, plain text without owner/name) ↔ `dashboard.js:243`, `:225`, `dashboard.css:248-249`; `:67-68` ("Not a clickable `<tr>`") ↔ `dashboard.js:549-551`; `:68-69` (PR column same rule, no disclosure button) ↔ `dashboard.js:267`, `:251-256`; `:90-91` (Flows) ↔ `:300`, `:304`; `:97` (Sessions) ↔ `:316`; `:128` (Accounting) ↔ `:333`; design-system `:179` (▸/▾, no colour token, 24×24px, `.number-link` on `color-action-primary-background`) ↔ `dashboard.css:212-228`, `:248-249` | Every concrete spec claim about this cell has a proving line in the shipped code. One imprecision, not a mismatch: screen-spec `:65` writes the wildcard `color-action-primary-*` where design-system `:179` and `dashboard.css:249` name `color-action-primary-background` exactly |
| R6b (code → spec): behaviour the code has that the specs do not describe | `docs/specs/screen-spec.md` §1.3, §2.6 | **Surface** | `dashboard.js:226` emits `target="_blank" rel="noopener noreferrer"`; grep of `docs/specs/` for `_blank`, `noopener`, "new tab", "새 탭" returns no hits | Links open in a new browser tab — a user-visible behaviour with no sentence in either spec, so the spec describes the implementation incompletely. See F5 |
| R6c (residual-mention sweep): no stale ↗ / `.external-link` description survives | issue #36, 요구사항 6 ("↗ 형태 … 서술을 … 갱신") | Present, with a stated caveat | `git grep 'external-link\|↗' b621082^ -- docs/specs/` → no hits; the same grep at `main` → no hits | The end state is correct, but this half of 요구사항 6 had **no work to do**: neither spec file ever described the ↗ form, so its premise was false. Recorded plainly rather than scored as satisfied work (the phase-1 survey's O6) |
| R6d (independence): the spec edit is not treated as its own evidence | method constraint, phase-1 proposal §"How this will be judged" | Present | Every R6a claim above names a `dashboard.js`/`dashboard.css` line as its proof; no spec sentence is cited as evidence for another spec sentence | `b621082` changed spec and code in one commit, so spec text was used only as the claim under test, never as its own proof |

## R7 — PR 본문에 closing 키워드 금지 (AC7)

| Requirement | spec_ref | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R7a: PR #37's body contains no closing keyword followed by an issue reference | issue #36, AC7 (issue #23 T2) | Present | `gh pr view 37 --json body`, raw body inspected: the only issue references are `for #36` and the literal `APPROVE issue-36/implementation`. The words "fix"/"fixes" occur only as "fix the `aria-controls`/`aria-expanded` wiring gaps found in the survey" — no `<keyword> #<n>` pair, inside or outside backticks | No token sequence GitHub parses as a closing directive is present; corroborated by issue #36 still being OPEN after PR #37 merged |
| R7b: the same holds for the merged commit message body | issue #36, AC7 | Present | `git log -1 --format=%B b621082`: "Fixes the pre-existing aria-expanded/aria-controls wiring gaps…" and "fixes two issues an adversarial hunt pass found" — neither followed by an issue reference; the only references are the squash header's `(#37)` (a PR number) and two `Subject: issue-36` trailers | Closing keywords appear as ordinary English verbs with no adjacent issue reference, so none forms a parseable pair; issue #36 remaining OPEN confirms none was parsed |

## R8 — ↗ 아이콘 제거, `.external-link` 앵커/스타일 정리 (요구사항 3)

| Requirement | spec_ref | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R8a: no `.external-link` anchor is emitted and no `.external-link` rule survives | issue #36, 요구사항 3 | Present | `grep -rn 'external-link\|↗' src/` → two hits, both source comments: `dashboard.js:210` and `dashboard.css:244`, each naming the ↗ icon as the thing replaced. The `.external-link` rule block is deleted in `git diff b621082^..b621082 -- src/rsb/web/dashboard.css`. Deployed assets agree: served `dashboard.css` has no `external-link` match, served HTML has no `↗` | Neither emitted markup nor a live selector remains; the surviving occurrences cannot render, and the removal is visible in the diff and on the deployed board |

## R9 — 새 토큰 추가 금지 (요구사항 2, second clause)

| Requirement | spec_ref | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R9a: no new design token was introduced by `b621082` | issue #36, 요구사항 2 ("새 토큰 추가 금지") | Present | `git diff b621082^..b621082 -- src/rsb/web/dashboard.css \| grep -E '^\+ *--[a-z]'` → no output (no custom property declared). The same commit's `docs/specs/design-system.md` diff is a single line in the §5 component table, adding no §2 token-table row. `.number-link` consumes `--color-action-primary-background` and `--color-blue-500`; `.issue-cell` consumes `--space-1` | No `:root` declaration was added, and the two new rules consume only pre-existing tokens |

## Open findings

Six non-Present findings. **None is a defect introduced by the #36 change.**
F1 and F2 are regressions that a later commit introduced into surfaces #36
established; F3–F6 are gaps of degree in #36's own delivery. All are
addressed to the `implementation` role, which owns `src/`, `test/`, and
`docs/specs/`. No patch is made here.

### F1 — `window.matchMedia` is called unguarded, and the throw kills every row-toggle listener

- **Severity: Major.** Lookup: user-visible (the disclosure control stops
  responding after one activation); reachable in a default scenario for any
  user agent lacking `matchMedia`; not a permanent/destructive state. It is
  not Blocking because every browser that can render this board ships
  `matchMedia`, so the deployed board is not believed to be affected.
- **Owner:** `implementation` role. **Introduced by:** `f353910` (issue
  #38), not by #36.
- **Rows:** R3c, R5a. **Evidence:** `dashboard.js:520` calls
  `window.matchMedia(WIDE_LAYOUT_QUERY)` with no guard, from
  `applySelectionLayout`, which `renderData` calls at `:642` — *before*
  `attachRowToggleHandlers` at `:643`. Under the #44 harness (jsdom, where
  `typeof window.matchMedia === "undefined"`) the resulting `TypeError:
  window.matchMedia is not a function` propagates out of the click handler
  at `:557`, aborting `renderData` mid-flight. The re-rendered buttons
  therefore never get listeners: after the first activation the control is
  inert, and `#detail-panel-slot` stays empty (Appendix A4, `native` run).
- **Consequence today:** `main`'s test suite is red —
  `::test_row_toggle_click_opens_detail_and_flips_aria_expanded` and
  `::test_row_toggle_reactivating_open_button_closes_it` fail (Appendix
  A2). Supplying `matchMedia` makes both behaviours correct in both layout
  branches (Appendix A4), so the product logic is sound and the exposure is
  the unguarded call plus the harness gap. Whether the fix belongs in
  `src/` (guard the call) or in `test/` (stub `matchMedia` in the harness)
  is the owning role's decision, not this record's.

### F2 — `aria-controls` asserts a false relationship in the narrow-layout branch

- **Severity: Minor.** Lookup: a spec/semantics violation that is
  user-visible only to assistive-technology users following the
  relationship; `aria-controls` support is weak across screen readers, and
  the panel is still reachable by reading order, so it does not defeat the
  disclosure's purpose.
- **Owner:** `implementation` role. **Introduced by:** `f353910` (issue
  #38), not by #36.
- **Row:** R3f. **Evidence:** `dashboard.js:238` hard-codes
  `aria-controls="detail-panel-slot"`. At `main`, `applySelectionLayout`
  `:519-525` takes a branch below the 1200px breakpoint that sets
  `DETAIL_SLOT.innerHTML = ""` and inserts the panel as a sibling
  `tr.detail-row` instead. The IDREF then resolves to a deliberately-empty
  element while the controlled content lives elsewhere in the DOM. At
  `b621082` no such branch existed (`dashboard.js:559@b621082` wrote the
  panel into that element unconditionally), so #36 shipped a correct IDREF.
- **Also unspecified:** `docs/specs/screen-spec.md` §1.3 states the
  `aria-controls="detail-panel-slot"` value as fact without noting that the
  narrow-layout branch relocates the content, so the spec does not describe
  the branch either.

### F3 — the Flows PRs column has no wrap protection

- **Severity: Minor.** Lookup: a spec violation under AC2's unrestricted
  reading ("Flows 표에서"), cosmetic, and the column the issue's 배경
  actually named as defective (Issue) is fixed.
- **Owner:** `implementation` role. **Row:** R2b (Absent).
- **Evidence:** `dashboard.js:304` → `prCellHtml` `:251-256` joins
  `<span class="mono">` elements with `", "`; `dashboard.css:84` gives
  `.mono` a `font-family` and nothing else. No rule constrains wrapping in
  that column, so a Flows row with several PRs can break between numbers —
  the same class of defect AC2 was written to eliminate, one column over.
  A single-PR cell is short enough that this is unlikely to show.

### F4 — the disclosure button's accessible name is not unique across tables

- **Severity: Minor.** Lookup: a semantics gap, user-visible to
  screen-reader users navigating by control, non-blocking (each button
  still has *a* name and works).
- **Owner:** `implementation` role. **Row:** R3e (Surface).
- **Evidence:** `dashboard.js:238` builds
  `aria-label="Toggle details for issue ${issue}"` from the issue number
  alone, while the same issue can render a button in all four tables
  (`:266`, `:300`, `:316`, `:333`). The `data-table` attribute that
  disambiguates them programmatically is not reflected in the name, so a
  user listing controls hears "Toggle details for issue 7" up to four times
  with no way to tell which table each belongs to — even though
  `isRowExpanded` `:199-207` treats them as genuinely distinct controls.

### F5 — new-tab opening is undocumented

- **Severity: Note.** Lookup: not itself a proven violation of a #36
  requirement (the issue asks for a link, not for a target), but a
  documented-behaviour gap against AC6's "스펙 문서가 실제 구현과 일치".
- **Owner:** `implementation` role. **Row:** R6b (Surface).
- **Evidence:** `dashboard.js:226` emits
  `target="_blank" rel="noopener noreferrer"`; no occurrence of `_blank`,
  `noopener`, "new tab", or "새 탭" exists anywhere under `docs/specs/`.
  `rel="noopener noreferrer"` is the correct companion to `target="_blank"`,
  so the code is not wrong — only undescribed.

### F6 — the change's own tests cover one of its four new helpers

- **Severity: Minor.** Lookup: a coverage gap, not a behaviour defect; the
  untested paths were verified correct here by inspection, so nothing is
  known-broken behind it.
- **Owner:** `implementation` role. **Row:** R5c (Surface).
- **Evidence:** `test_model.py:313-336` adds two tests, both
  `kind="issues"`. `dashboard.js:681`'s `module.exports` list omits
  `rowToggleButtonHtml` `:237`, `issueToggleCell` `:241`, and `prCellHtml`
  `:251`, so the node-based unit harness cannot reach them at all, and no
  test passes `kind="pull"` despite `:254` depending on it. The four
  disclosure DOM tests that do exercise the button arrived later, from
  issue #44 (`b2f6b63`).

## Observations — out of scope for #36, recorded rather than dropped

These are named scope notes, not verdicts and not #36 defects.

- **O1 (survey O1) — five number renderings sit outside 요구사항 1's
  enumeration** and are correctly left unlinked: the issue enumerated six
  columns and this review scored exactly those six. Nothing was silently
  widened.
- **O2 (survey O7) — `escapeHtml` covers five characters only**
  (`dashboard.js:25-29`). It is sufficient at the two boundaries #36 uses
  it for (`href` attribute value and element text), and the URL's scheme
  and host are a fixed literal at `:220`, so no scheme-injection path
  exists. There is no URL allow-list; that is a pre-existing design choice,
  not a #36 regression.
- **O3 (survey O9) — the Decision-queue PR cell always passes a
  one-element array** (`dashboard.js:267`, `prCellHtml([d.pr])`). A `null`
  `pr` would survive the `length === 0` guard and render `#null` linking to
  `…/pull/null`. `src/rsb/model.py:16` types `pr: int`, so triggering this
  requires a payload that violates the model; it is not reachable from
  conformant data and is not a #36 requirement.
- **O4 — a documented contrast figure is inaccurate, conservatively.**
  `docs/specs/design-system.md:64-65` states `neutral-0` on `blue-500` =
  4.6:1; computed from the declared hex values (`#ffffff` / `#2563eb`) the
  ratio is **5.17:1**. The claim understates the true value, so nothing
  fails a floor because of it. Pre-existing; §2.2 was not touched by
  `b621082`.
- **O5 — `${issue}` is interpolated unescaped** into `aria-label` and
  `data-issue` at `dashboard.js:238`, where the sibling `repo` is escaped.
  Issue numbers are integers in `model.py`, so this is a robustness
  asymmetry, not a live defect.
- **O6 — `test/node_modules/` is untracked and not ignored.** `.gitignore`
  has no `node_modules` entry, so the `npm install --prefix test` that
  `test_dashboard_dom.py:65` instructs the developer to run leaves 38
  packages showing as untracked in `git status`. Owned by issue #44's
  harness work; noted because this review had to run that install.

## Next steps

1. **This PR (#55) carries no further work.** The review is complete: all
   30 sub-requirements carry a verdict, and this record is the deliverable.
   The next act is the user's — merge to accept, or close unmerged to
   refuse.
2. **Nothing here is fixed by this role, and nothing should be.** No
   follow-up commit to `src/`, `test/`, or `docs/specs/` belongs on this
   branch; the hand-off below is the route.
3. **The `Unverifiable` pair (R2c, R3g) travels to the sibling role.**
   Step 2's `execution-observation` session for issue #36 has the standing
   to observe rendered layout and real keyboard operation; this record does
   not pre-empt what it will find.
4. **F1 is the one item with present-tense consequence**: `main`'s test
   suite is red right now, and a reader who runs `pytest` after
   `npm install --prefix test` will see it. Whoever picks that up should
   know from this record that it is not #36's doing.

## Open-finding resolution path

Findings are handed off; they are not resolved here, and this role does not
open issues (contract v3: requirements enter as issues authored by the user
only).

| Finding | Severity | Addressed to | Resolution path |
|---|---|---|---|
| F1 | Major | `implementation` (issue #38's surface, harness half issue #44's) | Needs a new user-authored issue against `f353910`'s `matchMedia` call and/or the #44 harness. Until then it stands recorded and unresolved; it is out of #36's subject, so it cannot be fixed under this issue's branch |
| F2 | Minor | `implementation` (issue #38's surface) | Same route as F1 — a user-authored issue covering `aria-controls` under the narrow-layout branch, plus the matching `screen-spec.md` §1.3 sentence |
| F3 | Minor | `implementation` | In #36's own subject. Either a follow-up issue extending AC2 to the Flows PRs column, or the user's explicit decision that AC2's narrow reading (Issue column only) was the intended one — in which case F3 closes as won't-fix and this row records why |
| F4 | Minor | `implementation` | In #36's own subject. A follow-up issue on the `aria-label`, or an accepted-as-is decision; either way the verdict on R3e stays `Surface` in this record |
| F5 | Note | `implementation` | Smallest path: one sentence in `screen-spec.md` §1.3 stating new-tab opening, under whichever issue next touches that spec. Not worth an issue of its own |
| F6 | Minor | `implementation` | Naturally resolved by issue #44's DOM-harness work if that work extends to `kind="pull"` and the three unexported cell helpers; otherwise a follow-up issue |

Re-review trigger: if any finding above is disputed, this role records the
dispute and re-examines the evidence against the same artifact — a disputed
finding is re-rated, never silently dropped. If a fix lands for F1–F6, the
verdict rows they attach to (R2b, R3c, R3e, R3f, R5a, R5c, R6b) are the
ones a re-review re-runs.

## Appendix — commands and verbatim output

All commands run from the repository root this session.

### A1 — suite before and after `npm install --prefix test` (at `main`)

Before (this session's first run, pre-install):

```
57 passed, 8 skipped in 3.11s
SKIPPED [8] test/rsb_tests/test_dashboard_dom.py:65: jsdom is not installed; run `npm install --prefix test` first
```

Install:

```
$ npm install --prefix test
added 38 packages, and audited 39 packages in 993ms
8 packages are looking for funding
found 0 vulnerabilities
```

### A2 — suite after the install (at `main`)

```
$ python3 -c "import sys; sys.path.insert(0, 'src'); import pytest; sys.exit(pytest.main(['test/', '-q', '-rs']))"
2 failed, 63 passed in 6.81s
```

Failures, both in `test/rsb_tests/test_dashboard_dom.py`:

```
test_row_toggle_click_opens_detail_and_flips_aria_expanded
  test_dashboard_dom.py:194: assert result["detailHasContent"] is True
  E  assert False is True
     (the preceding assertions -- before == "false", afterExpanded == "true" -- passed)

test_row_toggle_reactivating_open_button_closes_it
  test_dashboard_dom.py:244: assert result["expanded"] == "false"
  E  AssertionError: assert 'true' == 'false'
```

Restricted to the disclosure tests: `2 failed, 2 passed, 4 deselected in
2.45s` — `::test_row_toggle_click_only_affects_its_own_table` and
`::test_row_toggle_click_on_non_button_cell_does_not_open_detail` pass.

### A3 — the same harness run against the artifact under review

`git worktree add $TMPDIR/wt36 b621082`, then `test_dashboard_dom.py`,
`test/package.json`, and `test/node_modules` copied in unmodified from
`main` (the harness resolves `dashboard.js` as `parents[2]/src/rsb/web/`,
so it picks up the worktree's own source):

```
$ python3 -c "... pytest.main(['test/rsb_tests/test_dashboard_dom.py','-q','--no-header','-k','row_toggle'])"
4 passed, 4 deselected in 1.88s
```

Then, with the worktree returned to a pristine `b621082` (`git clean -xfd
test/`, removing the copied harness), the suite as it actually stood at
that commit:

```
$ python3 -c "... pytest.main(['test/','-q','--no-header','-rs'])"
55 passed in 2.89s
```

### A4 — instrumented probe isolating F1's mechanism (at `main`)

A throwaway jsdom driver, identical to the #44 harness except that
`window.matchMedia` is supplied, run against `src/rsb/web/dashboard.js`;
two synthetic activations of the same Decision-queue button. The probe file
was deleted after the run and is not committed.

```
narrow (matchMedia -> {matches:false}):
  {"initial":"false","afterClick1":"true","slotAfter1":false,"detailRowAfter1":true,
   "afterClick2":"false","slotAfter2":false,"detailRowAfter2":false}

wide   (matchMedia -> {matches:true}):
  {"initial":"false","afterClick1":"true","slotAfter1":true,"detailRowAfter1":false,
   "afterClick2":"false","slotAfter2":false,"detailRowAfter2":false}

native (jsdom's own window, no matchMedia):
  {"probe":{"typeofMatchMedia":"undefined","windowError":"window.matchMedia is not a function"},
   "initial":"false","afterClick1":"true","slotAfter1":false,"detailRowAfter1":false,
   "afterClick2":"true","slotAfter2":false,"detailRowAfter2":false}
  TypeError: window.matchMedia is not a function
      at applySelectionLayout (src/rsb/web/dashboard.js:520:30)
      at renderData (src/rsb/web/dashboard.js:642:3)
      at HTMLButtonElement.<anonymous> (src/rsb/web/dashboard.js:557:7)
```

Reading: with `matchMedia` present, open **and close** both work, and the
panel lands in the branch-appropriate container (`detailRow` when narrow,
`slot` when wide). Without it, the first activation leaves
`aria-expanded="true"` with no panel anywhere and the second does nothing —
exactly the two `main` failures in A2.

### A5 — deployed board (live fetches, all HTTP 200)

- `https://tokenmaxxxer.github.io/repo-status-board/` — no `external-link`
  and no `↗` in the served HTML.
- `…/dashboard.js:226` — serves the `.number-link` anchor; `:220` serves
  the `https://github.com/${ownerName}/${kind}/${number}` construction; the
  only `↗` is the comment at `:210`.
- `…/dashboard.css` — serves `.issue-cell` (`inline-flex`,
  `white-space: nowrap`) and `.number-link`
  (`color: var(--color-action-primary-background)`); no `external-link`
  match.
- `…/api/board.json` — `owner_name_by_repo` present with 3 entries, none
  null or empty.

### A6 — repository metadata

```
$ git log -1 --format='%H %an %ae' b621082
b6210821c55fbc108773f71f7adf12a427b1a097 이종관 jjongkwann@gmail.com

$ gh pr view 37 --json mergeCommit,headRefName,author
mergeCommit b6210821c55fbc108773f71f7adf12a427b1a097
headRefName issue-36/implementation
author      jjongkwann

$ git show --stat b621082   (code/spec portion)
 docs/specs/design-system.md   |  2 +-
 docs/specs/screen-spec.md     | 21 +-
 src/rsb/web/dashboard.css     | 36 ++-
 src/rsb/web/dashboard.js      | 106 +++++---
 test/rsb_tests/test_model.py  | 26 ++
```

### A7 — CI

`.github/workflows/deploy-board.yml`, the repository's only workflow:

```yaml
on:
  schedule:
    - cron: "*/30 * * * *"
  workflow_dispatch:
```

No `pull_request`/`push` trigger; no pytest, npm, or npm-test step in
either job.

## Hand-off

All six findings are addressed to the `implementation` role. F1 and F2
concern `f353910` (issue #38) and F1's harness half concerns `b2f6b63`
(issue #44) — both outside issue #36's subject, so neither is filed here as
a #36 defect and neither is fixed here. Filing follow-up issues is the
user's act, not this role's. R2c and R3g resolved `Unverifiable` for want of
a rendering engine and a real user agent respectively, and both are left to
the sibling `execution-observation` role rather than guessed at favourably.
