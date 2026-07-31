# issue-1 implementation — current-state survey (phase 1)

Author: implementation role, issue #1 (`상황판 CLI v1`).
Date: 2026-07-31.

## 1. Repo state

`repo-status-board` is a fresh repo (2 commits before this one):

- `96efd24` Init repo-status-board — adds `README.md` only.
- `09eb56d` Declare board: approvers allowlist — adds `docs/specs/approvers.md`
  (single entry: `JiwonJung94`).

There is no `src/`, no `test/`, and no prior `docs/issue-1/` tree. Nothing to
build on; this is a greenfield CLI.

`docs/specs/approvers.md` lists exactly one account (`JiwonJung94`), and that
account is also the author of issue #1 and of this branch's commits. Per the
role-handoff contract this puts phase-2 gating into **single-account mode**:
phase 2 opens on an issue-#1 comment whose entire body is exactly
`APPROVE issue-1/implementation`, posted by `JiwonJung94` (an issue-level PR
review Approve would also work in principle, but since author == sole
approver, a PR review from the same account does not count — the contract
requires the approver be a *different* account from the PR author for the
review path; the comment path is what applies here).

## 2. Issue #1 spec (verbatim read via `gh issue view 1`)

> `on-the-record`의 `spawn.py flows --json`(이슈: tokenmaxxxer/on-the-record#171,
> 스키마: docs/specs/flows-schema.md)을 데이터 소스로 하는 상황판 CLI.
>
> 1. `rsb` (또는 board.py) 명령: 여러 보드 레포를 설정 파일로 등록하고, 한 화면에
>    (a) 결정 대기열(최상단 — 사람이 지금 해야 할 일), (b) 이슈별 플로우 단계 표,
>    (c) 실행 중 세션, (d) 이슈별 비용 합계, (e) 위생 경고를 출력한다.
> 2. 데이터는 오직 flows --json 스키마로만 읽는다 — spawn.py 내부 파일 직접 파싱
>    금지. 스키마 버전 불일치 시 명확한 오류.
> 3. 갱신 모드: 1회 출력이 기본, --watch 로 주기 재렌더.
> 4. v1 은 CLI 만 — HTML 렌더러는 후속 이슈.
>
> 선행 조건: on-the-record#171 머지. 이 이슈의 phase 1(설계)은 스키마 초안
> 기준으로 병렬 진행 가능하나, phase 2 는 #171 머지 후에 연다.

Key takeaways for design:

- Single-binary CLI (`rsb`), config-driven, multi-repo aware.
- Strict single data source: `flows --json` per registered board repo. No
  direct parsing of `spawn.py`'s internal files (`runs/active.json`,
  `runs/ledger.jsonl`, session logs, etc.) — those are upstream implementation
  details, already summarized into the JSON contract.
- Five renderable sections, decision queue pinned at top as the actionable
  item.
- Default is single-shot; `--watch` adds periodic re-render.
- Scope is terminal/CLI rendering only; no HTML output in v1.

## 3. Prerequisite status: on-the-record#171

`gh api repos/tokenmaxxxer/on-the-record/issues/171` resolves to a **merged
PR** titled "issue-170: phase 1 — 26-role split catalog and rulebook skeleton
(proposal)" (state: MERGED). The `flows --json` schema document itself lives
at `tokenmaxxxer/on-the-record` `docs/specs/flows-schema.md` on `main`
(fetched via `gh api .../contents/docs/specs/flows-schema.md?ref=main`,
11445 bytes) and describes itself as "Frozen contract for issue #172, based
on the approved proposal `docs/issue-172/proposals/flows-json.md`". The
prerequisite ("on-the-record#171 merged") is satisfied — the schema exists,
is frozen, and is fetchable. It has been mirrored into this repo at
`docs/specs/flows-schema.md` for local reference (see note at the top of that
file for sync provenance).

## 4. `flows --json` schema summary (see `docs/specs/flows-schema.md` for the full text)

