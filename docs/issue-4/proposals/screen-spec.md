# Screen/flow spec — web dashboard pilot (issue #4, interaction-design)

Status: phase-1 proposal. Scope: interaction-design role only — this is
the screen/flow spec handed off from the approved
`docs/issue-4/proposals/hypotheses.md`. No visual/token design (colors,
spacing scale, typography) — that is ux-engineering's write surface per
the issue's expected chain (this repo is token-less; the first
design-system proposal is ux-engineering's job, not this one). No code.

Grounding: every field named below is one already produced by
`render_json_model` (`src/rsb/render.py`) from a `BoardModel`
(`src/rsb/model.py`). No new backend fields are invented here.

## 1. Single-screen layout

One route, one screen, read-only (no write actions — matches hypotheses.md
H2's "glance" framing; the CLI itself has no mutation commands to expose).
Regions, top to bottom:

### 1.1 Header

- **Populated by:** `generated_at` (render timestamp), plus a derived
  repo/error count identical to the CLI header
  (`repo_count = len(generated_at_by_repo) + len(errors)`, `error_count =
  len(errors)`).
- **Content:** dashboard title, "as of {generated_at}", "{N} repos,
  {M} errors" chip. A manual refresh control (button) lives here — no
  auto-poll interval is specified in this phase (H2's day-14 metrics
  measure single-glance sufficiency, not polling behavior; polling
  cadence is left as an implementation/ux-engineering decision).
- Structural — no hypothesis, but it is where the "as of" staleness cue
  lives, which matters for trust in the glance.

### 1.2 Summary strip

- **Populated by:** aggregate counts, computed client-side from the same
  payload — count of `decisions`, count of `flows` (or count of flows
  whose roles contain a non-terminal `loop_state`, if that distinction is
  cheap — otherwise total flow count is an acceptable v1), count of
  `sessions` where `alive == true`, count of `closure_sweep` +
  `unapproved_open_prs` combined as one "hygiene issues" number, and
  total `errors` count.
- **Content:** a row of glance chips/badges: "N awaiting decision", "N
  flows in progress", "N sessions active", "N hygiene issues", "N repo
  errors" (this last one only rendered when > 0). This is the single
  region a returning operator should be able to read in under a second
  and answer "does anything need me."
- This is the primary answer surface for H2 — see traceability table.

### 1.3 Decision queue (primary table, first below the summary strip)

- **Populated by:** `decisions[]` — issue, pr, phase, role, age_hours,
  awaiting, repo. Already sorted oldest-first by the model
  (`age_hours` descending).
- **Content:** a table, one row per decision, columns: Repo, Issue, PR,
  Phase, Role, Awaiting, Age. Age is rendered with a visual bucket (e.g.
  fresh / aging / stale bands) rather than only a raw "12.4h" string —
  this is the concrete element H3 (deferred, but not blocked) is
  designed around; bucket thresholds themselves are not fixed in this
  phase.
- Row click opens the **detail panel** (§1.6) scoped to that
  repo+issue.

### 1.4 Flows table

- **Populated by:** `flows[]` — issue, stage (+ stage_derived), roles
  (role/loop_state/verdict list), prs, repo.
- **Content:** table, one row per flow: Repo, Issue, Stage (marked
  "(raw)" when `stage_derived` is false, same convention as
  `render_text`), Roles (compact `role:loop_state` chips), PRs (linked
  issue/PR numbers), matching the CLI's existing `_fmt_roles`/`_fmt_prs`
  formatting intent.
- Row click opens the detail panel scoped to that repo+issue.

### 1.5 Sessions table

- **Populated by:** `sessions[]` — role, issue, elapsed_min, pid, alive,
  verdict, last_activity (ts/kind/detail or null).
- **Content:** table: Repo, Issue, Role, Elapsed, Alive (yes/no badge),
  Verdict, Last activity (formatted `HH:MM:SS kind: detail`, or an
  em-dash when null, per `_fmt_last_activity`/`_fmt_prs` conventions).

### 1.6 Detail panel (side panel or expandable row — layout choice
deferred to ux-engineering; behavior specified here)

- **Populated by:** filtering the already-loaded decisions/flows/
  sessions/ledger arrays down to the selected repo+issue — no new
  network call, since the whole `BoardModel` is already client-side.
- **Content:** for the selected issue: its decision-queue row (if any),
  its flow row (roles/verdicts), its session rows, and its ledger entry
  (`sessions`, `cost_usd_total`, `outcomes`) if present.
