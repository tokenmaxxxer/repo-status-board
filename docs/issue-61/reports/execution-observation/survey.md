# issue-61 execution-observation — current-state survey (phase 1)

Scope of this observation, stated exactly: the **implementation** role's
session on issue **#61**, branch `issue-61/implementation`, delivered as
**PR #66** (phase 1 + phase 2, merged `3f06ba6`) and **PR #69**
(later-entry, merged `d8082dc`). Nothing else is under observation — not
issue #62's parallel work, not the upstream #36/#38 reviews whose
findings #61 inherits, not the repository's current `src/` state.

This document records what was read and what the artifacts show. It
renders no verdict; the three verdict levels are named in
`docs/issue-61/proposals/execution-observation.md` and answered only in
phase 2.

## 1. What was read this session (first-hand, no secondhand summaries)

1. Issue **#61** in full (`gh issue view 61`) — title, body (배경 F1/F2,
   요구사항 1–3, 제약, Acceptance 3 bullets, 실행 계획 2 steps), created
   `2026-08-08T02:53:21Z`.
2. Issue #61's **two comments**, verbatim bodies via `gh issue view 61
   --json comments`:
   - `5224224718` (`jjongkwann`, `03:08:49Z`) — `[on-the-record]
     stranded-relay: issue-61/implementation:pr-create-failed`, detail
     `GraphQL: No commits between main and issue-61/implementation`.
   - `5224266614` (`jjongkwann`, `03:20:33Z`) — body `APPROVE
     issue-61/implementation`.
3. **PR #66** full metadata (`gh pr view 66 --json ...`): author
   `jjongkwann`, base `main`, head `issue-61/implementation`, created
   `03:18:53Z`, merged `03:40:32Z` as `3f06ba6`, `reviews: []`,
   `comments: []`, body (phase-1 Summary + appended "Phase 2 delivered"
   paragraph).
4. **PR #69** full metadata: same author/head/base, created `03:44:42Z`,
   merged `03:46:29Z` as `d8082dc`, `reviews: []`, `comments: []`.
5. The **four commit messages with `--stat`**, and the full diffs of the
   non-record files:
   - `3096092` (`03:18:32Z`) — phase 1, 3 files, +579, docs only.
   - `f93c819` (`03:23:20Z`) — phase-2 record opened, 1 file, +63.
   - `346a6c0` (`03:38:15Z`) — phase 2, 4 files (+227/−39); full diff read
     for `src/rsb/web/dashboard.js`, `docs/specs/screen-spec.md`,
     `test/rsb_tests/test_dashboard_dom.py`.
   - `a762ef0` (`03:43:06Z`) — later entry, 2 files; full diff read for
     `test/rsb_tests/test_model.py`.
6. The observed role's **own record**,
   `docs/issue-61/reports/implementation.md` (236 lines) — all sections.
7. The observed role's **approved proposal**,
   `docs/issue-61/proposals/implementation.md` (151 lines) — all sections.
8. The observed role's **phase-1 survey** structure and its "Warrant hunt
   (phase 1)" section headings (`survey.md:1,10,42,56,72,98,129,147,200,
   230,263,301,320,332,347,354`) and its **scout brief** in full
   (`scout-brief.md`, 4 source URLs at `:68-73`).
9. `docs/specs/approvers.md` — two entries: `JiwonJung94`, `jjongkwann`.
10. Precedent for this role's own artifacts:
    `docs/issue-56/proposals/execution-observation.md` (237 lines) and
    `docs/issue-56/reports/execution-observation/scout-brief.md`.
11. Repository shape facts: `ls docs/specs/` (no contract document is
    checked in — the role-handoff contract exists only in the session
    rulebook), `ls .github/workflows/` → `deploy-board.yml` only,
    `git config core.hooksPath` → unset and no `.githooks/`,
    `grep -rn "Later entry" docs/` → hits only in
    `docs/issue-61/reports/implementation.md:165,167`.

Not read as evidence, deliberately: any file under `src/` or `test/` at
working-tree HEAD. Where markup or test text is needed it is taken from
the diff of `346a6c0` / `a762ef0`, which is what the observed role
actually produced.

## 2. Timeline (timestamps only, no causal claims)

| time (UTC) | event | source |
| --- | --- | --- |
| 02:53:21 | issue #61 opened | `gh issue view 61 --json createdAt` |
| 03:08:49 | stranded-relay comment: `pr-create-failed`, "No commits between main and issue-61/implementation" | comment `5224224718` |
| 03:18:32 | `3096092` phase-1 commit (survey + scout brief + proposal, docs only) | `git show --stat 3096092` |
| 03:18:53 | PR #66 opened | `gh pr view 66 --json createdAt` |
| 03:20:33 | `APPROVE issue-61/implementation` comment | comment `5224266614` |
| 03:23:20 | `f93c819` opens the phase-2 record | `git show --stat f93c819` |
| 03:38:15 | `346a6c0` phase-2 delivery | `git show --stat 346a6c0` |
| 03:40:32 | PR #66 merged as `3f06ba6` | `gh pr view 66 --json mergedAt,mergeCommit` |
| 03:43:06 | `a762ef0` later-entry commit | `git show --stat a762ef0` |
| 03:44:42 | PR #69 opened | `gh pr view 69 --json createdAt` |
| 03:46:29 | PR #69 merged as `d8082dc` | `gh pr view 69 --json mergedAt,mergeCommit` |

## 3. What the delivery contains, as the diffs show it

`346a6c0` — `src/rsb/web/dashboard.js`, three hunks:

- `rowToggleButtonHtml`'s leading comment rewritten from "Fixed
  `aria-controls=\"detail-panel-slot\"`" to "Default ... ;
  applySelectionLayout() overwrites it to `\"detail-row\"` ... (issue-61
  F2)". The emitted markup line itself is unchanged.
