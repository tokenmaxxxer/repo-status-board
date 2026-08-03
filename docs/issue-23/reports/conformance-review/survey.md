# Conformance-review survey (issue #23)

Subject: PR #24 (`issue-23/implementation`, merged to `main` at commit
`4ea2e48`) checked against issue #23's 6 acceptance-criteria checkboxes
and `docs/specs/flows-schema.md` §2.2 (the `plan` field contract).
Scout: ran, 1 stage, saturated immediately — see `scout-brief.md`.

## What's merged (main, as of this survey)

- `docs/specs/flows-schema.md` — re-synced by PR #24: header "as of"
  date bumped to 2026-08-03, §2.2 gained a `plan` table row and JSON
  example key, §7 worked example gained a `plan` key.
- `src/rsb/model.py` — `PlanStep` dataclass (line 32-36: `step, roles,
  done`), `Flow.plan: object` field (line 46), `normalize_payload()`
  extraction (line 190-196) reading `fl.get("plan")`/`fl["plan"]`.
- `src/rsb/web/dashboard.js` — `isFlowInProgress()` (line 45-47),
  `selectSummary()`'s `flows` chip now filters through it (line 60);
  `planCellLabel()` (line 156-162) feeding a new "Plan" column in
  `flowRows()` (line 172); `buildPlanSteps()` (line 253-277, pure/no-DOM)
  and `renderPlanSection()` (line 278-296) feeding `renderDetailPanel()`
  (line 317, 323) via the existing `findDetail()` per-issue join.
- `test/rsb_tests/fixtures.py` — `PLAN_NULL_PAYLOAD`, `PLAN_EMPTY_PAYLOAD`,
  `PLAN_STEPS_PAYLOAD` (two PRs on one role, steps listed out of order).
- `test/rsb_tests/test_model.py` — 8 new tests, 4 Python-side
  (`normalize_payload` plan handling) + 4 Node-subprocess (`require()`s
  the real `dashboard.js`, no JS framework added).
- `docs/issue-23/reports/implementation.md` — phase-2 record, claims all
  6 ACs done, all 4 second-round cross-review findings (missing-key
  `.get()` rationale, aggregation wording, step-sort/multi-PR/empty-plan
  render spec, accessibility-out-of-scope) addressed.
- Test run this session: `python3 -c "import sys;
  sys.path.insert(0,'src'); import pytest;
  sys.exit(pytest.main(['test/','-q']))"` → **41 passed**, 0 failed —
  matches implementation.md's claimed count. (Bare `pytest test/ -q`
  fails to collect — `ModuleNotFoundError: rsb` — the `sys.path` prefix
  is required; this matches the repo's own documented invocation, not a
  new problem.)

Per the role directive, phase 2 will verify the 6 ACs and the schema
contract against the artifact and spec directly — the summary above and
`implementation.md`'s self-report are read here only to orient the
requirement list, not accepted as verdicts.

## Issue #23's 6 acceptance criteria (verbatim source, for the requirement list)

1. 스펙 사본에 §2.2 `plan` 행과 worked example이 원본과 일치
2. plan 있는 이슈: 스텝 순서·역할·done 상태가 화면에 보임
3. plan-only 이슈(보드 레코드 없음)가 생성 직후 flows에 나타남
4. 스텝별 역할에 loop_state/verdict, 대기 PR이 조인되어 표시
5. 요약 칩이 진행 중 flow만 셈 (delivered/closed 제외 기준 문서화)
6. `plan: null` vs `[]` 렌더링 구분(또는 동일 취급 결정)이 기록됨

## Observations shaping requirement decomposition (not verdicts)

- **AC1** bundles three separately-checkable facts: (a) §2.2 table row
  wording, (b) §7 worked-example key, (c) as-of date. Each is a distinct
  grep/diff target.
- **AC2** bundles three: step order, per-step roles, per-step done state
  — all rendered by `renderPlanSection()`, but each is a separate visual/
  logic fact worth its own row (a bug could hit one without the others,
  e.g. wrong sort but correct role display).