Top-level object: `schema_version` (bare int, bump only on breaking change),
`generated_at`, `repo`, `decision_queue[]`, `flows[]`, `sessions[]`,
`ledger[]`, `unattributed`, `hygiene`.

- **`decision_queue[]`** — one entry per open PR awaiting phase-1 or phase-2
  approval: `{issue, pr, phase, role, opened_at, age_hours, awaiting}`, where
  `awaiting` is `"approve-scope"` (phase 1) or `"approve-full"` (phase 2).
  This is explicitly the "what a human must act on right now" section — maps
  directly to issue's "결정 대기열(최상단)" requirement.
- **`flows[]`** — one entry per subject issue: `{issue, stage, stage_derived,
  roles[], prs[]}`. `stage` is one of five named stages
  (`proposal|approved|implementing|delivered|closed`) OR a raw unmapped
  `loop_state` string when `stage_derived: false` — renderer must treat
  `stage_derived: false` distinctly (e.g. render as "raw/unknown", not force
  into a color bucket).
- **`sessions[]`** — one entry per active roster row: `{role, issue,
  elapsed_min, pid, alive, verdict, last_activity}`. `last_activity` is
  `{ts, kind, detail}` or `null`. `verdict` is `"pending"` while alive, else
  looked up from ledger. Session data is sourced from the *orchestrator's own*
  `runs/` directory, not the board repo — i.e. this section is only
  meaningful when the dashboard is run against the same orchestrator checkout
  that ran the sessions (§5 of the schema doc, "Data provenance"). This is an
  important caveat for multi-repo config: sessions may be empty/absent for
  board repos not run from the local orchestrator.
- **`ledger[]`** — per-issue aggregate: `{issue, sessions, cost_usd_total,
  outcomes}`. Sibling `unattributed: {sessions, cost_usd_total}` for
  ledger entries with no derivable issue — must be rendered as its own
  bucket, not merged into a fake issue row.
- **`hygiene`** — single object: `closure_sweep[]` (verbatim
  `find_violations()` output) and `unapproved_open_prs[]` (`{issue, pr, role,
  opened_at}`).

Non-goals stated by the schema (binding on the consumer too): read-only, no
exit-code-as-alert semantics (hygiene violations are data, not exit codes),
no polling-cadence guidance (consumer's concern — i.e. `--watch`'s interval
is this CLI's own design decision, not dictated by the schema).

Versioning: `schema_version` is a bare integer, additive changes never bump
it, so the parser should be lenient about unknown/extra fields and strict
only about `schema_version` matching what it was built against (currently
`1`) — with a clear error message on mismatch, per issue requirement #2.

## 5. What upstream `flows --json` invocation looks like

The schema doc's §4 (GitHub API call-count contract) confirms `flows --json`
is invoked as a subcommand of `spawn.py` against a specific board repo
checkout (`-C <path>` flag implied by §5's "the target board repo passed via
`-C`"). This CLI does not need to reimplement any of that — it only needs to
shell out to (or otherwise invoke) `spawn.py flows --json -C <repo-path>` per
registered board repo and parse stdout. Multi-repo support in `rsb` means:
for each configured board repo, run this invocation once, parse it against
the shared schema, and merge/section the results into one screen (or fail
independently and mark that repo bad without blocking others — undecided,
see open questions in the proposal).

## 6. Open items carried into the proposal

- Exact multi-repo config file format/location.
- Exact CLI flag surface (`rsb`, subcommands vs. flags, `--watch` interval
  flag name/default).
- Layout algorithm for a single terminal screen showing 5 sections without
  requiring scrolling on a typical terminal (plus graceful degradation when
  content overflows).
- How `flows --json` is actually invoked (assume `spawn.py` is on `PATH` or a
  path is configured per repo — no `on-the-record` checkout exists in this
  environment to verify the exact invocation syntax beyond what the schema
  doc documents).
