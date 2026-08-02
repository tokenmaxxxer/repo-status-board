# Current-state survey — issue #23

Scope of the survey: the write set issue #23 touches — spec copy, data
model, JSON serialization, and the web dashboard's flows rendering +
summary aggregation.

## 1. Spec copy drift (`docs/specs/flows-schema.md`)

Local mirror is dated "as of 2026-07-31" and documents `flows[]` with
only `issue`, `stage`, `stage_derived`, `roles`, `prs` (§2.2). No `plan`
field anywhere in the doc, and the worked example (§7) has no `plan` key
either. The issue body pastes the exact upstream contract for `plan`
(type, parsing rule, `null` vs `[]` semantics, step-line format
`- [ ] step <N> <role>[ ‖ <role2> ...]`) — this is the re-sync source,
not a separate upstream fetch (no local on-the-record checkout exists in
this environment; the issue text is presented as "on-the-record 쪽 확정
사실", i.e. already-confirmed source-of-truth content quoted for this
sync).

## 2. Data model (`src/rsb/model.py`)

`Flow` dataclass (line 31-38): `repo, issue, stage, stage_derived, roles,
prs`. No `plan` field. `normalize_payload()`'s flow comprehension (line
144-157) reads `fl["issue"]`, `fl["stage"]`, `fl["stage_derived"]`,
`fl.get("roles", [])`, `fl.get("prs", [])` — `plan` is silently dropped
today (present in the raw payload per the issue, discarded because
nothing reads the key). Same pattern as `roles`/`prs`: default via
`.get()` since `plan` can be `null` (absent step block) as well as `[]`
(header present, no valid steps) — both must survive as distinct values
per the issue's requirement, so `.get("plan")` (defaulting to `None`,
not `[]`) is the correct extraction, mirroring how `stage`/`stage_derived`
are read directly (required) while list-shaped optional fields use
`.get(..., [])`. `plan` is optional-but-distinct (`None` is a valid,
different-meaning value from `[]`), so neither existing pattern applies
verbatim — needs `fl.get("plan")` with no default-to-list.

No `PlanStep` dataclass exists yet. Each step is
`{step: int, roles: [string], done: bool}` per the issue — a small
dataclass (`step`, `roles`, `done`) parallels the existing `FlowRole`
dataclass shape (line 24-28).

`render.py`'s `_dataclass_to_dict()` (line 159-166) recurses generically
over dataclasses/lists/dicts — a new `PlanStep` dataclass and a `plan`
field on `Flow` need no `render.py` changes; serialization is automatic.
Same for `render_text()` (plain-text CLI renderer) — issue #23's
acceptance criteria are dashboard (web) rendering only; the text
renderer isn't named in requirements or acceptance criteria, so a
plan-rendering addition there is not implied by the issue (confirmed:
issue body's "구현 시 터치 포인트" section names only `model.py` and
`dashboard.js`, not `render.py`'s `render_text`).

## 3. Web dashboard (`src/rsb/web/dashboard.js`)

- `flowRows()` (line 124-136): renders `stage`, `roles` (role:loop_state
  badges), `prs`, `repo` per flow row. No plan column today.
- `renderDetailPanel()` (line 207-222): per-issue detail panel, already
  joins `flow`, `decision` (from `decisions[]`), `sessions[]`, `ledger`
  by `(issue, repo)` via `findDetail()` (line 198-205) — this is the
  established join pattern issue #23 requirement 3 wants extended to
  plan steps (join each step's `roles` against `flow.roles`
  `{role, loop_state, verdict}` and against `decisions[]`
  `{pr, awaiting, ...}` for pending-PR info). `findDetail()` already
  pulls `detail.flow` and `detail.decision` — both already carry what
  step-level join needs (`flow.roles`, `decision.pr`/`decision.awaiting`);
  no new data fetch, just a lookup helper keyed by role name.
- `selectSummary()` (line 28-49): the aggregation bug. `flows: {
  label: \`${data.flows.length} flows in progress\`, status:
  "status-neutral" }` counts every flow in `data.flows` regardless of
  `stage` — includes `delivered` and `closed` stage flows in the "in
  progress" count. Per `flows-schema.md` §2.2, `stage` is one of
  `proposal | approved | implementing | delivered | closed`, or (when
  `stage_derived: false`) an arbitrary raw `loop_state` string. "In
  progress" should count `proposal | approved | implementing` (excludes
  the two terminal stages `delivered`/`closed`) — but `stage_derived:
  false` rows hold a string that is by construction never one of those
  five, so a naive `["proposal","approved","implementing"].includes(stage)`
  check silently excludes every raw/unmapped flow from the count too,
  even though such a flow is almost certainly still active (unmapped
  `loop_state` values arise mid-flow, not at terminal states — closure
  produces well-known states). This is exactly the "결정하고 문서화"
  ask in requirement 4: the fix must pick and document how
  `stage_derived: false` rows count toward "in progress".