- **AC3** is the one criterion whose subject (an issue is created →
  `flows[]` gets an entry) is **upstream** (`on-the-record`'s `flows
  --json` producer) per `flows-schema.md` §2.2's own text ("A plan-only
  subject... still gets a `flows[]` entry as soon as the issue is
  created" describes provider behavior). This repo (`rsb`) only
  consumes and renders `data.flows` as received — there is no local
  fixture or live upstream payload in this repo/environment to drive a
  real plan-only issue end to end. What **is** checkable locally: does
  `rsb`'s rendering path avoid dropping/filtering a flow entry that has
  no matching `decision`/`session`/`ledger` data (the shape a genuinely
  plan-only flow would have)? `findDetail()`/`renderDetailPanel()`'s
  early-return guard (`if (!detail.decision && !detail.flow &&
  detail.sessions.length === 0 && !detail.ledger)`) keys off `!detail.flow`
  — a plan-only flow entry present in `data.flows` sets `detail.flow`
  truthy regardless of decision/session/ledger, so the guard does not
  fire and the row/detail panel render normally. This is the scoped,
  locally-verifiable half of AC3; the "shows up the instant the issue is
  created" timing claim is provider-side and out of this repo's reach —
  flagged as a likely **Unverifiable-within-this-repo** candidate for
  phase 2 to formally record, not silently skip.
- **AC4** bundles two joins: role→`flows[].roles` (loop_state/verdict)
  and role→`decision_queue` (pending PR), both inside `buildPlanSteps()`.
  PR #24's own record (finding #3b) claims the join returns *all*
  matching PRs, not just the first — a specific, checkable sub-fact.
- **AC5** bundles two: (a) the count itself excludes delivered/closed,
  (b) the `stage_derived:false` handling is *documented*, not just coded
  — the AC's own text says "기준 문서화" (criterion: documented), so a
  code fix with no documentation trace is not a full AC5 pass even if the
  count is numerically correct. Documentation could live in the schema
  doc, the dashboard.js comment, and/or the implementation record —
  phase 2 needs to check at least one durable location, not just runtime
  behavior.
- **AC6** similarly has a "recorded" clause distinct from "renders
  distinctly" — `buildPlanSteps()`/`planCellLabel()` returning/rendering
  different values for `null` vs `[]` is one fact; a record of that
  decision (schema doc, code comment, or implementation record) is a
  second, separately-checkable fact.
- **Schema §2.2 contract (task's second axis, distinct from AC1)**: AC1
  checks the *doc copy* against the *upstream text*; the schema-contract
  check is whether the *implementation* (`PlanStep`/`Flow.plan` shape,
  `normalize_payload()`'s null/[]/missing-key handling) conforms to what
  §2.2 itself specifies. The schema table documents `null` vs `[]` as
  "distinct, never interchangeable" but is silent on the missing-key
  case (pre-`plan`-field legacy payloads) — PR #24 adds a repo-local
  policy (missing key ≡ `null` ≡ `None`) that is an *extension* of the
  schema, not something §2.2's text mandates either way. Phase 2 should
  record this distinction explicitly (schema-silent-but-implementation-
  reasonable) rather than call it either a pass or a violation without
  qualification.

## Constraints on phase 2's verification depth

- No browser/live server was driven this session (matches the same
  limitation `docs/issue-4/reports/conformance-review.md` recorded for
  its own review) — DOM-rendering claims (AC2, AC4, AC6's "distinct
  rendering") are checkable by code inspection plus the Node-subprocess
  tests added in PR #24 (which call the real `dashboard.js` functions,
  not a reimplementation), not by eyeballing a running page.
- AC3's provider-side timing claim cannot be driven at all from this
  repo/environment (no `on-the-record` checkout, no live `spawn.py`) —
  noted above as a phase-2 Unverifiable candidate for the provider-timing
  half specifically, distinct from the locally-verifiable
  non-filtering-behavior half.

## Write-set for this role

This role only reads `src/`, `test/`, `docs/specs/`, and issue #23; it
writes only `docs/issue-23/reports/conformance-review/`,
`docs/issue-23/proposals/conformance-review.md`, and (phase 2, after
approval) `docs/issue-23/reports/conformance-review.md`. No `src/`/`test/`
change is proposed or made by this role.