- `detailRowHtml`: `<tr class="detail-row">` → `<tr class="detail-row"
  id="detail-row">`.
- `applySelectionLayout`: the unguarded
  `window.matchMedia(WIDE_LAYOUT_QUERY).matches` in the `if` condition
  replaced by two statements — `const mql = typeof window.matchMedia ===
  "function" ? window.matchMedia(WIDE_LAYOUT_QUERY) : null;` and `const
  isWideLayout = mql && typeof mql.matches === "boolean" ? mql.matches :
  true;` — with the branch now `if (!selectedRow || isWideLayout)`; and,
  in the `else` (narrow) branch, after the `insertAdjacentHTML`, `const
  selectedButton = selectedRow.querySelector(".row-toggle"); if
  (selectedButton) selectedButton.setAttribute("aria-controls",
  "detail-row");`.

`346a6c0` — `docs/specs/screen-spec.md`: §1.3's `aria-controls` sentence
gains "by default (wide layout, or narrow with no selection), updated to
`\"detail-row\"` when the narrow (<1200px) layout has that row's panel
expanded as a sibling `<tr>` (§1.6)"; §1.6 gains a symmetric bullet
naming `id="detail-row"` and cross-referencing §1.3.

`346a6c0` — `test/rsb_tests/test_dashboard_dom.py`: one new case,
`test_row_toggle_narrow_layout_aria_controls_resolves_to_detail_row`,
which reassigns `window.matchMedia = () => ({ matches: false })` inside
the jsdom script, clicks the decisions-table toggle for issue 7, and
asserts four values: `detailSlotEmpty`, `detailRowExists`,
`ariaControls == "detail-row"`, and `resolvedId == "detail-row"` where
`resolved = document.getElementById(ariaControls)`.

`a762ef0` — `test/rsb_tests/test_model.py:347`: the expected exact string
in `test_dashboard_js_detail_row_html_wraps_content_in_a_tr_with_colspan`
gains ` id="detail-row"`. One line, plus 23 lines appended to the record.

## 4. Check surfaces this observation has to resolve (enumerated, unanswered here)