- No existing `plan`-adjacent rendering exists in `dashboard.js` to
  extend — this is new render surface, not a fix to existing plan code.

## 4. Styling (`src/rsb/web/dashboard.css`)

Token set already covers what a step list needs without new tokens:
`.badge` + `.status-*` (existing role:loop_state badges reuse this for
step status), `.mono` (existing convention for numeric/id-like text —
step numbers, role names already use `.mono` in `flowRows`/`sessionRows`
elsewhere), `.text-secondary` (existing convention for muted/absent
states, e.g. `plan: null`). No breakpoint or layout token gaps found for
a step list rendered inside the existing `.region`/`.detail-panel`
containers.

## 5. Tests (`test/rsb_tests/`)

- `fixtures.py`: `WORKED_EXAMPLE`, `EMPTY_PAYLOAD`, `RAW_STAGE_PAYLOAD`,
  `WITH_LAST_ACTIVITY_PAYLOAD` — none include a `plan` key today (predates
  the field). `RAW_STAGE_PAYLOAD`'s flow (`stage_derived: False`) is the
  fixture requirement-4's aggregation-count decision needs a test against.
- `test_model.py`: asserts field-by-field on normalized dataclasses;
  a `plan` field needs equivalent coverage (`plan: null` passthrough,
  `plan: []` passthrough as distinct from `null`, `plan` with steps →
  `PlanStep` objects with correct `roles` list for parallel steps).
- No `test_dashboard.js`-equivalent JS test file exists — `dashboard.js`
  exports `{ ageBucket, ageBucketStatus, selectSummary, isPageEmpty }` via
  the `module.exports` guard (line 315-317) specifically for testability,
  but grepping `test/` finds no JS test runner/harness in this repo (no
  `package.json`, no `jest`/`node --test` config, no `test_dashboard*`
  file). `selectSummary`'s existing test coverage, if any, is not part of
  `test/rsb_tests/` — Python-side aggregation-adjacent logic has no JS
  counterpart test today. This is a pre-existing gap, not one issue #23
  introduces; phase 2 will need to decide how (or whether) to add JS-side
  test coverage for the `selectSummary` fix given no harness currently
  exists.

## 6. Prior art in this repo

`docs/issue-13/reports/implementation.md` (F1-F4 dashboard fixes, merged)
is the closest precedent: same file (`dashboard.js`), same style of
"spec says X, shipped code does Y, minimal-diff fix" reasoning, same
phase-1/phase-2 structure. Its F1 fix threaded a new top-of-function
check into `renderData()` without touching unrelated render logic — a
useful shape precedent for the aggregation fix in requirement 4 (small,
localized change to `selectSummary()`, not a `dashboard.js`-wide
rewrite).

## Write-set summary (what phase 2 will actually touch)

- `docs/specs/flows-schema.md` — re-sync `plan` field, update as-of date.
- `src/rsb/model.py` — `PlanStep` dataclass, `Flow.plan` field,
  `normalize_payload()` extraction.
- `src/rsb/web/dashboard.js` — plan rendering (flow row and/or detail
  panel — decided in proposal), step-role join against `flow.roles` +
  `decisions[]`, `selectSummary()` in-progress-count fix.
- `src/rsb/web/dashboard.css` — only if the step list needs a rule the
  existing token set doesn't cover (survey found none required; proposal
  will confirm at build time).
- `test/rsb_tests/fixtures.py`, `test/rsb_tests/test_model.py` — plan
  fixture data + normalization coverage.
- No `src/rsb/render.py`, `src/rsb/webserver.py`, or `src/rsb/fetch.py`
  changes — none of these three touch `plan` or `stage` filtering logic;
  confirmed by reading all three in full.