- Structural convenience region — supports H2 indirectly (keeps the
  operator from needing the terminal to see "everything about issue
  N" in one place) but is not itself directly measured by a
  pre-registered metric.

### 1.7 Accounting strip (bottom, lower priority than decision/flows/
sessions per the glance-first ordering)

- **Populated by:** `ledger[]` (issue, sessions, cost_usd_total,
  outcomes) and `unattributed[]` (repo-level sessions, cost_usd_total).
- **Content:** compact table or per-repo summary line: Issue, Sessions,
  Cost (USD), Outcomes (key:value chips), Repo; plus an "unattributed:
  N sessions, $X — repo" line per repo that has one, matching
  `render_text`'s existing footer convention.

### 1.8 Hygiene panel

- **Populated by:** `closure_sweep[]` (issue, violation, detail, repo)
  and `unapproved_open_prs[]` (issue, pr, role, opened_at, repo).
- **Content:** a flat list, one line per violation: `[closure-sweep]
  issue N: violation — detail — repo` or `[unapproved-pr] issue N pr M
  (role, opened at ts) — repo`, same content as `render_text`'s HYGIENE
  section. Counted into the summary strip's "hygiene issues" chip.

### 1.9 Errors panel

- **Populated by:** `errors[]` — repo, message.
- **Content:** only rendered when non-empty; one line per repo error:
  "{repo}: {message}". See §2 for how this interacts with the
  Error page-state.

## 2. States

### 2.1 Page-level Loading

- **Trigger:** initial load, or manual refresh, before the first
  response returns.
- **Renders:** skeleton placeholders in the header (date), summary strip
  (grey chip outlines), and each table region (a few grey placeholder
  rows) — per §4 scout assumption, independent per-region skeletons
  rather than one full-page spinner, since the backend already fetches
  per-repo and can partially resolve.
- **Copy:** header shows "Loading…" in place of "as of {timestamp}".
  No user action available except an implicit cancel-by-navigation;
  no retry control needed since there is nothing to retry yet.

### 2.2 Page-level Empty

- **Trigger:** load succeeds, zero repos configured, or all configured
  repos returned but every array (`decisions`, `flows`, `sessions`,
  `ledger`, `closure_sweep`, `unapproved_open_prs`) is empty and
  `errors` is also empty (genuinely nothing to show, not a failure).
- **Renders:** summary strip shows all-zero chips (not hidden — a
  visible "0 awaiting, 0 in progress, 0 active, 0 issues" is itself the
  glance answer "nothing needs you"). Below it, a single inline
  empty-state message replaces the tables: "No activity to show for the
  configured repos." No CTA needed (there is no "add data" action this
  screen owns); this state is a valid, reassuring answer, not a dead end.

### 2.3 Region-level Empty

- **Trigger:** the overall load succeeded and at least one region has
  data, but a specific table's array is empty (e.g. no open decisions
  while flows/sessions have rows).
- **Renders:** that table's body is replaced with a single centered row/
  line, matching the CLI's existing `_table` "(none)" convention: e.g.
  "Nothing awaiting decision" for the decision queue, "(none)" for
  flows/sessions/accounting, "No hygiene issues" for hygiene. This is
  deliberately low-emphasis (plain text, not an illustration) since it
  is the common/expected case for a healthy board, not a genuine gap.

### 2.4 Page-level Error (total failure)

