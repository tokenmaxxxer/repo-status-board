# Conformance-review survey (issue #36)

Phase-1 current-state survey for the conformance-review role on issue
\#36. This file records *where the evidence lives* and *what constrains
the check* — it assigns no verdicts. Verdicts are phase-2 output and go
to `docs/issue-36/reports/conformance-review.md` only after an approval
per role-handoff contract v3 §19.

## 1. Target artifact

- Subject issue: **#36** — "링크 표기 변경 — ↗ 아이콘 대신 번호를 `#<n>`
  파란 링크로, 상세 트리거 재배치".
- Step 1 of the issue's execution plan (`implementation`) is **merged**:
  PR **#37** (`issue-36/implementation`), squashed to `main` as commit
  **`b621082`**, merged 2026-08-03T11:30:30Z. Its squash body carries
  both phase-1 and phase-2 sub-commits, so the merged commit is
  simultaneously the proposal and the built change.
- `b621082` touches 9 files:

  | File | ± |
  |---|---|
  | `docs/issue-36/proposals/implementation.md` | +176 |
  | `docs/issue-36/reports/implementation.md` | +280 |
  | `docs/issue-36/reports/implementation/scout-brief.md` | +106 |
  | `docs/issue-36/reports/implementation/survey.md` | +154 |
  | `docs/specs/design-system.md` | 2 (1 line rewritten) |
  | `docs/specs/screen-spec.md` | 21 |
  | `src/rsb/web/dashboard.css` | 36 |
  | `src/rsb/web/dashboard.js` | 106 |
  | `test/rsb_tests/test_model.py` | +26 |

- **`main` has moved since**: HEAD is `b2f6b63`. Two later merges touch
  surfaces this review must judge — `f353910` (issue #38, PR #43) and
  `b2f6b63` (issue #44, PR #45, which added
  `test/rsb_tests/test_dashboard_dom.py` and `test/package.json`).
  Consequence recorded in §4 O8: the *current* wording of
  `docs/specs/design-system.md:179` is not the wording `b621082` wrote.
  Phase 2 judges issue #36's acceptance criteria against **`main` as it
  stands**, and attributes each line to its originating commit before
  calling any drift a #36 defect.

## 2. Issue #36's requirements, verbatim

Six numbered 요구사항:

1. **번호를 링크로** — 이슈/PR 번호를 `#<n>` 텍스트의 `<a href>` 로 렌더링.
   대상은 issue #34 와 동일(Decision queue/Flows/Sessions/Accounting 의
   이슈 번호, Decision queue 의 PR, Flows 의 PRs 열).
2. **파란색** — `design-system.md` 의 기존 토큰
   `color-action-primary-background`(= `blue-500`) 사용. 새 토큰 추가 금지.
3. **↗ 아이콘 제거** — `.external-link` 앵커/스타일 정리.
4. **상세 패널 트리거 재배치** — 새 위치·형태를 제안서에서 결정하고 근거를
   남길 것. 기존 `aria-expanded`/`aria-controls` 시맨틱과 키보드 조작은 유지.
5. **owner/name 부재 시** — 링크 없이 `#<n>` 텍스트로만 표시.
6. **문서 동기화** — `design-system.md`/`screen-spec.md` 에서 issue #34 가
   기록한 ↗ 형태와 행-상세 트리거 서술을 이번 변경에 맞게 갱신.

Seven 수용 기준 checkboxes:

- 이슈/PR 번호가 `#<n>` 파란 링크로 보이고 GitHub 으로 이동한다
- Flows 표에서 줄바꿈 없이 한 줄에 표시된다
- 상세 패널을 키보드만으로 열고 닫을 수 있다 (행 클릭 방식으로 회귀 없음)
- owner/name 없는 레코드가 깨진 링크를 만들지 않는다
- 기존 테스트 전부 통과
- 스펙 문서가 실제 구현과 일치
- 주의: PR 본문에 closing 키워드 금지

The issue also carries a **prohibition**, not a checkbox: "행 전체 클릭으로
되돌리는 것은 금지". Phase 2 treats it as a negative sub-fact of AC3.

