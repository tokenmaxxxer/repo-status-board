# Execution-observation record (issue #36, phase 2)

Subject observed: the **implementation** role's phase-1→phase-2 execution
on issue #36, as landed in **PR #37** (`issue-36/implementation` → `main`,
MERGED `2026-08-03T11:30:30Z`, merge commit
`b6210821c55fbc108773f71f7adf12a427b1a097`,
`https://github.com/tokenmaxxxer/repo-status-board/pull/37`), its two
commits `403dbd0c4bf1b54f176e9f7e79e16e1c76401da7` (phase 1) and
`2c462e0b660d6f325b4a7e5b920d774837f03d95` (phase 2), and its own record
`docs/issue-36/reports/implementation.md`. Scope, method, and evidence
sources were fixed in advance by this role's own phase-1 proposal,
`docs/issue-36/proposals/execution-observation.md`, committed at
`21cba3a` and carried on PR #49.

code_under_review: PR #37 (`issue-36/implementation` → `main`, merged @
`b621082`) — `src/rsb/web/dashboard.js`, `src/rsb/web/dashboard.css`,
`test/rsb_tests/test_model.py`, `docs/specs/screen-spec.md`,
`docs/specs/design-system.md`, `docs/issue-36/reports/implementation.md`.
loop_state: reported

## Why

Phase 2 for this role was opened by issue #36's comment whose entire body
is `APPROVE issue-36/execution-observation` (jjongkwann,
`2026-08-04T07:24:27Z`,
`https://github.com/tokenmaxxxer/repo-status-board/issues/36#issuecomment-5175870378`),
read byte-for-byte this session via
`gh api repos/:owner/:repo/issues/36/comments`. This record executes
`docs/issue-36/proposals/execution-observation.md` §0–§3: a three-level
verdict (outcome / trajectory / step), an AC-by-AC table carrying an
explicit demonstrated / asserted-only label per
`docs/issue-36/reports/execution-observation/scout-brief.md:39-41`, the
three-item disclosure checklist from the same brief as the literal check
list for AC3, and any deficiency written in the four-part blameless
shape. Additionally, per this session's invocation, it judges whether
issue #34's execution-observation finding **F1** (the ↗-icon wrap that
gave rise to issue #36) is discharged.

## What was done

Read PR #37 in full — its body, both PR-level comments, both commit
messages, and the complete diff of all five non-record files its phase-2
commit `2c462e0` touched — plus its own phase-2 record
`docs/issue-36/reports/implementation.md`, its approved proposal at
`403dbd0`, issue #36's body and both issue comments, issue #34's
execution-observation record (for F1), and the third-party artifact
`test/rsb_tests/test_dashboard_dom.py` added on `main` by `b2f6b63`.
Against that evidence, rendered the three-level verdict this role's
contract requires, per the method this role committed to in its own
approved phase-1 proposal: issue #36's seven acceptance criteria each
mapped to a specific hunk or named third-party artifact and labeled
demonstrated / asserted-only; the phase-1→phase-2 trajectory checked
against the phase-1 commit's file set, the proposal-vs-diff match, the
four single-account approval facts, and the six timestamps; and each of
the five step-level candidates enumerated in advance either cleared with
a citation or written up as a finding in the four-part blameless shape.
Also judged issue #34 F1's two halves separately, as that finding's own
action item separated them. No code, test, spec, or other role's record
was written or changed by this role, and no `pytest`, `node`, jsdom,
browser, or `rsb serve` command was executed this session — per the
re-execution prohibition.

## What was read this session

Nothing below is secondhand; every item was read in this session.

- `gh issue view 36` (body: 6 requirements, 7 ACs, 2-step plan; state
  OPEN) and `gh api repos/:owner/:repo/issues/36/comments` (both comment
  bodies, verbatim).
- `gh pr view 37 --json number,title,state,author,url,mergedAt,
  mergeCommit,body,commits,reviews` — full body, both commit SHAs and
  messages, `reviews: []`.
- `gh pr view 37 --json comments` — both PR-level comments, verbatim.
- `git show 2c462e0 -- src/rsb/web/dashboard.js` and
  `git show 2c462e0 -- src/rsb/web/dashboard.css docs/specs/design-system.md
  docs/specs/screen-spec.md test/rsb_tests/test_model.py` — the complete
  phase-2 diff of all five non-record files, plus
  `git show 2c462e0 --stat`.
- `git show 2c462e0:docs/specs/screen-spec.md` (§1.6) and
  `git show 2c462e0:docs/specs/design-system.md` (token table line 61).
- `git show origin/main:docs/issue-36/reports/implementation.md` — the
  observed role's own phase-2 record, in full (280 lines).
