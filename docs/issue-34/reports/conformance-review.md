# Conformance-review record (issue #34)

loop_state: reported

## What was done

Two verdict passes over issue #34's 7 acceptance-criteria checkboxes,
both worked from the artifact and the issue text directly — not from
`docs/issue-34/reports/implementation.md`'s self-report.

- **Pass 1 (2026-08-03, shipped in PR #40)** — checked PR #35
  (`issue-34/implementation`) as merged to `main` at `5d05b5f`.
- **Pass 2 (2026-08-04, this update)** — re-checked the same 7
  requirements against `main` at `b2f6b63` (merged into this branch),
  because the shipped implementation of this very feature changed after
  pass 1: issue-36 (`b621082`, PR #37) rewrote the link markup
  (`.external-link` trailing icon → `.number-link` on the `#<n>` number
  itself) and moved the detail-panel click listener off the whole `<tr>`
  onto the `.row-toggle` button; issue-38 (`f353910`, PR #43) added a
  `window.matchMedia`-driven detail-panel placement; issue-44
  (`b2f6b63`, PR #45) added a jsdom DOM-layer test harness. A verdict
  recorded against `5d05b5f` no longer describes what the board serves,
  so pass 2 re-derives all 7.

Pass 2 evidence was produced this session by: direct code reads of
`src/rsb/model.py`, `src/rsb/render.py`, `src/rsb/web/dashboard.js`; two
throwaway `node`+jsdom probes that load the shipped, unmodified
`dashboard.js` against a real DOM and dispatch real clicks (one against a
synthetic payload, one against the **live deployed** `board.json`); a
live `curl` of `https://tokenmaxxxer.github.io/repo-status-board/api/board.json`
(HTTP 200, `generated_at` `2026-08-04T05:38:47Z`); two full test-suite
runs (with and without `jsdom` installed); and a read of PR #35's body
text via `gh pr view 35 --json body`. The probe files were deleted after
use — this role changes no `src/`/`test/` file.

## Why

Issue #34's own acceptance-criteria checklist is the spec; this role's
mandate (contract v3 §19) is a per-requirement verdict for that checklist
against what actually shipped to `main`, independent of the building
role's account. Pass 2 exists because "what shipped" moved: three later
issues edited the exact code paths issue #34's ACs describe.

## Upstream basis

Rests on `docs/issue-34/proposals/conformance-review.md` (this role's
approved phase-1 proposal, requirement list R1–R7) and
`docs/issue-34/reports/conformance-review/survey.md`, approved via issue
#34 comment `APPROVE issue-34/conformance-review` (jjongkwann, listed in
`docs/specs/approvers.md`; single-account mode — this PR's author ==
approver — so the issue-comment path of contract v3 §19 applies, exact
string match). Subject artifact for pass 2: `main` at `b2f6b63`
(i.e. PR #35 as subsequently amended by PR #37/#43/#45).

Method: `review-traceability`'s `finding-record` verdict set (Present /
Surface / Absent / Incorrect / Unverifiable), one row per requirement,
kept 1:1 with issue #34's 7 checkboxes per the approved proposal's
framing, each with an evidence pointer and rationale.
`review-severity`'s `severity-classification` is applied to the one open
finding, using Microsoft's four-level bug bar
(Critical/Important/Moderate/Low) adapted for this non-security context —
the same bar pass 1 used.

Method substitution, stated plainly: the approved proposal's R2/R3/R4
"click it in a real browser" methods could not run (no browser in this
sandbox). Pass 2 substitutes DOM-level exercise — jsdom 30.0.1 loaded as
`global.window`/`global.document` before `require()`-ing the shipped
`dashboard.js`, then real `HTMLElement.click()` dispatch against the
rendered rows. This is weaker than a human click-through for
paint/navigation concerns and stronger than pass 1's code-read-only
evidence for event-wiring concerns; where it is the only evidence, the
row says so.

## R1–R7

Pass 2 verdict is the operative one. The pass-1 column is kept so the
delta is traceable.

| # | Requirement (issue #34 수용 기준) | Pass 1 (`5d05b5f`) | Pass 2 (`b2f6b63`) | Evidence (pass 2) | Rationale |
|---|---|---|---|---|---|
| R1 | "board.json 의 각 레코드에서 owner/name 을 얻을 수 있다" | Present | **Present** | `src/rsb/model.py:110` (`BoardModel.owner_name_by_repo`), `:267` (`owner_name = payload.get("repo")`), `:271`, `:294` (`merge_repos()` population); `src/rsb/render.py:174` (`render_json_model()` emits `owner_name_by_repo`); `test/rsb_tests/test_model.py:89-105`, `test_render.py:50-54`, `test_webserver.py:41`; live fetch this session → `{"on-the-record": "tokenmaxxxer/on-the-record", "repo-status-board": "tokenmaxxxer/repo-status-board", "tokenmaxxxer-core": "tokenmaxxxer/tokenmaxxxer-core"}` | Unchanged by PR #37/#43/#45 — the propagation path is confirmed at every layer and the deployed payload carries non-null owner/name for all 3 configured repos, ~7h before this pass |
| R2 | "이슈 번호에서 GitHub 이슈로 이동한다 (3개 레포 모두)" | Present | **Present** | `src/rsb/web/dashboard.js:218-221` (`buildGithubUrl`), `:223-227` (`numberLinkHtml`), `:241-244` (`issueToggleCell`); 4 call sites — `:266` decisions, `:300` flows, `:316` sessions, `:333` accounting/ledger; jsdom probe rendering the **live** payload produced 74 `a.number-link` anchors, 0 malformed hrefs, issue links per repo: `tokenmaxxxer/on-the-record` 35, `tokenmaxxxer/tokenmaxxxer-core` 23, `tokenmaxxxer/repo-status-board` 11; every anchor `target="_blank" rel="noopener noreferrer"` | Markup changed shape since pass 1 (the `#<n>` number *is* the link now, no trailing ↗ icon) but the requirement is unchanged and met in all 4 tables. "3개 레포 모두" is now evidenced by real rendered hrefs for all three repos, not by the genericity argument alone. Actual browser navigation still unexercised (no browser); an `<a href>` with a well-formed absolute URL is deterministic markup, so this is not scored as a gap |
| R3 | "PR 번호(decision queue, flows PRs 열)에서 GitHub PR 로 이동한다" | Present | **Present** | `dashboard.js:251-256` (`prCellHtml`), call sites `:267` (decision queue, single PR) and `:304` (Flows PRs column, multi-PR); synthetic probe → decision cell `…/pull/101`, Flows cell `…/pull/102`, `…/pull/103` comma-joined; live-payload probe → `tokenmaxxxer/tokenmaxxxer-core` 4 pull links, `tokenmaxxxer/on-the-record` 1 | Both required sites route through the same `numberLinkHtml`; the multi-PR Flows cell renders one independent anchor per number. `repo-status-board` had no PR-bearing row in the live payload at fetch time, so its PR links are covered by the synthetic probe only — noted, not scored as a gap (no per-repo branching exists in the code path) |
| R4 | "상세 패널을 여는 기존 동작이 회귀하지 않는다 (클릭·키보드 모두)" | Incorrect | **Present** | `dashboard.js:549-572` (`attachRowToggleHandlers` binds `click` **only** to `.row-toggle` buttons), re-attached after every re-render at `:643`; no `<tr>`-level listener remains (`grep -n addEventListener dashboard.js` → only `.row-toggle`, `#refresh-button`, `#repo-filter`, `#partial-retry`, `#retry-button`); no `keydown`/`keyup`/`keypress` handler exists anywhere in the file. jsdom probe, both layouts (`matchMedia` stubbed `matches:false` and `matches:true`): toggle click → `aria-expanded` `false`→`true`, 1 `.detail-panel` rendered (narrow: inserted `tr.detail-row`; wide: `#detail-panel-slot`); second toggle click → back to `false`, 0 panels; **clicking `a.number-link` leaves `aria-expanded` at `false` and renders 0 detail panels** | Pass 1's Incorrect verdict — activating the link also toggled the panel, because the click listener sat on the whole `<tr>` and nothing called `stopPropagation()` — no longer reproduces: issue-36 (`b621082`) moved the listener onto the button itself, which removes the coupling at the source rather than papering over it. Keyboard: the two controls are separate DOM siblings inside `.issue-cell` (native `<button>` first, native `<a href>` second), so they are two ordinary tab stops with their own default activation, and no key handler exists that could intercept either. Real-browser tab-through remains unexercised (no browser) — the DOM structure plus the absence of key handlers is the basis |
| R5 | "owner/name 없는 레코드가 깨진 링크를 만들지 않는다" | Present | **Present** | `dashboard.js:219` (falsy/non-string guard → `null`), `:225` (`numberLinkHtml` falls back to `escapeHtml("#" + number)`); `test/rsb_tests/test_model.py:313`, `:328` (link-present / plain-text-fallback cases); probe: `buildGithubUrl(null|""|123, …)` → `null`, `numberLinkHtml(null,"issues",5)` → `"#5"`; synthetic probe row with `owner_name_by_repo["repo-b"] = null` rendered Issue cell `…<button class="row-toggle">…</button>#9` and PR cell `<span class="mono">#202</span>` — zero anchors, zero `href="null"`/`href="undefined"` | The fallback is plain escaped text at both link sites, and it degrades per-repo (repo-a's links still render in the same table). The live board currently has no null-owner repo, so this path is evidenced by the synthetic probe and unit tests, not live |
| R6 | "기존 테스트 전부 통과" | Present | **Present** (with caveat, see finding) | This session on the merge of `main` `b2f6b63`: `python3 -c "import sys; sys.path.insert(0,'src'); import pytest; sys.exit(pytest.main(['test/','-q']))"` → **57 passed, 8 skipped, 0 failed** (the 8 skips are `test_dashboard_dom.py`'s, gated on `jsdom` being installed — the configuration CI actually runs). After `npm install --prefix test`, the same command → **63 passed, 2 failed** | Green in the configuration the project actually runs, and every test that existed at issue #34's delivery passes. The 2 failures appear only once the optional jsdom dependency is installed, are in tests added by issue-44 *after* this issue, and are caused by code added by issue-38 — not by issue #34's link work (root cause in the finding below). Scored Present for *this issue's* requirement; the failure is recorded and handed off rather than absorbed here |
| R7 | "주의: PR 본문에 closing 키워드 금지 (issue #23 T2 — 백틱 인용도 파싱됨)" | Present | **Present** | `gh pr view 35 --json body` re-fetched this session: the only `#34` occurrence is "Phase 1 (research/survey/proposal) for #34."; the only `clos*`/`fix*`/`resolv*` token anywhere in the body is the literal word "closure" (from `closure_sweep`), not adjacent to any issue reference | No closing keyword in any casing or backtick form binds to `#34`, so the issue was not auto-closed by PR #35's merge — which matches reality (issue #34 is still OPEN) |

## Open findings

Next steps: (1) merge decision on this PR by a human approver; (2) a
human files a follow-up issue for the jsdom-harness finding below —
roles never file issues, and this role never patches `src/`/`test/`.

Resolution path: the finding is addressed to the DOM-test-harness owner
(issue #44's test-authoring role, with issue-38's unguarded `matchMedia`
call as the co-located cause); it is handed off, not fixed here, and no
issue-#34 requirement is left open by it.

- **The jsdom DOM test harness fails 2 of its 8 tests in its own
  documented configuration (`npm install --prefix test`)**

  severity: Moderate

  `test_dashboard_dom.py` skips with "jsdom is not installed; run
  `npm install --prefix test` first". Following that instruction
  (jsdom 30.0.1) makes
  `test_row_toggle_click_opens_detail_and_flips_aria_expanded` and
  `test_row_toggle_reactivating_open_button_closes_it` fail. Root cause,
  reproduced directly this session: jsdom implements no
  `window.matchMedia` (`typeof new JSDOM("").window.matchMedia` →
  `undefined`), and `dashboard.js:520` calls it unguarded, so the first
  toggle click throws `TypeError: window.matchMedia is not a function`
  at `applySelectionLayout` (`:520`) ← `renderData` (`:642`) ← the
  button's own click listener (`:557`). The throw aborts `renderData`
  *before* `attachRowToggleHandlers` (`:643`) re-binds listeners, so the
  detail panel never renders (failure 1) and the re-rendered button has
  no listener at all, leaving `aria-expanded="true"` stuck (failure 2).
  Stubbing `window.matchMedia` in the same harness makes both scenarios
  behave correctly, which is what R4's Present verdict rests on.

  Moderate, not higher: no user-facing defect (real browsers implement
  `matchMedia`, and the live board is unaffected), but the harness is
  unusable as delivered, and because CI never installs jsdom the failure
  is invisible there — a new DOM test would be written against a
  permanently-red suite. Two candidate fixes for whoever picks it up
  (not chosen here): stub `matchMedia` in `_run_dom_js`'s program
  preamble, or guard the call site (`typeof window.matchMedia ===
  "function" ? … : false`).

## Resolved since pass 1

- **External-link click also toggles the detail panel (pass-1 R4,
  severity Low)** — resolved by issue-36 (`b621082`, PR #37), which
  binds the click listener to `.row-toggle` instead of the whole `<tr>`.
  Verified not to reproduce: clicking `a.number-link` in the jsdom probe
  leaves `aria-expanded="false"` with 0 detail panels rendered, in both
  the narrow and wide layout branches. No follow-up issue is needed for
  it.

## Scope notes

- Correction to pass 1's scope note: issue #34's requirement-4 prose
  "새 탭 여부도 결정해 문서화" **is** documented — the approved
  `docs/issue-34/proposals/implementation.md:90` fixes `target="_blank"`,
  and `docs/issue-36/proposals/implementation.md:76-77`, `:162`
  re-affirm it explicitly as a kept issue-#34 convention. Pass 1 recorded
  it as undocumented after looking only at `docs/issue-34/decisions/` and
  `docs/specs/`; that was too narrow a search and is withdrawn. It
  remains outside the R1–R7 table either way (it is prose, not one of
  the 7 checkboxes). `docs/specs/design-system.md:179` documents
  `.number-link`'s styling but not its new-tab behavior — a spec-prose
  gap, not an AC failure.
- `src/rsb/render.py` (CLI text renderer) links and additional GitHub API
  calls remain out of scope, per the issue body's own "범위 밖" section.
- Attribution is recorded where it differs from the reviewed subject
  (R4's fix, R6's caveat), because pass 2's subject is `main` as a whole,
  not PR #35 in isolation; no verdict here grades issue-36, issue-38 or
  issue-44's own acceptance criteria.
- Per contract, this record reports verdicts only; no `src/`/`test/`
  change is made by this role. It is this role's terminal phase-2
  deliverable for issue #34; next step is the human PR-merge decision on
  this PR (acceptance) or a requested revision on the same branch
  (feedback).