## 3. Evidence-location map

Everything below is a *locator*, not a judgment.

**Number-as-link (요구사항 1/2/5, AC1, AC4)**
- `src/rsb/web/dashboard.js:218-221` `buildGithubUrl(ownerName, kind, number)`
  — returns `null` when `ownerName` is falsy or non-string.
- `src/rsb/web/dashboard.js:223-227` `numberLinkHtml(...)` — emits
  `<a class="number-link" href=… target="_blank" rel="noopener noreferrer">#<n></a>`,
  or `escapeHtml("#" + number)` with no anchor when the URL is `null`.
- Two direct call sites: `:243` (`issueToggleCell`, kind `"issues"`) and
  `:254` (`prCellHtml`, kind `"pull"`).
- Six rendered columns: `:266` Decision-queue Issue, `:267`
  Decision-queue PR, `:300` Flows Issue, `:304` Flows PRs, `:316`
  Sessions Issue, `:333` Accounting Issue.
- Owner/name source: `:589` `const ownerNameByRepo = data.owner_name_by_repo || {}`,
  produced by `src/rsb/render.py:174` from `src/rsb/model.py:110,294`.
- Colour: `src/rsb/web/dashboard.css:248-251` `.number-link { color: var(--color-action-primary-background); text-decoration: none; }`;
  `:252-255` underline on hover **and** focus; `:256-259` focus-visible
  outline `2px solid var(--color-blue-500)`.
- Token definitions: `dashboard.css:9` `--color-blue-500: #2563eb`;
  `:23` `--color-action-primary-background: var(--color-blue-500)`;
  `:21` `--color-text-primary: var(--color-neutral-900)` = `:8` `#111827`;
  `:3` `--color-neutral-0: #ffffff`.
- Token doc: `docs/specs/design-system.md:61`
  `| color-action-primary-background | blue-500 | refresh button, links |`.

**↗ removal (요구사항 3)**
- Zero `.external-link` rules in `dashboard.css`; zero `external-link`
  strings in `dashboard.js`; zero occurrences in `index.html`.
- The glyph survives only in two source comments —
  `dashboard.css:244` and `dashboard.js:210` — and in historical
  `docs/issue-34/**` and `docs/issue-36/reports/implementation/scout-brief.md`.

**Disclosure trigger (요구사항 4, AC3)**
- `src/rsb/web/dashboard.js:237-239` `rowToggleButtonHtml(...)` —
  `<button type="button" class="row-toggle" aria-expanded aria-controls="detail-panel-slot" aria-label="Toggle details for issue {n}" data-issue data-repo data-table><span aria-hidden="true">▸|▾</span></button>`.
- Emitted **leading** the link inside `<span class="issue-cell">`
  (`:243`).
- Handler: `:549-573` `attachRowToggleHandlers` — binds `click` to each
  `.row-toggle` (not to `<tr>`), toggles-to-close at `:555-556`, focus
  moves to `#detail-panel-heading` on open (`:568-569`) and back to the
  originating button on close (`:562-566`).
- `<tr>` carries no `data-*` and no listener — `:178-182` (comment +
  `<tr>${r.cells.join("")}</tr>`), `:465` detail row.
- `aria-controls` target exists: `src/rsb/web/index.html:25`
  `<div id="detail-panel-slot"></div>`.
- Layout branch: `:485-526` `applySelectionLayout` — fills
  `DETAIL_SLOT.innerHTML` only when the row can't be uniquely located or
  `matchMedia("(min-width: 1200px)")` matches; otherwise empties the slot
  (`:522-525`) and inserts a sibling `<tr class="detail-row">`.
- CSS: `dashboard.css:212-228` `.row-toggle` (chrome stripped,
  `min-width/min-height: 24px`, inline-flex), `:229-232` focus-visible.

**Flows single-line (AC2)**
- `dashboard.css:237-242` `.issue-cell { display:inline-flex; gap:var(--space-1); white-space:nowrap; }` — the **only** nowrap on a data cell.
- `.issue-cell` wraps the Issue cell only (`dashboard.js:243`). The Flows
  **PRs** cell emits `<span class="mono">…</span>` per PR joined by
  `", "` (`dashboard.js:253-255`); `.mono` (`dashboard.css:84`) sets
  `font-family` only.