- `git show 403dbd0:docs/issue-36/proposals/implementation.md` — the
  approved proposal's scope declarations.
- `git show origin/main:docs/issue-34/reports/execution-observation.md` —
  the prior pass's F1 finding, in full.
- `git log -1 b2f6b63` + `git show --stat b2f6b63` +
  `git show b2f6b63:test/rsb_tests/test_dashboard_dom.py` — the
  third-party artifact already on `main`.
- `cat docs/specs/approvers.md`; `gh pr view 49`.
- This role's own phase-1 artifacts at `21cba3a`:
  `docs/issue-36/reports/execution-observation/survey.md`,
  `.../scout-brief.md`, `docs/issue-36/proposals/execution-observation.md`.

Deliberately **not** read as evidence: the working tree's `src/**`.
`main` now also carries `b2f6b63` and later commits, so current file
state is not PR #37's diff.

## Independence statement

This role did not author, edit, or execute any part of the observed
artifact — PR #37, its commits `403dbd0` / `2c462e0`, the merge commit
`b621082`, or `docs/issue-36/reports/implementation.md` — in this session
or any prior one. Nothing under `src/`, `test/`, `docs/specs/`,
`docs/issue-36/proposals/implementation.md`,
`docs/issue-36/reports/implementation.md` or
`docs/issue-36/reports/implementation/` is touched by this branch; this
record and this role's own phase-1 files are the only things it writes.
Every claim below is drawn from PR #37's actual diff, commits, and
comments, and from the observed role's own record — never from re-running
the observed code, and never from treating the present state of `src/**`
as evidence of what the implementation role did or decided. **No verdict
language appears anywhere above this statement.**

## How phase 2 was opened for this role

`gh pr view 49` returns `headRefName: issue-36/execution-observation`
(correct branch, one branch per issue × role) and state OPEN;
`gh pr view 37 --json reviews` returns `[]`, and no PR review Approve
exists on PR #49 either — so the two-account review path does not apply.
`docs/specs/approvers.md` lists exactly two accounts, `JiwonJung94` and
`jjongkwann`; PR #49's author is `jjongkwann`, the same account —
single-account mode. Contract v3 §19's single-account clause requires an
issue-level comment whose entire body is exactly
`APPROVE issue-36/execution-observation`, posted by an approvers.md
account. `gh api repos/:owner/:repo/issues/36/comments` returns exactly
two comments on issue #36, and their bodies are, byte-for-byte,
`APPROVE issue-36/implementation` (`issuecomment-5165555487`,
`2026-08-03T11:08:44Z`) and `APPROVE issue-36/execution-observation`
(`issuecomment-5175870378`, `2026-08-04T07:24:27Z`) — both by
`jjongkwann`, neither carrying surrounding prose. The second is a
string-exact match for this role's gate string; the first is an exact
match for a *different* role's gate string and is not read as approving
this role. No near-miss or affirmative-sounding non-matching comment
exists on issue #36 to disclose. Phase 2 for this role is authorized, and
this record is the first artifact written in it.

## Three-level verdict

### 1. Outcome — did PR #37 land what issue #36 asked?

Issue #36's body (`gh issue view 36`, read this session) lists seven
acceptance-criteria checkboxes. "Demonstrated" below requires a primary
artifact other than the observed role's own record
(`docs/issue-36/reports/execution-observation/scout-brief.md:14-17`).

