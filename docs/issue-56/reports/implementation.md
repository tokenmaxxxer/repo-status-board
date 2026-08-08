# Implementation record — renderErrors 접힘 처리 + .number-link 실측 판정 (issue #56, phase 2)

code_under_review: src/rsb/web/dashboard.js, src/rsb/web/dashboard.css, test/rsb_tests/test_dashboard_dom.py, docs/specs/screen-spec.md, docs/specs/design-system.md
loop_state: landed

## Why

Approved via issue #56 comment `APPROVE issue-56/implementation`
(jjongkwann, 2026-08-04T10:29:48Z, single-account mode — PR #57 author
and approver are the same account, both listed in
`docs/specs/approvers.md`). Executes
`docs/issue-56/proposals/implementation.md`'s "What will be done"
exactly as approved, resting on
`docs/issue-56/reports/implementation/survey.md` and
`docs/issue-56/reports/implementation/scout-brief.md`.

## What was done

Executed `docs/issue-56/proposals/implementation.md`'s "What will be
done" exactly as approved, no content deviation (see "Rationale for
deviations" below for the one operational, non-content deviation).

1. **`dashboard.js`**: removed `renderErrors(errors)` (previously
   `dashboard.js:355-365`) and its call site inside `renderData`
   (previously `dashboard.js:632`, `${renderErrors(data.errors)}`,
   between the Sessions and Hygiene sections). The rest of `renderData`'s
   render order (Decision queue → Flows → Sessions → Hygiene →
   Accounting) is unchanged.
2. **`dashboard.css`**: `.number-link` (`:248-259`) gained `min-width:
   24px; min-height: 24px; display: inline-flex; align-items: center;
   justify-content: center` — the same box-model pattern `.row-toggle`
   already uses (`dashboard.css:220-227`). Verified against both real
   DOM contexts (`.issue-cell` pairing it with a `.row-toggle` button;
   the bare `.mono` cell where it's the sole content) via jsdom
   `getComputedStyle` loaded against the actual shipped `dashboard.css`
   — the rule resolves with no override in either context, and neither
   ancestor collapses the child's own min-box (`.mono` sets only
   `font-family`; `.issue-cell` sets `align-items: center`, not
   `stretch`). No `gap`/alignment adjustment in `.issue-cell` was needed.
3. **`screen-spec.md`**: §1.9 "Errors panel — `ErrorListItem`" deleted.
   §2.5 "Partial failure (banner)" gained one line stating the banner is
   the only surface that displays partial-failure repo errors, naming
   the removed duplicate. **`design-system.md`**: §5 prose (24×24px
   guaranteed-control list) and the §6 `DataTable` component-inventory
   row both now list `.number-link` among the 24×24px-guaranteed
   controls.
4. **`test_dashboard_dom.py`**: added
   `test_partial_failure_raw_message_absent_from_main_content_and_errors_section_gone`
   — document-scoped to `#main-content` itself (not any one child
   element within it, per issue-38 execution-observation F1's root
   cause) — asserting a failed repo's raw message text is absent from
   `#main-content`, that no `"Errors"` `<h2>` exists, that no
   `.error-list` exists, and that the same message IS present
   (collapsed) inside `#partial-banner`.
5. This section plus "Requirement 2" below carry the F3 실측 판정 as
   required.

## Requirement 2 — WCAG 2.5.8 exception determination (실측 보고)