- No per-column width rules exist; table-level only —
  `dashboard.css:178,181` (`width:100%; min-width:640px`), `:205`
  `.table-scroll { overflow-x:auto }`.

**Tests (AC5)**
- `test/rsb_tests/test_model.py:313-325` and `:328-336` — the two new
  `numberLinkHtml` tests (both `kind="issues"`; neither covers `"pull"`).
- `test/rsb_tests/test_dashboard_dom.py:177-245` — four `.row-toggle`
  DOM tests (added later, by issue #44 / `b2f6b63`).
- Harnesses: `test_model.py:170-179` `_run_dashboard_js` (node, no DOM,
  skips if `node` absent); `test_dashboard_dom.py:51-95` `_run_dom_js`
  (node + jsdom, skips if `node` **or** `test/node_modules/jsdom` absent).
- Documented invocation: `docs/handbooks/rsb.md:37-63` — `python -m pytest test/`,
  plus the one-time `npm install --prefix test`.
- `.github/workflows/deploy-board.yml` runs **no** tests and has no
  `pull_request`/`push` trigger; there is no CI test signal to cite.

**Doc sync (요구사항 6, AC6)**
- `docs/specs/screen-spec.md:60-69` (§1.3 canonical passage), `:78-81`,
  `:89-92` (§1.4 Flows), `:97` (§1.5), `:115-124` (§1.6), `:128` (§1.7),
  `:222-227` (§2.6).
- `docs/specs/design-system.md:179` (`DataTable` component row), `:163-165`,
  `:183`.
- The `b621082` spec diff itself: `design-system.md` +1 line rewritten,
  `screen-spec.md` §1.3 and §1.4 rewritten.

**PR body (AC7)**
- PR #37 body, obtainable with `gh pr view 37 --json body`.

## 4. Observations shaping requirement decomposition (not verdicts)

- **O1 — the issue names its own scope, and five number renderings sit
  outside it.** 요구사항 1 enumerates exactly six columns. Numbers are
  still rendered as bare text at `dashboard.js:348` and `:349` (Hygiene
  list items), `:419` (detail-panel pending-PR badge), `:449`
  (detail-panel `<h2>`) and `:450` (detail-panel decision line).
  `renderHygiene` is not even passed `ownerNameByRepo` (`:346`, called at
  `:635`). None of these five is in the issue's enumerated target list,
  so they are a **scope note**, not a candidate defect — but phase 2 must
  say so explicitly rather than silently ignore them.
- **O2 — AC2 is ambiguous across two Flows columns.** `white-space:
  nowrap` protects the Issue cell only; the Flows **PRs** column has no
  nowrap wrapper. The issue's 배경 §2 names the Flows *Issue* column as
  the observed defect ("Flows 표의 Issue 열이 좁아"), so the AC's core is
  the Issue cell — but the AC text says "Flows 표에서", not "Issue 열에서".
  Phase 2 splits AC2 into the Issue cell (core) and the PRs column
  (secondary reading), and states which reading each verdict answers.
- **O3 — the DOM tests currently do not execute.** `test/node_modules`
  does not exist in this checkout, so `test_dashboard_dom.py:64-65` skips
  all 8 of its tests, including the four that cover the relocated
  disclosure trigger. A run reporting "57 passed, 8 skipped" therefore
  carries **zero execution evidence for the behaviour AC3 is about**.
  Phase 2 must run `npm install --prefix test` first and report the
  counts before and after; if the install cannot complete, the affected
  sub-facts are Unverifiable, not passing (see the scout brief's
  must-be).
- **O4 — `aria-controls` is fixed to `detail-panel-slot` in both layout
  branches.** Below the 1200px breakpoint the panel is rendered as a
  sibling `<tr class="detail-row">` while the slot is emptied
  (`dashboard.js:522-525`), so the IDREF resolves to an existing but
  empty element that is not the container being shown. 요구사항 4 says the
  existing `aria-controls` semantics must be *maintained*; whether
  "maintained" is satisfied by an IDREF that resolves to the wrong
  element in one branch is a genuine sub-fact, decomposed under R3.
- **O5 — there is no `keydown`/`keypress` handler anywhere in
  `dashboard.js`.** Keyboard operation rests entirely on native
  `<button>` semantics (Enter/Space). That is the correct mechanism, but
  it means AC3's keyboard claim is evidenced by *element type + focus
  order*, not by an intercepted key event — phase 2 must verify the
  element is a real focusable `<button type="button">` and that both
  controls in the cell are separate tab stops in DOM order.
- **O6 — 요구사항 6's first clause has a false premise, and the spec edit
  is self-ratifying.** Neither `design-system.md` nor `screen-spec.md`
  contained `↗` or `external-link` at `b621082^` (verified by dumping
  both files at that commit: 0 occurrences each). Issue #34 never
  recorded the ↗ form in the specs, so there was nothing to update on
  that half of the clause. Separately, the spec text and the code it
  describes landed in the *same* commit, so phase 2 must check
  bidirectionally — spec→code **and** code→spec — rather than confirming
  the spec against itself.
- **O7 — `escapeHtml` covers five characters only.** `dashboard.js:25-29`
  escapes `& < > " '`. The `href` at `:226` is attribute-escaped but has
  no URL-scheme allow-list, so a hostile `owner_name` value could still
  produce a `javascript:` href. `owner_name` originates upstream
  (`model.py`, from the `repo` field of `flows --json`), and issue #36
  neither introduced the URL nor asked for URL hardening — this is
  recorded as an out-of-scope observation for a follow-up issue, not a
  #36 requirement.
- **O8 — later commits amended the same spec line.** `design-system.md:179`
  now also carries issue #38's "24×24px minimum size per issue #38 P2-5"
  clause, which `b621082` did not write. Attribute before judging.
- **O9 — the Decision-queue PR column always passes a 1-element array**
  (`dashboard.js:267` `prCellHtml(ownerNameByRepo[d.repo], [d.pr])`), so
  the `length === 0` "-" fallback at `:252` is unreachable there and a
  null `d.pr` would render `#null`. Adjacent to AC4 but not the same
  claim (AC4 is about missing owner/name); phase 2 keeps them separate.

## 5. Constraints on phase 2's verification depth

- **No browser, no layout engine.** jsdom implements the DOM but not CSS
  layout, so no local means exists to *observe* whether the Flows Issue
  cell wraps. CSS-rule inspection establishes a contributing cause, not
  the rendered outcome (see the scout brief). AC2 is therefore expected
  to resolve as partially-evidenced or Unverifiable, and the proposal
  says so up front rather than substituting rule-reading for observation.
- **Colour rendering cannot be observed either**, but the contrast
  question is arithmetic on declared token values and *is* computable
  from `dashboard.css:3,8,9,23` — that part is verifiable.
- **`npm install --prefix test` requires network access** to
  `registry.npmjs.org`. If it fails, the four disclosure DOM tests stay
  skipped and the dependent sub-facts become Unverifiable.
- **The live site** (`https://tokenmaxxxer.github.io/repo-status-board/`)
  is deployed by a `*/30 * * * *` cron and is a legitimate secondary
  evidence source for AC1/AC4 (does the shipped page contain
  `class="number-link"` anchors, and does `api/board.json` carry
  `owner_name_by_repo`), subject to network availability.
- **No CI test run exists to cite** — `deploy-board.yml` runs no tests.
- **This role does not fix anything it finds** (contract; role
  directive). Every non-Present verdict hands off to the owning role via
  a finding addressed to it.

## 6. Write-set for this role

Phase 1 (this PR) writes exactly three files:

- `docs/issue-36/reports/conformance-review/survey.md` (this file)
- `docs/issue-36/reports/conformance-review/scout-brief.md`
- `docs/issue-36/proposals/conformance-review.md`

Phase 2, only after an approval per contract v3 §19, writes exactly one
more: `docs/issue-36/reports/conformance-review.md`. No file under
`src/`, `test/`, `docs/specs/`, or another role's report area is written
by this role in either phase.