- **Trigger:** the fetch to the backend/API itself fails (network error,
  5xx, or — mapped from the CLI's own semantics — *every* configured
  repo is in `errors`, i.e. `_run_once`'s `all_failed` condition).
- **Renders:** full-page error state replacing the summary strip and all
  table regions: an icon/heading ("Couldn't load board status"), the
  underlying message if available (repo error messages, joined), and a
  primary **Retry** button that re-triggers the load (returns to
  Loading state). No stale content is shown underneath — full failure
  means nothing trustworthy to display, consistent with the scout
  assumption of full-page error for total failure vs. banner for
  partial.

### 2.5 Partial failure (banner, not page error)

- **Trigger:** `errors[]` is non-empty but not every repo failed (some
  repos returned data).
- **Renders:** a dismissible-but-persistent banner directly under the
  header: "{M} of {N} repos failed to load — {repo}: {message}(, …)".
  The rest of the screen (summary strip, tables) renders normally using
  whatever repos *did* succeed. A **Retry** action on the banner
  re-fetches only the failed repos if the backend supports partial
  refetch, otherwise triggers a full reload — implementation detail,
  not fixed here.

### 2.6 Detail panel states

- **Loading:** not applicable — detail panel has no independent fetch
  (§1.6), so it cannot be in a loading state once the page has loaded.
- **Empty:** if a row is clicked but, by the time of render, that
  issue no longer has any matching decision/flow/session/ledger entry
  (stale selection after a refresh), show "This issue no longer has
  board activity" inside the panel rather than closing it silently.

## 3. Traceability table

| UI element / region | Traces to | Metric/purpose |
|---|---|---|
| Summary strip | H2 (glance sufficiency) | Primary surface for "does anything need me" answered without a terminal switch — target: ≥80% of checks resolved here (median load ≤3s per hypotheses.md §3) |
| Decision queue table + age buckets | H2, and lays groundwork for H3 (attention signal) | H2: queue visibility avoids terminal fallback. H3 (deferred): age bucketing is the exact mechanism hypothesized to reduce missed/late approvals |
| Flows table | H2 | Part of the single-screen glance view whose sufficiency H2 measures |
| Sessions table | H2 | Same — "is anything running / stuck" is part of "does anything need me" |
| Detail panel | H2 (supporting) | Reduces terminal-fallback need for "tell me more about issue N" without a second screen/route |
| Accounting strip | Structural / no hypothesis | Cost/ledger data exists in the CLI payload; included for parity, not measured by any pre-registered metric in hypotheses.md |
| Hygiene panel | Structural / no hypothesis | Surfaces existing CLI hygiene data; no hypothesis in hypotheses.md targets hygiene specifically |
| Errors panel / Error state / partial-failure banner | H2 (support), and implicitly H1 | A dashboard that silently shows stale/wrong data on partial failure would itself force a terminal check — undermines H2 if mishandled; also indirectly supports H1 (off-terminal use is only real demand if the view is trustworthy when things go wrong) |
| Header ("as of" timestamp, manual refresh) | Structural / no hypothesis, but supports H2's "≤3s to render" metric by making load time and staleness visible | timing observability |
| Off-terminal view timestamp instrumentation (not a UI element, a logging hand-off) | H1, H2 | Every view load timestamped per hypotheses.md §3 — implementation-phase requirement, noted here so it isn't lost between roles |

Every hypothesis (H1, H2, H3) traces to at least one row above. Every
major UI element has a listed reason (hypothesis or "structural/no
hypothesis").

## 4. Basic interaction flow

1. **Load:** operator opens the dashboard URL. Page shows per-region
   Loading skeletons (§2.1).
2. **Render:** data arrives (partially or fully) and the page renders
   header, summary strip, and all table regions per §1. If some/all
   repos failed, the appropriate Error or partial-failure state
   (§2.4/§2.5) renders instead of/alongside normal content.
3. **View summary:** operator reads the summary strip first — this is
   the glance check the hypotheses target. If all chips read zero/clear,
   the flow ends here (H2 success case: no terminal fallback needed).
4. **Scan tables:** if the summary strip indicates something is
   outstanding, operator scans the decision queue (oldest/most-aged
   first, already sorted) and flows/sessions tables for the specific
   item.
5. **Drill in:** operator clicks a decision/flow/session row for the
   issue in question, opening the detail panel (§1.6) with everything
   known about that repo+issue assembled from already-loaded data (no
   extra round trip).
6. **Resolve or leave:** operator either takes the needed action outside
   this screen (e.g. reviews the PR on GitHub — this screen has no write
   actions) or, having confirmed nothing needs them, closes the tab.
   Either way, per H2, they should not need to return to the terminal's
   `rsb` CLI to get information this screen already showed them.
7. **Refresh (optional):** operator manually refreshes (header control)
   on a later glance; flow returns to step 1.

## 5. Open items explicitly deferred (not decided here)

- Visual design tokens, spacing, color, typography — ux-engineering.
- Auth/access model for exposing this data over the web — flagged as a
  hand-off in hypotheses.md §5, still unresolved; this spec assumes the
  data is reachable but does not specify how access is gated.
- Auto-refresh/poll interval, if any — left to implementation.
- Age-bucket thresholds for the decision queue (§1.3) — a concrete
  numeric threshold is an implementation/ux-engineering decision, not
  fixed here.