**판정: 인라인 예외 불성립 (exception does not apply)** → 최소 크기
CSS를 적용한다(이슈 #56 요구사항 2의 괄호 조건대로, "What was done" §2).

1차 출처(W3C `Understanding SC 2.5.8`,
https://w3c.github.io/wcag/understanding/target-size-minimum.html,
scout-brief에서 직접 인용)의 인라인 예외 문구는 "target이 문장 안에
있거나, 그 크기가 non-target 텍스트의 line-height로 제약되는 경우"로
좁게 한정된다. 보조 출처(TestParty, AllAccessible)는 표 셀·리스트
항목의 단독 링크를 명시적으로 예외 미적용 사례로 든다: "the exception
doesn't universally apply to all text links, only to those which
actually are constrained by line-height... links inside table cells or
list items would need to meet the 24×24 requirement unless they are
genuinely constrained by surrounding text formatting."

`.number-link`가 실제로 등장하는 두 DOM 문맥(survey §2,
`dashboard.js`):

- `.issue-cell` 안 — 옆에 있는 것은 `.row-toggle` 버튼(타깃)뿐, 둘러싸는
  산문 텍스트가 없다.
- `.mono` 셀 안 — 링크가 셀의 유일한 내용물, 마찬가지로 산문 텍스트가
  없다.

두 문맥 모두 "문장 안" 조건과 "non-target 텍스트의 line-height로
제약" 조건 어느 쪽도 충족하지 않는다 — 인라인 예외 불성립. issue-38
본문의 8×17px 실측치는 *문제의 크기*를 잰 것이고, F3가 지적한 공백은
*예외 성립 여부 판정* 자체가 issue-38 승인 결정
(`docs/issue-38/proposals/implementation.md:310-312`, phase-2 실측
확인을 조건으로 걸었음)이 요구한 그대로 한 번도 수행되지 않았다는
것이었다 — 이 절이 그 판정이다.

실제 픽셀 렌더링 측정(브라우저·스크린리더)은 이 샌드박스에 그 수단이
없어(proposal Constraints, survey §2 — `google-chrome`/`chromium`
바이너리 부재, `python3 -c "import playwright"` →
`ModuleNotFoundError`, issue-38 phase 2가 겪은 것과 동일한 제약) CSS
박스 모델 계산값 대조(jsdom `getComputedStyle`, 실제 `dashboard.css`
로드, "What was done" §2)로 대체했다 — proposal의 Constraints가 이미
이 대체를 명시적으로 예정해 두었으므로(승인된 계획 그대로), 이는
Rationale for deviations 대상이 아니라 계획된 대체다.

## What did not work

None in the built content (code/CSS/docs/test all landed as approved,
first attempt, no discard-and-redo). The one non-content hiccup is
recorded under "Rationale for deviations" below since it changed how a
verification step was carried out.

## Rationale for deviations

The approved proposal's "What will be done" content (dashboard.js,
dashboard.css, screen-spec.md, design-system.md, the new test) landed
exactly as written — no content deviation. The one deviation is
operational, in how the test suite was *invoked*:
`docs/issue-44/reports/test-authoring.md` documents `PYTHONPATH=src
python -m pytest test/` as this sandbox's entry point (the package
isn't `pip install -e .`'d in), and this proposal's "How you'll know it
worked" implicitly assumes that same invocation. This session's sandbox
refused any command carrying a `VAR=value` env-prefix (e.g.
`PYTHONPATH=src ...`) as needing an approval it could not obtain in a
headless, single-shot session with no later turn to grant it. Tests
were run instead via `cd src && python3 -m pytest ../test/ -q` —
equivalent in effect (`python -m` prepends the invocation cwd to
`sys.path`, so `import rsb` resolves the same way) and touching no path
outside the frozen write set. This changed *how* verification ran, not
*what* was verified or *what* was built, and is disclosed here per the
deviation-tracking requirement rather than left implicit.

## Doc-placement ladder

- [x] `docs/specs/screen-spec.md` §1.9 deleted, §2.5 augmented — same
      turn as the code (see "What was done" §3).
- [x] `docs/specs/design-system.md` §5 prose + §6 `DataTable` row —
      same turn as the code (see "What was done" §3).
- [x] `docs/issue-56/reports/implementation.md` (this file).

## Tests

`cd src && python3 -m pytest ../test/ -q` — **64 passed, 2 failed**.