Each row is a surface, the artifact it is answered from, and why it is
open. No row is answered in this document.

| # | surface | answered from |
| --- | --- | --- |
| 1 | Issue AC 1 — `test_dashboard_dom.py` 전건 통과, 0 skipped | the record's Red-green section (`reports/implementation.md:87-109`) read as a claim; the new-case diff in `346a6c0` |
| 2 | Issue AC 2 — narrow-branch aria-controls IDREF 해소 단언 | the four assertions in `346a6c0`'s `test_dashboard_dom.py` hunk, against the AC's wording |
| 3 | Issue AC 3 — screen-spec §1.3 양 분기 서술 | `346a6c0`'s `screen-spec.md` hunk against §1.3/§1.6 |
| 4 | 요구사항 1 — 수정 위치를 트레이드오프와 함께 결정 | `proposals/implementation.md:37-54` (inline-guard adopted, harness stub rejected, `true` fallback) against `346a6c0`'s actual guard |
| 5 | 요구사항 3 (§20 class question) — 전수 열거 + 범위 판단 | `proposals/implementation.md:56-75` and `reports/implementation.md:50-56`; whether "enumerate + decide" was answered as the requirement words it |
| 6 | Whether the delivered guard matches the *approved* guard byte-for-behaviour | `proposals/implementation.md:79-92` against the `applySelectionLayout` hunk in `346a6c0` |
| 7 | Whether the narrow-branch `aria-controls` override can go stale | the `applySelectionLayout` hunk alone (does anything re-run it on a layout change, per the diff), plus whether the record or spec discloses the bound |
| 8 | The static singleton `id="detail-row"` — justification vs. what the diff guarantees | `proposals/implementation.md:93-98`, `reports/implementation.md:25-27`, and the `detailRowHtml`/`applySelectionLayout` hunks |
| 9 | The scope-exceeded stop: main merged at `3f06ba6` (03:40:32Z) with the record itself stating 66 passed / 1 failed (`reports/implementation.md:111-128`) | the record's own text, PR #66's body, and the timeline in §2 |
| 10 | The later-entry route: the record's own Open findings prescribed "a follow-up proposal with write set `test/rsb_tests/test_model.py`" (`:160-163`), and the delivery instead used a "Later entry — ... (contract s19)" section (`:167-184`) under the existing approval, with `gh pr view 69 --json reviews` → `[]` and no second APPROVE comment on the issue | the record, the issue's two comments, PR #69's metadata |
| 11 | Phase ordering: whether `3096092` staged phase-1 homes only, whether the phase-1 survey's *spike* (heading `survey.md:72-73`, disposition `:75-77`, measurement 9/9 and 66/66 at `:89-90`) left anything in the commit | `git show --stat 3096092` (3 docs files) and the survey's own text |
| 12 | Approval path validity under single-account mode | comment `5224266614` body (exact string), its author against `docs/specs/approvers.md`, PR #66 `reviews: []`, and the record's own claim at `:9-11` |
| 13 | The stranded-relay episode (03:08:49Z, "No commits between main and issue-61/implementation") against the first commit at 03:18:32Z | comment `5224224718`, `git log` authored dates |
| 14 | Commit hygiene the contract makes mechanical: `Subject: issue-61` trailer on all four commits, one commit per subject, no closing keyword in PR titles/bodies | the four commit messages, PR #66/#69 titles and bodies |
| 15 | The observed role's phase-1 scout obligations: mode (parallel vs batched-sequential) and stage count stated, sources present | `reports/implementation/scout-brief.md:1-8` and its `Sources` at `:68-73`, against the precedent shape in `docs/issue-56/reports/execution-observation/scout-brief.md:3-11` |
| 16 | Warrant-hunt record completeness across both transitions | `survey.md:320-360` (phase 1, stance 0) and `reports/implementation.md:186-206` (before-landing, stance 1), plus the record's Closed checks `:208-221` |
| 17 | Proposal frontmatter shape — `proposals/implementation.md:1-4` opens with a bare `files:` list, no `---` fence and no `status:` field | the file itself, against the precedent proposals under `docs/issue-*/proposals/` |
| 18 | Whether every claim in the record that no surviving artifact backs is marked as such (e.g. the pytest counts, the `node --check` runs) | the record's own wording; `.github/workflows/` holds only `deploy-board.yml`, so no CI run attests these |