| # | Criterion (issue #36 body) | Evidence | Label |
|---|---|---|---|
| AC1 | 이슈/PR 번호가 `#<n>` 파란 링크로 보이고 GitHub 으로 이동한다 | `git show 2c462e0 -- src/rsb/web/dashboard.js`: `externalLinkHtml` → `numberLinkHtml(ownerName, kind, number)` returning `<a class="number-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml('#'+number)}</a>`; `prCellHtml` routes each PR number through the same helper; `issueToggleCell` emits it after the toggle button. `git show 2c462e0 -- src/rsb/web/dashboard.css`: new `.number-link { color: var(--color-action-primary-background); }`. `git show 2c462e0:docs/specs/design-system.md:61` documents that token as `blue-500`, use "refresh button, links" — so requirement 2's "no new token" holds: the CSS hunk introduces only `var(--color-action-primary-background)` and `var(--color-blue-500)`, both pre-existing. `git show 2c462e0 -- test/rsb_tests/test_model.py` asserts the exact rendered string for the owner/name-present case. | **Demonstrated** (markup + token mapping + test, all in `2c462e0`); the rendered *color* itself is structural, not pixel-verified |
| AC2 | Flows 표에서 줄바꿈 없이 한 줄에 표시된다 | `git show 2c462e0 -- src/rsb/web/dashboard.css` adds `.issue-cell { display: inline-flex; align-items: center; gap: var(--space-1); white-space: nowrap; }`, and `git show 2c462e0 -- src/rsb/web/dashboard.js`'s `issueToggleCell` wraps button + link in `<span class="issue-cell">`; the ↗ anchor whose wrap the issue reported is deleted outright (the same CSS hunk removes `.external-link` and its `:hover`/`:focus`/`:focus-visible` rules). | **Asserted-only, structurally supported.** No artifact of any kind measures rendered layout: jsdom performs no layout (`docs/issue-36/reports/execution-observation/scout-brief.md:18-21`), so neither `docs/issue-36/reports/implementation.md`'s jsdom run nor `b2f6b63`'s `test_dashboard_dom.py` speaks to wrapping |
| AC3 | 상세 패널을 키보드만으로 열고 닫을 수 있다 (행 클릭 회귀 없음) | Checked against scout-brief's three-item disclosure checklist (`scout-brief.md:22-27`). (i) *Real `<button>`*: `2c462e0`'s new `rowToggleButtonHtml` emits `<button type="button" class="row-toggle" …>` with an `aria-hidden` `▸`/`▾` glyph and an `aria-label="Toggle details for issue ${issue}"` carrying the accessible name. (ii) *`aria-expanded` synchronized with actual visibility*: the same commit replaces `attachRowClickHandlers` (bound to `tbody tr[data-issue]`) with `attachRowToggleHandlers` bound to `.row-toggle`, reading the button's own `data-issue`/`data-repo`/`data-table` and setting `selectedIssue = isRowExpanded(...) ? null : { issue, repo, sourceTable }`; `renderTable`'s `<tr>` no longer emits `data-issue`/`data-repo` at all, so no whole-row target survives. (iii) *`aria-controls` points at a container that exists*: the literal `aria-controls="detail-panel-slot"` replaces `rowToggleId`'s never-rendered `detail-row-*` id, and `rowToggleId` is deleted. Independent confirmation: `git show b2f6b63:test/rsb_tests/test_dashboard_dom.py` adds `test_row_toggle_click_opens_detail_and_flips_aria_expanded` (asserts `before == "false"`, `afterExpanded == "true"`, detail slot non-empty), `test_row_toggle_click_on_non_button_cell_does_not_open_detail`, `test_row_toggle_click_only_affects_its_own_table`, and `test_row_toggle_reactivating_open_button_closes_it`; `git log -1 b2f6b63` states each corresponding test was verified to fail against `b621082^` — the tree immediately before PR #37 merged. | **Demonstrated for the pointer/state half** (`2c462e0` markup + `b2f6b63`'s independent, pre-fix-failing tests). **Not demonstrated for the literal keyboard half** — every artifact activates via `.click()`; see F3 |
| AC4 | owner/name 없는 레코드가 깨진 링크를 만들지 않는다 | `git show 2c462e0 -- src/rsb/web/dashboard.js`: `buildGithubUrl` returns `null` for falsy/non-string `ownerName`, and `numberLinkHtml` returns `escapeHtml('#'+number)` — plain text, no anchor — on that branch. `git show 2c462e0 -- test/rsb_tests/test_model.py`: `test_dashboard_js_number_link_html_falls_back_to_plain_text_without_owner_name` asserts the result is exactly `"#42"`. | **Demonstrated** (`2c462e0`, code + test in the same commit) |
| AC5 | 기존 테스트 전부 통과 | `docs/issue-36/reports/implementation.md` ("Tests") states `python3.11 -c "… pytest.main(['test/', '-q'])"` → **55 passed**, 0 failed (53 pre-existing + 2 new), plus `node --check src/rsb/web/dashboard.js` clean. Re-running is prohibited for this role (`docs/issue-36/proposals/execution-observation.md:100-105`). Partial third-party corroboration: `git log -1 b2f6b63` records "Full suite: 63/63 passing" on a later tree that contains `2c462e0`, consistent with the 55 having stayed green, though it measures a different commit. | **Asserted-only** (the observed role's own record), with the `b2f6b63` corroboration noted as indirect |
| AC6 | 스펙 문서가 실제 구현과 일치 | `git show 2c462e0 -- docs/specs/screen-spec.md`: §1.3 rewritten to the leading-button + trailing-`#<n>`-link shape with the exact `aria-controls="detail-panel-slot"` and `aria-label` strings the code emits; §1.4, §1.5 and §1.7 updated to "same §1.3 pattern". `git show 2c462e0 -- docs/specs/design-system.md`: §6's `DataTable` row names `.number-link` / icon-only `.row-toggle`. Both match the JS/CSS hunks in the same commit. **But** `git show 2c462e0:docs/specs/screen-spec.md` §1.6 still reads "expandable row below `breakpoint-lg`", while the same commit's `dashboard.js` comment hunk states "no `insertDetailRow()` exists; the narrow-layout behavior screen-spec.md §1.6 documents remains unimplemented … out of scope for this change". | **Met for the surfaces this change touched** (`2c462e0`, both spec files); **not met for §1.6**, by the commit's own written admission — see F2 |
| AC7 | PR 본문에 closing 키워드 금지 (백틱 인용 포함) | `gh pr view 37 --json body`, read in full this session: the only issue reference is `Phase 1 (research/survey/proposal) for #36.`; no `close`/`fix`/`resolve`-family keyword appears in any form, backticked or plain. `gh pr view 37 --json comments`: neither comment (`issuecomment-5165555695`, `issuecomment-5165741708`) contains one either. | **Demonstrated** (PR #37 body and both comment bodies, read verbatim) |

**Outcome verdict: PR #37 landed the substance of what issue #36 asked —
six of the seven ACs are met against the merged diff `2c462e0`, four of
them demonstrated by a primary artifact other than the observed role's
own record, and AC6 is met for every surface the change touched but not
for `screen-spec.md` §1.6, which `2c462e0`'s own `dashboard.js` comment
declares stale in the same commit that left it unedited.** The two
criteria that resist demonstration are bounded and named rather than
waved through: AC2's rendered single-line claim has no layout-bearing
artifact anywhere (`scout-brief.md:18-21` — jsdom performs no layout),
and AC5's 55-passed figure rests on
`docs/issue-36/reports/implementation.md` alone because re-running is
prohibited for this role
(`docs/issue-36/proposals/execution-observation.md:100-105`).

### 2. Trajectory — was the implementation role's phase-1→phase-2 path sound?

**Scouted when required.** `gh pr view 37 --json commits` shows `403dbd0`
(`2026-08-03T11:03:51Z`) as the phase-1 commit, and its message states the
survey found the `aria-expanded`/`aria-controls` wiring already broken
pre-issue-36; PR #37's body enumerates the three files it carries,
including `docs/issue-36/reports/implementation/scout-brief.md`, described
there as "4 parallel search angles, converged in 1 stage" citing Adrian
Roselli's expando-table pattern, Carbon's row-expansion convention, and
W3C ARIA APG's disclosure-pattern guidance. Scouting therefore ran and
produced its mandatory file before the proposal.

**Surveyed before proposing.** The same commit `403dbd0` carries
`docs/issue-36/reports/implementation/survey.md`, and
`git show 403dbd0:docs/issue-36/proposals/implementation.md:51-61` shows
the proposal's Rationale section arguing *from* that survey — it cites
"survey §2" for `selectedIssue.sourceTable` being permanently `undefined`
and for `aria-controls` pointing at a nonexistent id, and weighs
reproducing the bug versus fixing it in the same edit. The survey is the
proposal's stated input, not a document written alongside it for form.

**Real human approval, correctly gated, with nothing shipped before it.**
`docs/specs/approvers.md` lists `JiwonJung94` and `jjongkwann`; PR #37's
author is `jjongkwann` (`gh pr view 37 --json author`) and its `reviews`
array is `[]` — single-account mode. Issue #36's comment
`APPROVE issue-36/implementation` (`issuecomment-5165555487`,
`2026-08-03T11:08:44Z`) is a byte-exact match for that role's gate
string. Ordering, all timestamps from `gh pr view 37 --json commits` and
`gh api …/issues/36/comments`: phase-1 commit `403dbd0` `11:03:51Z` →
approval `11:08:44Z` → approval-attached feedback comment
`issuecomment-5165555695` `11:08:45Z` → phase-2 commit `2c462e0`
`11:28:51Z` → phase-2-complete comment `issuecomment-5165741708`
`11:29:18Z` → merge `11:30:30Z`. Strictly monotonic: no phase-2 code
commit precedes the approval.

**Shipped scope versus approved scope.**
`git show 403dbd0:docs/issue-36/proposals/implementation.md:70-103`
specifies `numberLinkHtml`'s `escapeHtml('#' + number)` fallback,
`rowToggleButtonHtml`'s literal attribute string including
`aria-controls="detail-panel-slot"`, the deletion of `rowToggleId`, and
the rebinding of the click listener off `tr[data-issue]` — and `2c462e0`'s
hunks match that spec function-for-function. The two pre-existing-bug
fixes (`sourceTable`, `aria-controls`) were declared in the proposal with
a rationale before approval (`403dbd0` proposal lines 51-61), so they are
approved scope, not scope creep. The two post-proposal fixes recorded
under "Adversarial hunt" in `docs/issue-36/reports/implementation.md` —
escaping the link-text branch, and removing dead `data-issue`/`data-repo`
from `<tr>` — both land in files the proposal already owned, are
one-to-few lines each, and follow directly from the approved rewrite (the
dead attributes exist *because* the approved change removed their only
reader). Judged relationally per
`docs/issue-36/reports/execution-observation/scout-brief.md:28-29`, that
is within-scope tidying of the same change, not an unrelated expansion.

**The approval-attached feedback comment.**
`issuecomment-5165555695`
(`https://github.com/tokenmaxxxer/repo-status-board/pull/37#issuecomment-5165555695`)
mandated that the disclosure rewiring be **operated in an actual browser**
and the result recorded, naming three minimum checks. What the record
delivers (`docs/issue-36/reports/implementation.md`, "PR #37 feedback
resolution") is a jsdom run against the shipped unmodified file, with the
browser attempt's failure documented concretely (Chrome
`crashpad`/`ProcessSingleton` permission errors, no
Playwright/Selenium/Puppeteer) and the substitution labeled in the record
itself as "a substitute for an actual GUI browser, not equivalent to
one". Item 1 (empty-cell click) and item 3 (`aria-expanded` flips
true→false with the panel filling and emptying) are covered by that run
and independently corroborated by `b2f6b63`'s `test_dashboard_dom.py`;
item 2's keyboard half is not, and the record says so in the same
paragraph rather than elsewhere ("jsdom does not itself translate a raw
`keydown` into a `click` … noted honestly rather than glossed over").

**Trajectory verdict: sound.** Scout and survey both preceded and fed the
proposal (`403dbd0`'s file set;
`git show 403dbd0:docs/issue-36/proposals/implementation.md:51-61` citing
survey §2); approval was real, string-exact, from a listed approver, and
correctly single-account-gated (`issuecomment-5165555487`); no code
shipped before it (`403dbd0` `11:03:51Z` and `2c462e0` `11:28:51Z` against
approval `11:08:44Z`); the shipped diff matches the approved spec
(`403dbd0` proposal lines 70-103 vs. `2c462e0`'s hunks); and the one
mandate that could not be met literally was substituted, disclosed at the
point of use, and its residual gap named
(`docs/issue-36/reports/implementation.md`, "PR #37 feedback resolution"
and "What did not work") — which is the behavior a blocked verification
mandate is supposed to produce. The single qualification is
presentational, not procedural: PR #37's own title and body never caught
up with what the PR carries at merge (F1 below).

### 3. Step — which specific artifact, if any, is deficient?

Each candidate enumerated in advance at
`docs/issue-36/proposals/execution-observation.md:47-58` is either cleared
with a citation or written up below.

- **(a) The jsdom substitution vs. the feedback comment's three items** —
  partially cleared. Items 1 and 3 are covered twice over: by the record's
  raw jsdom output (`docs/issue-36/reports/implementation.md`,
  `"item1_emptyCellClickOpensDetail": false`,
  `"item3_ariaExpandedAfterOpen": "true"`,
  `"item3_ariaExpandedAfterClose": "false"`) and independently by
  `git show b2f6b63:test/rsb_tests/test_dashboard_dom.py`'s
  `test_row_toggle_click_on_non_button_cell_does_not_open_detail` and
  `test_row_toggle_click_opens_detail_and_flips_aria_expanded`, which
  `git log -1 b2f6b63` states were verified to fail against `b621082^`.
  Item 2's keyboard half is covered by neither → **F3**.
- **(b) `screen-spec.md` / `design-system.md` vs. requirement 6 / AC6** —
  cleared for §1.3/§1.4/§1.5/§1.7 and design-system §6
  (`git show 2c462e0 -- docs/specs/screen-spec.md docs/specs/design-system.md`,
  which match the JS/CSS hunks in the same commit); **not cleared for
  §1.6** (`git show 2c462e0:docs/specs/screen-spec.md`, "expandable row
  below `breakpoint-lg`") → **F2**.
- **(c) The two post-proposal hunt fixes vs. approved scope** — cleared.
  Both land in files
  `git show 403dbd0:docs/issue-36/proposals/implementation.md:70-103`
  already claims, both are small, and the dead-attribute removal is a
  direct consequence of the approved rebinding; relational scope test per
  `docs/issue-36/reports/execution-observation/scout-brief.md:28-29`. The
  escaping fix additionally closes a real injection path the approved spec
  had left half-applied — that proposal's line 75 specifies
  `escapeHtml('#' + number)` for the no-link fallback branch only.
- **(d) Evidence backing AC2** — not cleared as *demonstrated*, and not a
  deficiency of PR #37 either: the wrap-prevention rule exists in the
  merged CSS (`git show 2c462e0 -- src/rsb/web/dashboard.css`,
  `.issue-cell { … white-space: nowrap; }`) and the wrapping element is
  gone; what is missing is any layout-bearing artifact in this repository,
  which no artifact of PR #37 could have supplied given the environment
  `docs/issue-36/reports/implementation.md` ("What did not work")
  documents. Recorded under "What could not be verified".
- **(e) PR #37's title and body vs. what it carries at merge** — not
  cleared → **F1**.

**Step verdict: two artifacts are deficient — PR #37's own title/body as
merged (F1), and `docs/specs/screen-spec.md` §1.6 as left by `2c462e0`
(F2) — plus one verification item that no artifact closes (F3).** Neither
deficiency is in the delivered link-rendering or disclosure-wiring logic:
every hunk of `2c462e0`'s `dashboard.js` / `dashboard.css` /
`test_model.py` traced above resolves correctly, and `b2f6b63`'s
pre-fix-failing tests independently confirm the wiring half.

## Issue #34 F1 — discharged or not?

`git show origin/main:docs/issue-34/reports/execution-observation.md`
lines 343-396 state F1 in two explicitly separate halves. Judged
separately, because that finding's own action item separated them:

**CSS half — discharged structurally, unverified behaviorally.** F1's
impact clause names "`git show 027b6f07:src/rsb/web/dashboard.css` lines
176-188, no `white-space`/wrap-prevention rule" as the shipped defect.
`git show 2c462e0 -- src/rsb/web/dashboard.css` deletes that entire
`.external-link` block (rule plus `:hover`/`:focus`/`:focus-visible`) and
adds `.issue-cell { display: inline-flex; align-items: center; gap:
var(--space-1); white-space: nowrap; }`, while
`git show 2c462e0 -- src/rsb/web/dashboard.js` removes the ↗ glyph
entirely — `numberLinkHtml` emits no icon, so the two-element pair whose
wrap issue #36's body reported ("Flows 표의 Issue 열이 좁아 ↗ 가 번호 아래
줄로 떨어진다") no longer exists in that form, and the replacement pair
(button + `#<n>`) sits inside a `nowrap` inline-flex container. That is a
direct, targeted fix of exactly the phenomenon F1 named. It is
**structurally** discharged: as noted in AC2 above, no artifact measures
rendered layout, so this verdict rests on the CSS declaration shipped in
`2c462e0`, not on a measurement of the deployed page.

**Documentation half — not discharged, and correctly not discharged by
PR #37.** F1's action item states plainly: "What remains un-superseded is
the documentation half — the feedback-resolution paragraph at
`docs/issue-34/reports/implementation.md:92-113` still reads as a complete
layout answer." `git show 2c462e0 --stat` lists exactly six files, none
under `docs/issue-34/`; that paragraph is untouched on `main`. This is not
a deficiency of PR #37: issue #36's body asks for nothing about issue
#34's record, and contract v3's record-ownership rule bars the issue-36
implementation role from editing another issue's role record. F1's
documentation half therefore stays where its own action item put it — in
the human's hands, on issue #34's record.

**Net: the defect that gave rise to this issue is fixed in the merged
tree at `2c462e0`; the record-clarity half of F1 remains open by design,
not by omission.**

## Findings

**F1 (step-level — PR #37's title and body describe phase-1-only content
while the PR merged the phase-2 build).**

- **Impact**: anyone reading
  `https://github.com/tokenmaxxxer/repo-status-board/pull/37` — the
  permanent record of this change — sees the title "issue-36 phase 1:
  link-as-text proposal + row-toggle relocation" and a body opening "No
  code changes yet — this commits the current-state survey, scout brief,
  and build proposal", followed by a "Test plan (phase 2, once approved)"
  with four unchecked boxes. The PR in fact merged `2c462e0`, which
  changes `src/rsb/web/dashboard.js` (106 lines), `dashboard.css` (36),
  `test/rsb_tests/test_model.py` (+26) and both spec files
  (`git show 2c462e0 --stat`). The actual phase-2 outcome, including the
  jsdom substitution and the two hunt fixes, is recoverable only from a
  comment (`issuecomment-5165741708`) and from
  `docs/issue-36/reports/implementation.md`. A reviewer skimming the PR
  page can reasonably conclude no code shipped.
- **Timeline**: PR #37 opened with a phase-1-only body (body text read
  this session, matching `403dbd0` at `2026-08-03T11:03:51Z`) → approval
  `11:08:44Z` → phase-2 commit `2c462e0` `11:28:51Z` → phase-2-complete
  comment `issuecomment-5165741708` `11:29:18Z`, which reports the build
  but does not amend the title or body → merge `11:30:30Z` with both
  still phase-1-shaped.
- **Root cause**: the two-phase contract puts phase-2 work on the same PR
  that carried phase 1, and the mechanism used to report phase 2 was a new
  comment rather than an edit of the PR body. Comments append; the title
  and body are what a reader sees first, and nothing in the workflow
  forces them to be re-synchronized at the phase boundary.
- **Action item**: hand-off only — this role does not edit the observed
  role's artifacts. For the human to judge: whether "update the PR title
  and body to describe what the PR now carries" should become an explicit
  step in the contract's phase-2 checklist. The same pattern is visible on
  issue #34's PR #35 (`docs/issue-34/reports/execution-observation.md`
  records its phase-2 outcome likewise in a comment), so this reads as a
  process shape rather than a one-off lapse by this session.

**F2 (step-level — `screen-spec.md` §1.6 left documenting behavior the
same commit's own source comment declares unimplemented).**

- **Impact**: issue #36's AC6 requires the spec documents to match the
  implementation. `git show 2c462e0:docs/specs/screen-spec.md` §1.6 states
  "Layout choice resolved: side panel at/above `breakpoint-lg` (1200px),
  expandable row below `breakpoint-lg`". The same commit's `dashboard.js`
  comment hunk states the opposite for the narrow case: "there is no
  separate per-table inline expansion path (no `insertDetailRow()` exists;
  the narrow-layout behavior screen-spec.md §1.6 documents remains
  unimplemented, issue-36 survey §2 — out of scope for this change)". A
  reader of the spec is told the board has an expandable-row narrow layout
  that does not exist; a reader of the code is told the spec is stale.
  Neither document points at the other.
- **Timeline**: `403dbd0` `2026-08-03T11:03:51Z` — the survey identifies
  the gap (per the `dashboard.js` comment's own citation, "issue-36 survey
  §2") → `2c462e0` `11:28:51Z` edits `screen-spec.md` §1.3/§1.4/§1.5/§1.7
  and writes the stale-§1.6 statement into a source comment in the same
  commit, leaving §1.6 itself unedited → merged `11:30:30Z` with AC6
  unaddressed for that section.
- **Root cause**: the change scoped its doc sync to the sections it
  touched (Issue/PR cell rendering), which is a defensible scope call, but
  the same commit simultaneously *established* that §1.6 is stale by
  writing that fact into the code. Discovering a spec defect and declaring
  it out of scope inside the artifact, without leaving any marker in the
  spec itself, leaves the spec asserting something the codebase now
  formally denies.
- **Action item**: hand-off only. For the human to judge: whether a
  one-line "unimplemented" marker in `screen-spec.md` §1.6 belongs in a
  follow-up, or whether the narrow-layout behavior should be built. Either
  way the decision is the human's; this role files no issue (contract v3 —
  issues are user-authored only).

**F3 (verification item — the keyboard half of the approval-attached
feedback comment's item 2 is closed by no artifact).**

- **Impact**: `issuecomment-5165555695` required, as minimum check (2),
  "버튼만 Tab 으로 포커스해 Enter/Space 로 열고 닫힌다". Every artifact that
  exercises the control activates it with `.click()`:
  `docs/issue-36/reports/implementation.md`'s jsdom section says so
  explicitly ("the activation itself was exercised via `.click()`"), and
  `git show b2f6b63:test/rsb_tests/test_dashboard_dom.py`'s four
  `.row-toggle` tests all call `decBtn.click()`. So issue #36's AC3,
  worded "키보드만으로 열고 닫을 수 있다", rests on the inference that a
  native `<button>` activates on Enter/Space per the HTML specification —
  a strong inference, given `rowToggleButtonHtml` emits a real
  `<button type="button">`
  (`git show 2c462e0 -- src/rsb/web/dashboard.js`) and the record's jsdom
  run confirms `focus()` moves `document.activeElement` onto it — but an
  inference, not an observation.
- **Timeline**: feedback comment `2026-08-03T11:08:45Z` → phase-2 commit
  `2c462e0` `11:28:51Z` with the jsdom substitution and its explicit
  caveat → merge `11:30:30Z` → `b2f6b63` (`2026-08-03T21:31:44+09:00`)
  adds a durable jsdom harness covering the click path but not keyboard
  activation.
- **Root cause**: environmental, and disclosed rather than concealed — no
  browser automation exists in the sandbox
  (`docs/issue-36/reports/implementation.md`, "What did not work": Chrome
  `crashpad`/`ProcessSingleton` permission errors, no
  Playwright/Selenium/Puppeteer), and jsdom does not translate `keydown`
  into button activation
  (`docs/issue-36/reports/execution-observation/scout-brief.md:18-21`,
  citing `jsdom#1634`). The observed role named this gap at the exact
  point the claim is made, which is the correct handling of a blocked
  verification; the gap is nonetheless still open.
- **Action item**: hand-off only. For the human to judge: a one-time
  manual Tab + Enter/Space pass against
  `https://tokenmaxxxer.github.io/repo-status-board/` would close AC3's
  last inference cheaply, and would settle AC2's rendered-layout claim in
  the same look, since both concern the same page.

## What could not be verified

- **AC2's rendered single-line claim** and **AC1's rendered blue**: no
  layout- or paint-bearing artifact exists in this repository. jsdom
  performs no layout
  (`docs/issue-36/reports/execution-observation/scout-brief.md:18-21`), so
  the observed role's run and `b2f6b63`'s harness are both silent on it.
  Reported unsettled with its reason rather than settled by re-running,
  per `docs/issue-36/proposals/execution-observation.md:100-105`.
- **AC5's 55-passed figure**: re-running the observed role's tests is
  prohibited for this role. Reported as claimed by
  `docs/issue-36/reports/implementation.md` ("Tests"), with `b2f6b63`'s
  63/63 on a later tree noted as indirect corroboration only.
- **The `b621082^` failure verification behind `b2f6b63`'s tests** is
  itself taken from `git log -1 b2f6b63`'s commit message — a third-party
  artifact read, not a re-execution.

## Upstream basis

- Issue #36 (`gh issue view 36`) — the seven acceptance criteria and the
  two-step execution plan this record judges step 1 against.
- Issue-level approval `APPROVE issue-36/execution-observation`
  (`issuecomment-5175870378`, `2026-08-04T07:24:27Z`) — the gate that
  opened this phase, verified against `docs/specs/approvers.md`.
- `docs/issue-36/proposals/execution-observation.md` @ `21cba3a` — this
  role's own approved phase-1 proposal, whose §0-§3 fixed the verdict
  levels, evidence sources, step-candidate list, and record shape in
  advance.
- `docs/issue-36/reports/execution-observation/survey.md` and
  `scout-brief.md` @ `21cba3a` — the current-state survey's seven gaps and
  the scout pass's must-bes, which supplied the
  demonstrated/asserted-only labelling rule and the three-item disclosure
  checklist used above.
- `docs/issue-34/reports/execution-observation.md` @ `origin/main` — F1,
  whose discharge this session was asked to judge.
- Role-handoff contract v3 §19 (two-phase gating, single-account approval
  path) and §20 (record fields).

## Open findings

F1, F2 and F3 above are open. All three are handed to the human on this
role's own PR; none is filed as an issue (contract v3 — issues are
user-authored only), and none is fixed here (this role never edits the
observed role's `src/`, `test/`, `docs/specs/`, or record). Issue #34's
F1 documentation half also remains open on issue #34's record, as judged
in the "Issue #34 F1" section above — untouched by PR #37, and correctly
so.

## Open-finding resolution path

This role cannot resolve F1, F2 or F3 itself: F1 lives on the observed
role's PR metadata, F2 in `docs/specs/screen-spec.md`, and F3 requires a
browser this role is barred from using against the observed code — all
three outside this role's write surface (independence requirement, and
`docs/issue-36/proposals/execution-observation.md:106-117`). Resolution is
therefore in the human's hands, through one of:

- **Reviewing**: the approver reads F1/F2/F3 on PR #49 and judges each.
  Merging PR #49 accepts this record including its findings; closing it
  unmerged refuses it.
- **Filing**: if F2 warrants code or spec work, the human authors a new
  issue for it (issues are user-authored only under contract v3); this
  role neither files nor drafts one. F1 is a process observation better
  settled by amending the contract's phase-2 checklist than by a code
  issue.
- **Closing in place**: F3 needs no new issue if the human simply performs
  the one-time manual Tab + Enter/Space check on
  `https://tokenmaxxxer.github.io/repo-status-board/` and notes the
  result — that single look also settles AC2's rendered-layout claim and
  the behavioral half of issue #34 F1's CSS discharge.

## Next steps

1. Human reviews PR #49 and decides on this record (merge = acceptance,
   close unmerged = refusal). Nothing further from this role is pending
   until then.
2. Issue #36's execution-plan step 2 also names a parallel
   `conformance-review` role; this record speaks only to PR #37 and
   renders no verdict on that role's work
   (`docs/issue-36/proposals/execution-observation.md:118-119`). The plan
   step is complete for this role's half only.
3. If the human runs the manual browser pass described above, F3 closes
   and AC2/AC3 move from asserted-only/inferred to demonstrated; that
   result belongs in a human-authored note or issue, not in this record,
   which is closed to further edits once PR #49 is judged.
