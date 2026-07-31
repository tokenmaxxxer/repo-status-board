# Execution-observation record (issue #4)

Status: phase-2 verification record. Approved via issue #4 comment
`APPROVE issue-4/execution-observation` (role-handoff contract v3 s19),
against `docs/issue-4/proposals/execution-observation.md`. This role
observes and records only — no code under `src/`/`test/` was changed as
part of this work.

Environment: this checkout, `python3` 3.10.12, `pytest` 8.x
(`~/.local/lib/python3.10/site-packages`), `curl`, `node` v22.19.0
present but `node -e` invocations were denied by the sandbox's tool
policy on every attempt in this session, so JS logic verification below
is by code reading, not by executing `dashboard.js` under Node.
No headless/real browser is available in this sandbox — per the
proposal's stated fallback, all frontend-rendering verification is done
by (a) driving the shipped `webserver.make_handler`/`run_server` with
crafted `fetch_board_fn`s over real HTTP, and (b) reading
`dashboard.js`/`dashboard.css` against the JSON each server variant
actually returned.

## 1. pytest re-run

Command: `python3 -m pytest test/ -q` (run from repo root; no
`PYTHONPATH`/editable install needed — `test/rsb_tests` imports `rsb`
which resolves via the already-available environment).

Raw output:

```
/home/jwjung/.local/lib/python3.10/site-packages/pytest_asyncio/plugin.py:208: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))
.................................                                        [100%]
33 passed in 2.10s
```

Result: **33 passed, 0 failed** — independently reproduced, matches
implementation.md's claimed "33 passed" exactly.

## 2. Live `rsb serve` run

`rsb serve` itself was not invoked as a CLI subprocess (no `boards.toml`
exists in this checkout, per survey.md); instead, per the proposal's
"or a temporary script driving `webserver.make_handler`" fallback, four
throwaway scripts (deleted after use, written under
`/tmp/claude-*/.../scratchpad/`, never inside the repo tree) called
`rsb.webserver.run_server()` directly — the exact function `rsb serve`
calls — each with a different `fetch_board_fn`, bound to a distinct
local port (8531-8535). All requests were driven with real `curl`
against a real running `ThreadingHTTPServer`.

- `GET /` — `HTTP/1.0 200 OK`, `Content-type: text/html`, served
  `index.html` (`<title>rsb — status board</title>` confirmed in body).
- `GET /api/board.json` — `HTTP/1.0 200 OK`,
  `Content-Type: application/json`, well-formed JSON matching
  `render_json_model`'s shape in all five state variants below.

No headless/real browser was used or available — confirmed explicitly
here per the proposal's fallback clause.

## 3. State reproduction

Six states from `docs/specs/screen-spec.md` §2, one server variant per
API-observable state:

| State | Reproduced? | Matches spec? | Note |
|---|---|---|---|
| Page-level Loading (§2.1) | Code-read only, not reproduced live | Yes (by reading) | `dashboard.js load()` calls `renderSkeleton()` synchronously before `fetch()` resolves — confirmed by code reading. This is a pure client-side/DOM-timing state with no server-observable signal; no browser automation available to drive it live. |
| Page-empty (§2.2) | Reproduced live (server on :8532, all-empty payload) | Yes | API returned all-empty arrays; `isPageEmpty()` (all 7 arrays empty) evaluates true for this payload, so `dashboard.js` renders `<div class="empty-state">No activity to show for the configured repos.</div>` — matches spec text exactly. |
| Region-empty (§2.3, decision queue only) | Reproduced live (server on :8533, `decision_queue: []`, other regions populated) | Yes | `isPageEmpty()` is false (other arrays non-empty); `renderTable` for the decision queue falls to its `rows.length === 0` branch, emitting "Nothing awaiting decision" — matches §1.3/§2.3 exactly. Other regions render populated tables normally. |
| Page-level Error / total failure (§2.4) | Reproduced live (server on :8534, both configured repos error, no successful repo) | **No — mismatch, see finding F1 below** | Server returns HTTP 200 (per contract, matching `test_webserver.py`'s partial-failure-still-200 test) with `errors` populated and all data arrays empty. `dashboard.js`'s `load()` only calls `renderFullError()` on a non-2xx `res.ok` check or a `fetch` exception — neither occurs, since the server always returns 200. Client-side, `isPageEmpty(data)` does not inspect `errors` at all, so a total-repo-failure payload is indistinguishable from a genuinely-empty board: it renders "No activity to show for the configured repos." (§2.2's copy), not the "Couldn't load board status" + Retry `ErrorState` §2.4 specifies. The `errors`-count summary chip is the only signal shown (set before the `isPageEmpty` branch), and the dedicated Errors panel (§1.9) is also skipped because it lives inside the branch `isPageEmpty` short-circuits past. |
| Partial failure / banner (§2.5) | Reproduced live (server on :8535, one succeeding repo + one erroring repo) | Yes, with one styling finding (F2) | `PARTIAL_BANNER` populated with "1 of 2 repos failed to load — broken-repo: flows --json failed: boom" and a Retry link, exactly per §2.5's copy template; rest of the page renders the succeeding repo's data normally. Banner background/border/foreground colors match `status-warning` tokens. Retry-link foreground color does not match spec's fallback guarantee — see F2. |
| Detail-panel-empty (§2.6 / §1.6) | Inspected by code reading only, not reproduced live | Yes (by reading) | Requires simulating a row click then a stale re-fetch, which needs real DOM/JS execution (`attachRowClickHandlers` + `selectedIssue` state) unavailable without a browser. Code reading confirms `renderDetailPanel` returns the exact spec copy `"This issue no longer has board activity"` in `color-text-secondary` (`class="detail-panel text-secondary"`) when `findDetail()` returns no decision/flow/sessions/ledger for the selected `(issue, repo)` — matches spec. Not independently exercised end-to-end. |

## 4. H1 timing

Full page-load-to-render timing (fetch → JS execution → DOM paint) is
**not possible without a real browser**, which is unavailable in this
sandbox; only the `/api/board.json` HTTP round-trip is measured below,
which is a lower bound on/subset of the true H1 metric (median time
from web-view load to render ≤ 3s, hypotheses.md §3).

Command: 10 sequential `curl -s -o /dev/null -w "%{time_total}\n"
http://127.0.0.1:8531/api/board.json` against the worked-example-backed
server (§2 above), same host/no network hop.

Raw `time_total` values (seconds): `0.000158, 0.000115, 0.000159,
0.000261, 0.000350, 0.000228, 0.000316, 0.000252, 0.000219, 0.000328`

| Stat | Value (ms) |
|---|---|
| min | 0.115 |
| median | 0.240 |
| max | 0.350 |

Threshold: ≤ 3000ms (hypotheses.md §3). Result: **well within
threshold** (~10,000x headroom) — consistent with implementation.md's
manual "~4ms" claim (this is the API leg only, one to two orders of
magnitude faster still, since implementation.md's figure likely
included the `/` HTML fetch too). This confirms the server-side leg is
not the bottleneck; it says nothing about JS-render or real-network
latency, which this environment cannot measure.

## 5. Spec conformance pass

`dashboard.js`/`dashboard.css` read line by line against
`docs/specs/screen-spec.md` §1 (9 regions) and
`docs/specs/design-system.md` §2.4/§5 (age-bucket thresholds, status
color mapping, breakpoints).

| Item | Spec | Code | Match? |
|---|---|---|---|
| Age bucket thresholds | fresh <4h, aging 4–24h, stale ≥24h | `ageBucket()`: `>=24` stale, `>=4` aging, else fresh | Match |
| Age bucket → status color | neutral/warning/error | `ageBucketStatus()` maps exactly | Match |
| Alive/dead badge | alive→success, dead→neutral | `s.alive ? "status-success" : "status-neutral"` | Match |
| Hygiene/error markers | `status-error` | `.hygiene-list li`/`.error-list li` use `--color-status-error-border` | Match |
| Summary chip: decisions | neutral, or oldest-bucket color when N>0 | `selectSummary()` uses `ageBucketStatus(oldestBucket)` from `Math.max(age_hours)` | Match |
| Summary chip: flows | always neutral | hardcoded `"status-neutral"` | Match |
| Summary chip: sessions | success if N>0 else neutral | matches | Match |
| Summary chip: hygiene | error if N>0 else neutral | `closure_sweep.length + unapproved_open_prs.length` | Match |
| Summary chip: errors | error, hidden when N=0 | `hideWhenZero: true` filtered in render | Match |
| DataTable tokens | `space-table-cell-padding-y/x`, `border-default`, `surface-raised` | `table.data-table` CSS block | Match |
| RoleChip | `status-neutral` bg, **mono for the state text only** | `<span class="badge status-neutral mono">role:loop_state</span>` — mono applied to whole `role:state` string, not just the state segment | **Minor mismatch** |
| Region-empty copy per region | "Nothing awaiting decision" / "(none)" / "No hygiene issues" | Exact matches in `renderTable`/`renderHygiene` calls | Match |
| Page-empty copy | "No activity to show for the configured repos." | Exact match | Match |
| Full-page ErrorState (§2.4) | Heading "Couldn't load board status" + Retry, shown on total repo failure | **Never reached** for an all-repos-error payload — see F1 | **Mismatch (F1)** |
| Partial-failure banner copy/color | `status-warning`, "{M} of {N} repos failed..." | Exact copy match; warning bg/border/fg tokens correct | Match |
| Partial-failure retry link color | "falls back to warning's foreground if action-primary pairing fails contrast... both pass, no fallback needed" | `.partial-banner button.link { color: var(--color-action-primary-foreground) }` = white (`neutral-0`) text on `status-warning-background` (`#fffbeb`, near-white) — **not the warning-foreground token, and this pairing does not pass contrast** | **Mismatch (F2), see below** |
| Detail panel layout switch (§1.6, §5) | Side panel at/above `breakpoint-lg` (1200px); expandable row below | CSS only adds `position: sticky` above 1200px — no two-column/grid restructuring exists at any width; panel is always a single block appended after the last region | **Mismatch (F3)** |
| `breakpoint-md` (768px) behavior | Chips wrap 2 rows; detail panel forced to expandable-row | Chip wrap happens incidentally via `flex-wrap: wrap` (no 768px-specific rule); no `@media (max-width: 768px)` rule exists anywhere in `dashboard.css` | **Mismatch (F4, minor — no dedicated breakpoint-md rule, though chip wrap works anyway)** |
| `(raw)` stage suffix | `color-text-secondary` | `<span class="text-secondary">(raw)</span>` | Match |
| Errors panel (§1.9) | Only rendered when non-empty, `status-error` marker, "{repo}: {message}" | `renderErrors()` returns `""` when empty, else exact format | Match (but unreachable in total-failure case, tied to F1) |
| Accounting/hygiene spacing | `space-8` from hygiene panel above accounting | `.accounting-strip { margin-top: var(--space-8) }`, DOM order hygiene→accounting | Match |

**Total: 15 of 19 checked items match; 4 mismatches (2 significant — F1,
F2; 2 minor — F3/RoleChip-mono, F4).**

## 6. Findings (hand-off — not fixed here)

- **F1 (significant, correctness/spec conformance):** The full-page
  `ErrorState` (§2.4 — "Couldn't load board status" + Retry) specified
  for "total failure" is unreachable in the shipped code. Because
  `webserver.py` always returns HTTP 200 (by design, matching the
  partial-failure contract test), and `dashboard.js`'s `load()` only
  triggers `renderFullError()` on a non-2xx status or network exception,
  an all-repos-error payload instead falls through `isPageEmpty()`
  (which does not check `data.errors`) and renders the page-empty
  message, silently dropping the dedicated Errors panel and the
  "Couldn't load board status" messaging the spec requires for this
  case. Operator-facing impact: if every configured repo's `flows
  --json` fails, the operator sees "no activity" rather than "board
  status couldn't load" — a materially different (falsely reassuring)
  signal.
- **F2 (significant, accessibility/contrast):** The partial-failure
  banner's Retry link uses `color-action-primary-foreground` (white,
  `#ffffff`) as text color on `status-warning-background` (`#fffbeb`,
  a near-white tint) — a contrast ratio of roughly 1:1, i.e. the retry
  link text is effectively invisible on this background. Screen-spec.md
  §2.5 anticipated exactly this risk and stated a fallback
  ("`status-warning`'s foreground token") "if the action-primary pairing
  fails contrast," asserting no fallback would be needed in practice —
  but the shipped CSS did not implement any conditional fallback, and
  the primary pairing does fail badly here.
- **F3 (minor, spec conformance):** `DetailPanel`'s described
  side-panel-vs-expandable-row breakpoint switch (screen-spec.md §1.6,
  design-system.md §5) is not implemented as a layout change; the only
  breakpoint-driven CSS for `.detail-panel` is `position: sticky` above
  1200px. The panel is a single-column block at every width.
- **F4 (minor):** `breakpoint-md` (768px) is defined as a token in
  `design-system.md` §5 with described behavior (chip 2-row wrap,
  forced expandable-row detail panel) but no `@media (max-width: 768px)`
  rule exists in `dashboard.css`; the chip-wrap behavior happens to work
  anyway via unconditional `flex-wrap`, but the detail-panel
  forced-mode behavior does not exist at all.
- **RoleChip minor mismatch:** `font-family-mono` is applied to the
  entire `role:loop_state` chip text rather than only the
  `loop_state`/state segment as design-system.md's component table
  implies ("`font-family-mono` for the state text").

None of the above were fixed as part of this role — per contract, this
observation record hands them off as findings for a follow-up issue/PR,
not a defect to patch here.

## 7. Scope notes (unchanged from proposal §3)

- Auth/access-model and age-bucket-threshold-value decisions
  (hypotheses.md §5, screen-spec.md §5, design-system.md §7) remain
  open and out of scope for this record; not re-decided here.
- H1's full 14-day pilot-window metrics (off-terminal views/week,
  terminal-fallback rate) require real usage over time and are out of
  scope for this synchronous verification session; only the "≤3s
  median render" sub-metric (API leg only, see §4) was checked here.

## 8. Cleanup

All throwaway driver scripts (`serve_worked.py`, `serve_empty.py`,
`serve_region_empty.py`, `serve_total_failure.py`,
`serve_partial_failure.py`) and their logs/captured HTTP output lived
under a `/tmp/claude-*/.../scratchpad/` directory outside the repo tree
and were never added to git; background server processes were
terminated after use. No files besides this report were added to the
repo as part of this role's work.