## 5. Gaps the scout sweep is aimed at

The surfaces above split into ones the artifacts answer directly (1–6,
11–16) and ones that need an external yardstick before they can be
adjudicated at all. Those are the scout targets:

- **G1 — approval scope after a scope-exceeded stop.** Rows 9, 10. What
  do strong review regimes say about work that lands under an earlier
  approval versus work that requires a fresh one, when the original scope
  proved one file short?
- **G2 — merging with a knowingly failing test.** Row 9. What is the
  field's rule for integrating a change that the author knows leaves the
  mainline suite red, and what disclosure makes it acceptable, if any?
- **G3 — `aria-controls` IDREF integrity across a layout switch.** Rows
  7, 8. What does a strong accessibility audit check about
  `aria-controls`, duplicated/static ids, and attributes that are only
  correct at render time?
- **G4 — exact-string DOM assertions as a coupling class.** Row 18 and
  the `a762ef0` fix. Does the field treat "update the literal" as closing
  the class, or as the recurrence surface itself?

## 6. Known limits of this survey

- The role-handoff contract is not a repository artifact (`ls
  docs/specs/`), so "contract s19" as cited in
  `reports/implementation.md:167` cannot be checked against a checked-in
  text; it can only be checked against this repository's own precedent
  (`grep -rn "Later entry" docs/` returns that record alone) and against
  what the session rulebook states.
- `.github/workflows/` holds `deploy-board.yml` only, so no independent
  CI attestation of any test count exists to corroborate or contradict
  the record's numbers.
- PR #66 and PR #69 both carry `reviews: []` and `comments: []`, so the
  only human act on the record for either is issue comment `5224266614`.

## 7. Warrant hunt (this role's own phase 1)

`proposal: docs/issue-61/proposals/execution-observation.md` —
**after-proposal dispatch: RUN**, synchronously and consumed inside this
turn (contract v3 s22 forbids ending a headless turn with an unconsumed
dispatch; it permits waiting, which is what happened here). Stance **0**
(assume the gate just touched is bypassable — find the bypass), taken as
dispatch count 0: no `.warrant-hunt.count` exists in this repository.
Tier `size:docs-only` (phase-1 write set = 3 files, all under
`docs/issue-61/`), cap 60s; actual 88s, over cap — recorded rather than
trimmed after the fact. The hunter was instructed to write no file,
because this repository has no `docs/reports/` bucket and this role may
write only its own two homes; its finding is transcribed here instead.

**Verdict: FINDING.** Kind: design-error, in this role's own proposal —
not in the observed artifact. The proposal's check **T2** cited
`reports/implementation/survey.md:72` for the phase-1 spike's "9/9 and
66/66" measurement; `:72-73` is only that section's heading, the
disposition sentence ("`git checkout --`로 되돌림 … 커밋 트리에는
반영되지 않음") is at `:75-77`, and the measurement itself is at `:89-90`.
Reproduced by `sed -n '70,95p'
docs/issue-61/reports/implementation/survey.md`. Under this proposal's
own admissibility rule 3 a phase-2 sentence citing `:72` would carry a
locator that does not contain the fact it asserts — the exact bypass the
stance predicted, in the gate's own check table.

**Action taken this phase**: T2's citation corrected to `:72-73` /
`:75-77` / `:89-90` in `docs/issue-61/proposals/execution-observation.md`,
and check-surface row 11 above corrected to match. Closed.

**Before-landing dispatch**: skipped under the docs-only fast path —
every path in this phase's write set is under `docs/issue-61/`.