The new test
(`test_partial_failure_raw_message_absent_from_main_content_and_errors_section_gone`)
is among the 64 passing. The 2 failures
(`test_row_toggle_click_opens_detail_and_flips_aria_expanded`,
`test_row_toggle_reactivating_open_button_closes_it`) are **pre-existing
on `main`, unrelated to this issue's write set** — confirmed via `git
show f353910` (issue-38 phase 1) adding an unguarded
`window.matchMedia(WIDE_LAYOUT_QUERY)` call at `dashboard.js:508` that
jsdom's environment does not implement by default, so any row-toggle
click reaching that branch fails inside this DOM-wiring test harness.
Out of scope for issue #56 per this session's task instructions —
disclosed here as pre-existing, not fixed.

`node --check src/rsb/web/dashboard.js` — clean.

grep verification (matches proposal's "How you'll know it worked"):

- `grep -rn "renderErrors" src/ test/` — 0 functional hits (the only
  text hit is the removed name's mention inside the new test's own
  explanatory comment, expected).
- `grep -n "ErrorListItem" docs/specs/screen-spec.md` — 0 hits (§1.9
  confirmed deleted).
- `grep -n "number-link" docs/specs/design-system.md` — 2 hits, both
  stating the 24×24px minimum size.

## Warrant hunt

### before-landing — stance 0: assume the fix is bypassable — find a path where the claimed guarantee does not hold

Verdict: NO FINDING
Seed: docs/issue-56/proposals/implementation.md diff — dashboard.js renderErrors() removal + call-site removal, dashboard.css .number-link min-24px hit-target addition (dashboard.css:248-259)
cap_seconds: 120
tier: default
diff_stat_lines: 148 (5 files)
started_at: 2026-08-08T02:15:00Z
ended_at: 2026-08-08T02:31:32Z

Investigated two candidate bypasses, both suggested by the hunt prompt itself, and reproduced neither as an actual violation:

1. **Total-failure path reaching `#main-content`.** Traced every use of `data.errors[].message` in dashboard.js (`renderFullError` at line 566 and the partial banner at line 588 are the only two). Built a jsdom repro (`node` + `test/node_modules/jsdom`, same harness convention as `test/rsb_tests/test_dashboard_dom.py`) feeding a payload where `generated_at_by_repo` is empty and `errors` has one entry containing a marker string. Confirmed `renderFullError()` does put the message text into `#main-content` (`main.textContent.includes(marker) === true`, `#partial-banner` stays empty) — so the literal "the only surface is `#partial-banner`" wording is technically false for total failure. But the actual substance of the guarantee (never raw/uncollapsed) still holds: `renderFullError` routes the message through the same `collapsibleDetailHtml()` helper the banner uses (`<details><summary>Details</summary><p>${escapeHtml(...)}</p></details>`, no `open` attribute — collapsed by default, HTML-escaped). This is also pre-existing, unchanged-by-this-diff code (only `renderErrors()`'s definition and its call site were removed), and the proposal's guarantee is explicitly scoped to "partial-failure," not total failure. Not a repro of a defect — it's an accurately-scoped pre-existing mechanism.
2. **`.number-link` CSS override in one of its two DOM contexts.** Grepped dashboard.css for every rule touching `.number-link`, `.mono`, `.issue-cell`, and any bare `a`/`a:link` reset — found none that touch `display`/`min-width`/`min-height` besides the new rule itself (only `:hover`/`:focus`/`:focus-visible` variants exist, touching `text-decoration`/`outline` only). Built a jsdom repro loading the real dashboard.css against both real DOM shapes (`<td class="mono"><span class="issue-cell"><button class="row-toggle">...<a class="number-link">` and `<td><span class="mono"><a class="number-link">`) and read `getComputedStyle` — both resolve to `display: inline-flex; min-width: 24px; min-height: 24px; align-items: center` with no override. `.mono` only sets `font-family`; `.issue-cell` sets `align-items: center` (not `stretch`), so it doesn't collapse the child's own min-box. Separately found `numberLinkHtml()`'s pre-existing fallback (`buildGithubUrl` returns null when `ownerName` is missing) renders plain escaped text with no `<a class="number-link">` element at all — but since that's not a link/interactive element in that branch, WCAG 2.5.8 (target size) doesn't apply to it, so it isn't a bypass of the claimed guarantee either.

No runnable repro of an actual violation of either claimed guarantee (as scoped by the proposal) was produced. Returning NO FINDING per the "no repro, no finding" rule.

closed_checks:
- full-test-suite: `cd src && python3 -m pytest ../test/ -q` — 64
  passed, 2 pre-existing failures (matchMedia gap, `f353910`, out of
  scope — see "Tests" above). code_sha: this branch's pending commit
  (code_under_review: as listed above).
- syntax-check: `node --check src/rsb/web/dashboard.js` — clean.
- grep-renderErrors-removed: `grep -rn "renderErrors" src/ test/` — 0
  functional hits (see "Tests" above).
- grep-ErrorListItem-removed: `grep -n "ErrorListItem"
  docs/specs/screen-spec.md` — 0 hits.
- grep-number-link-24px: `grep -n "number-link"
  docs/specs/design-system.md` — present, 24×24px minimum size stated.
- before-landing-warrant-hunt: stance 0 (bypass claimed guarantees) —
  NO FINDING (see "Warrant hunt" above).

## Open findings

None — the before-landing warrant hunt (above) returned NO FINDING, and
no other check surfaced an issue.

## Next steps

None — phase 2 is complete. This record is finalized (`loop_state:
landed`); commit follows immediately.

## Open-finding resolution path

N/A — no open findings (see "Open findings" above).
