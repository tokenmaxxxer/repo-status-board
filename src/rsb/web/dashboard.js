/* rsb web dashboard — screen-spec.md §1-§2 mapped to DOM. No build step. */

const REFRESH_BUTTON = document.getElementById("refresh-button");
const HEADER_META = document.getElementById("header-meta");
const SUMMARY_STRIP = document.getElementById("summary-strip");
const PARTIAL_BANNER = document.getElementById("partial-banner");
const MAIN = document.getElementById("main-content");
const DETAIL_SLOT = document.getElementById("detail-panel-slot");
const REPO_FILTER = document.getElementById("repo-filter");

// Detail-panel layout switch — matches dashboard.css's
// `@media (min-width: 1200px)` rule (design-system.md's `breakpoint-lg`).
// At/above this width: DETAIL_SLOT renders as a sticky side panel. Below
// it, applySelectionLayout() inserts the same content as a `<tr>`
// immediately after the selected row instead (screen-spec.md §1.6).
const WIDE_LAYOUT_QUERY = "(min-width: 1200px)";

// Fetched board payload, promoted to module scope (was local to load())
// so the repo-filter `<select>`'s `change` handler can re-render a
// filtered view without a refetch.
let boardData = null;

/* ---- pure state-selection / formatting helpers (no DOM) ---- */

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function ageBucket(ageHours) {
  if (ageHours >= 24) return "stale";
  if (ageHours >= 4) return "aging";
  return "fresh";
}

function ageBucketStatus(bucket) {
  return { fresh: "status-neutral", aging: "status-warning", stale: "status-error" }[bucket];
}

// "In progress" policy for the flows summary chip (issue-23 requirement 4;
// wording corrected per 2차 교차 검토 finding #2). A flow counts as
// in-progress when its `stage` is one of the three known non-terminal
// stages, OR when `stage_derived` is `false` (an unmapped raw `loop_state`
// string — flows-schema.md §2.2). This is a policy choice, not a
// guaranteed-exact count: it can OVER-count if the upstream rulebook ever
// produces an unmapped raw `loop_state` for a flow that has actually
// already reached a terminal stage (delivered/closed) but has no mapping
// rule yet. The alternative — excluding stage_derived:false from the count
// — was rejected because it under-counts far more often in practice:
// unmapped states arise mid-flow (a new/renamed loop_state not yet given a
// rulebook mapping), not at closure, since the well-known terminal states
// are exactly the ones the rulebook already maps. See
// docs/issue-23/proposals/implementation.md "Rationale" for the original
// analysis; this comment corrects that document's verification-criteria
// phrasing ("정확히 셈" / counts exactly), which overclaimed precision this
// policy does not actually guarantee.
function isFlowInProgress(f) {
  return f.stage_derived === false || ["proposal", "approved", "implementing"].includes(f.stage);
}

function selectSummary(data) {
  const decisionCount = data.decisions.length;
  const oldestBucket = decisionCount > 0
    ? ageBucket(Math.max(...data.decisions.map((d) => d.age_hours)))
    : null;
  return {
    decisions: {
      label: `${decisionCount} awaiting decision`,
      status: decisionCount > 0 ? ageBucketStatus(oldestBucket) : "status-neutral",
    },
    flows: {
      label: `${data.flows.filter(isFlowInProgress).length} flows in progress`,
      status: "status-neutral",
    },
    sessions: {
      label: `${data.sessions.length} sessions active`,
      status: data.sessions.length > 0 ? "status-success" : "status-neutral",
    },
    hygiene: {
      label: `${data.closure_sweep.length + data.unapproved_open_prs.length} hygiene issues`,
      status: (data.closure_sweep.length + data.unapproved_open_prs.length) > 0 ? "status-error" : "status-neutral",
    },
    errors: { label: `${data.errors.length} repo errors`, status: "status-error", hideWhenZero: true, count: data.errors.length },
  };
}

function isPageEmpty(data) {
  return data.decisions.length === 0
    && data.flows.length === 0
    && data.sessions.length === 0
    && data.ledger.length === 0
    && data.unattributed.length === 0
    && data.closure_sweep.length === 0
    && data.unapproved_open_prs.length === 0;
}

// Client-side repo filter for the repo-filter `<select>` (issue #29
// requirement 2) — recomputes a repo-scoped view of an already-fetched
// payload with no refetch. Pure/DOM-free so it gets `node -e` coverage via
// the module.exports guard below, same convention as buildPlanSteps.
// `repo` falsy (e.g. the "All repos" option's value `""`) returns `data`
// unchanged; otherwise every per-issue section is filtered to `.repo ===
// repo` and `generated_at_by_repo` is narrowed to just that repo's key.
function filterByRepo(data, repo) {
  if (!repo) return data;
  return {
    ...data,
    decisions: data.decisions.filter((d) => d.repo === repo),
    flows: data.flows.filter((f) => f.repo === repo),
    sessions: data.sessions.filter((s) => s.repo === repo),
    ledger: data.ledger.filter((le) => le.repo === repo),
    unattributed: data.unattributed.filter((u) => u.repo === repo),
    closure_sweep: data.closure_sweep.filter((v) => v.repo === repo),
    unapproved_open_prs: data.unapproved_open_prs.filter((u) => u.repo === repo),
    errors: data.errors.filter((e) => e.repo === repo),
    generated_at_by_repo: Object.fromEntries(
      Object.entries(data.generated_at_by_repo).filter(([repoKey]) => repoKey === repo)
    ),
  };
}

// Repo-list source for populating the repo-filter `<select>`: the union of
// repos that succeeded (`generated_at_by_repo` keys) and repos that failed
// (`errors[].repo`) — i.e. every repo the board is configured for,
// regardless of load outcome.
function repoList(data) {
  const repos = new Set([
    ...Object.keys(data.generated_at_by_repo),
    ...data.errors.map((e) => e.repo),
  ]);
  return Array.from(repos).sort();
}

/* ---- render fragments ---- */

function renderSkeleton() {
  MAIN.setAttribute("aria-busy", "true");
  HEADER_META.textContent = "Loading…";
  SUMMARY_STRIP.innerHTML = ["status-neutral", "status-neutral", "status-neutral", "status-neutral"]
    .map(() => `<span class="chip skeleton" style="width:8em;"></span>`)
    .join("");
  PARTIAL_BANNER.innerHTML = "";
  DETAIL_SLOT.innerHTML = "";
  MAIN.innerHTML = ["Decision queue", "Flows", "Sessions", "Accounting", "Hygiene"]
    .map((title) => `
      <section class="region">
        <h2>${title}</h2>
        <div class="skeleton skeleton-row"></div>
        <div class="skeleton skeleton-row"></div>
        <div class="skeleton skeleton-row"></div>
      </section>
    `).join("");
}

function renderFullError(message) {
  HEADER_META.textContent = "";
  SUMMARY_STRIP.innerHTML = "";
  PARTIAL_BANNER.innerHTML = "";
  DETAIL_SLOT.innerHTML = "";
  MAIN.innerHTML = `
    <div class="error-state" role="alert">
      <h2>Couldn't load board status</h2>
      <p>The board data couldn't be loaded.</p>
      ${collapsibleDetailHtml("Details", message)}
      <button id="retry-button" class="refresh-button">Retry</button>
    </div>
  `;
  document.getElementById("retry-button").addEventListener("click", load);
  MAIN.setAttribute("aria-busy", "false");
}

function renderTable(headers, rows, emptyMessage, caption) {
  if (rows.length === 0) {
    return `<div class="region-empty">${escapeHtml(emptyMessage)}</div>`;
  }
  const head = `<tr>${headers.map((h) => `<th scope="col">${escapeHtml(h)}</th>`).join("")}</tr>`;
  // `data-issue`/`data-repo` used to live on this <tr> for the old
  // whole-row click handler (issue #36 removed that path in favor of
  // `.row-toggle`'s own `data-*` attributes) — not re-added here, the
  // row-toggle button inside `r.cells` is the only thing click-bound now.
  const body = rows.map((r) => `<tr>${r.cells.join("")}</tr>`).join("");
  const captionHtml = `<caption class="visually-hidden">${escapeHtml(caption)}</caption>`;
  // `.table-scroll` (dashboard.css) gives each table its own horizontal
  // scroll container independent of the page — one shared change point
  // covers all four dashboard tables (decisions/flows/sessions/ledger),
  // since they all route through this function.
  return `<div class="table-scroll"><table class="data-table">${captionHtml}<thead>${head}</thead><tbody>${body}</tbody></table></div>`;
}

// Issue-cell disclosure trigger (issue #23 execution-observation's
// click-only-row finding; issue #29 requirement 5; relocated to a
// leading icon-only button by issue #36 once the issue number itself
// became a GitHub link and could no longer double as the button's
// label) — a real <button> per WAI-ARIA APG's disclosure pattern, not a
// clickable <tr>. `sourceTable` identifies which of the four tables
// this button belongs to, so `isRowExpanded` only reports true for the
// row actually selected in that specific table, never every table
// showing the same (issue, repo).
function isRowExpanded(sourceTable, issue, repo) {
  return !!(
    selectedIssue
    && selectedIssue.sourceTable === sourceTable
    && selectedIssue.issue === issue
    && selectedIssue.repo === repo
  );
}

// GitHub deep-link helper (issue #34, rewritten by issue #36 to render
// the issue/PR *number itself* as the link text instead of a trailing ↗
// icon) — pure/DOM-free so it gets `node -e` coverage via the
// module.exports guard below, same convention as buildPlanSteps/
// filterByRepo. `ownerNameByRepo` (owner/name per repo short name, keyed
// the same way as `generated_at_by_repo`) is looked up per-record by
// callers; when a repo has no owner/name on record, `buildGithubUrl`
// returns `null` and `numberLinkHtml` falls back to plain `#<n>` text
// (AC5 — no broken link).
function buildGithubUrl(ownerName, kind, number) {
  if (!ownerName || typeof ownerName !== "string") return null;
  return `https://github.com/${ownerName}/${kind}/${number}`;
}

function numberLinkHtml(ownerName, kind, number) {
  const url = buildGithubUrl(ownerName, kind, number);
  if (url === null) return escapeHtml(`#${number}`);
  return `<a class="number-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(`#${number}`)}</a>`;
}

// Icon-only disclosure button, separate from and leading the `#<n>`
// link (never overlapping/nesting it) per scout-brief's must-be: a
// native <button>, leading position, decorative glyph
// (`aria-hidden="true"`) that flips with `aria-expanded`, accessible
// name carried by `aria-label` since the glyph no longer can. Fixed
// `aria-controls="detail-panel-slot"` — the only detail container this
// codebase actually renders (issue-36 survey §2; no per-table
// `detail-row-*` element is ever created).
function rowToggleButtonHtml(sourceTable, issue, repo, expanded) {
  return `<button type="button" class="row-toggle" aria-expanded="${expanded}" aria-controls="detail-panel-slot" aria-label="Toggle details for issue ${issue}" data-issue="${issue}" data-repo="${escapeHtml(repo)}" data-table="${sourceTable}"><span aria-hidden="true">${expanded ? "▾" : "▸"}</span></button>`;
}

function issueToggleCell(sourceTable, issue, repo, ownerName) {
  const expanded = isRowExpanded(sourceTable, issue, repo);
  return `<span class="issue-cell">${rowToggleButtonHtml(sourceTable, issue, repo, expanded)}${numberLinkHtml(ownerName, "issues", issue)}</span>`;
}

// PR-cell helper (issue #34 AC3, rewritten by issue #36) — shared by
// decisionRows' single-PR cell and flowRows' multi-PR cell. Empty/falsy
// `prNumbers` keeps the existing "-" fallback; each PR number renders as
// its own `#<n>` link (or plain text, AC5) — no disclosure control here,
// so the cell structure itself is otherwise unchanged.
function prCellHtml(ownerName, prNumbers) {
  if (!prNumbers || prNumbers.length === 0) return "-";
  return prNumbers
    .map((prNumber) => `<span class="mono">${numberLinkHtml(ownerName, "pull", prNumber)}</span>`)
    .join(", ");
}

function decisionRows(decisions, ownerNameByRepo) {
  return decisions.map((d) => {
    const bucket = ageBucket(d.age_hours);
    return {
      issue: d.issue,
      repo: d.repo,
      cells: [
        `<td>${escapeHtml(d.repo)}</td>`,
        `<td class="mono">${issueToggleCell("decisions", d.issue, d.repo, ownerNameByRepo[d.repo])}</td>`,
        `<td>${prCellHtml(ownerNameByRepo[d.repo], [d.pr])}</td>`,
        `<td>${d.phase}</td>`,
        `<td>${escapeHtml(d.role)}</td>`,
        `<td>${escapeHtml(d.awaiting)}</td>`,
        `<td>${d.age_hours.toFixed(1)}h <span class="badge ${ageBucketStatus(bucket)}">${bucket}</span></td>`,
      ],
    };
  });
}

// "Plan" table-cell summary: `plan === null` renders the same
// text-secondary placeholder other absent-value cells use elsewhere in
// this table; `plan.length === 0` renders a distinct "0 steps" label
// (never conflated with the null case); a non-empty plan renders a
// compact "done/total" badge. The full per-step, per-role breakdown lives
// in the detail panel (renderPlanSection) — this cell is a scan-friendly
// summary only, matching the rest of flowRows' one-badge-per-cell
// convention.
function planCellLabel(plan) {
  if (plan === null || plan === undefined) return `<span class="text-secondary">—</span>`;
  if (plan.length === 0) return `<span class="text-secondary">0 steps</span>`;
  const done = plan.filter((p) => p.done).length;
  const total = plan.length;
  const status = done === total ? "status-success" : "status-neutral";
  return `<span class="badge ${status} mono">${done}/${total} done</span>`;
}

function flowRows(flows, ownerNameByRepo) {
  return flows.map((f) => ({
    issue: f.issue,
    repo: f.repo,
    cells: [
      `<td>${escapeHtml(f.repo)}</td>`,
      `<td class="mono">${issueToggleCell("flows", f.issue, f.repo, ownerNameByRepo[f.repo])}</td>`,
      `<td>${escapeHtml(f.stage)}${f.stage_derived ? "" : ' <span class="text-secondary">(raw)</span>'}</td>`,
      `<td>${planCellLabel(f.plan)}</td>`,
      `<td>${f.roles.map((r) => `<span class="badge status-neutral mono">${escapeHtml(r.role)}:${escapeHtml(r.loop_state)}</span>`).join(" ")}</td>`,
      `<td>${prCellHtml(ownerNameByRepo[f.repo], f.prs)}</td>`,
    ],
  }));
}

function sessionRows(sessions, ownerNameByRepo) {
  return sessions.map((s) => ({
    issue: s.issue,
    repo: s.repo,
    cells: [
      `<td>${escapeHtml(s.repo)}</td>`,
      `<td>${escapeHtml(s.role)}</td>`,
      `<td class="mono">${issueToggleCell("sessions", s.issue, s.repo, ownerNameByRepo[s.repo])}</td>`,
      `<td class="mono">${s.elapsed_min.toFixed(1)}m</td>`,
      `<td class="mono">${s.pid}</td>`,
      `<td><span class="badge ${s.alive ? "status-success" : "status-neutral"}">${s.alive ? "alive" : "dead"}</span></td>`,
      `<td>${s.last_activity
        ? `<span class="mono">${escapeHtml(s.last_activity.ts)}</span> ${escapeHtml(s.last_activity.kind)}: ${escapeHtml(s.last_activity.detail)}`
        : '<span class="text-secondary">—</span>'}</td>`,
    ],
  }));
}

function renderAccounting(ledger, unattributed, ownerNameByRepo) {
  const rows = ledger.map((le) => ({
    issue: le.issue,
    repo: le.repo,
    cells: [
      `<td>${escapeHtml(le.repo)}</td>`,
      `<td class="mono">${issueToggleCell("ledger", le.issue, le.repo, ownerNameByRepo[le.repo])}</td>`,
      `<td class="mono">${le.sessions}</td>`,
      `<td class="mono">$${le.cost_usd_total.toFixed(2)}</td>`,
      `<td>${Object.entries(le.outcomes).map(([k, v]) => `<span class="badge status-neutral mono">${escapeHtml(k)}:${escapeHtml(v)}</span>`).join(" ")}</td>`,
    ],
  }));
  const table = renderTable(["Repo", "Issue", "Sessions", "Cost", "Outcomes"], rows, "(none)", "Accounting ledger");
  const unattributedLines = unattributed.map((u) =>
    `<div class="unattributed">(unattributed: ${u.sessions} sessions, $${u.cost_usd_total.toFixed(2)} — ${escapeHtml(u.repo)})</div>`
  ).join("");
  return `${table}${unattributedLines}`;
}

function renderHygiene(closureSweep, unapprovedPrs) {
  const items = [
    ...closureSweep.map((v) => `<li>[closure-sweep] issue ${v.raw.issue}: ${escapeHtml(v.raw.violation)} — ${escapeHtml(v.raw.detail || "")} — ${escapeHtml(v.repo)}</li>`),
    ...unapprovedPrs.map((u) => `<li>[unapproved-pr] issue ${u.issue} pr ${u.pr} (${escapeHtml(u.role)}, opened ${escapeHtml(u.opened_at)}) — ${escapeHtml(u.repo)}</li>`),
  ];
  if (items.length === 0) return `<div class="region-empty">No hygiene issues</div>`;
  return `<ul class="hygiene-list">${items.join("")}</ul>`;
}

function renderErrors(errors) {
  if (errors.length === 0) return "";
  return `
    <section class="region">
      <h2>Errors</h2>
      <ul class="error-list">
        ${errors.map((e) => `<li>${escapeHtml(e.repo)}: ${escapeHtml(e.message)}</li>`).join("")}
      </ul>
    </section>
  `;
}

// Pure (no-DOM) plan-step builder for the detail panel — kept separate
// from renderPlanSection() so it can be exercised directly (see
// test/rsb_tests/test_model.py) without a browser/DOM. Joins each step's
// roles against `flow.roles` (loop_state/verdict) and `decisions`
// (pending PRs), reusing the same per-issue join pattern findDetail()
// already established (issue-23 requirement 3 / on-the-record #189 D3:
// the join is this repo's responsibility, not the provider payload's).
//
// Return shape distinguishes `plan: null` from `plan: []` all the way
// through, per issue-23 requirement / 2차 교차 검토 finding #3c:
//   null            -- flow has no plan block, or no flow at all
//   { steps: [] }   -- plan header present, zero valid steps
//   { steps: [...] } -- non-empty plan, `steps` sorted by `step` ascending
//                      (finding #3a: display order is step-number order,
//                      not payload array order)
function buildPlanSteps(flow, decisions, issue, repo) {
  if (!flow || flow.plan === null || flow.plan === undefined) return null;
  const sorted = flow.plan.slice().sort((a, b) => a.step - b.step);
  return {
    steps: sorted.map((step) => ({
      step: step.step,
      done: step.done,
      roles: step.roles.map((roleName) => {
        const roleStatus = (flow.roles || []).find((r) => r.role === roleName) || null;
        // finding #3b: ALL matching pending PRs for this (issue, repo,
        // role), not just the first — a role can have more than one open
        // PR against the same subject.
        const pendingPrs = decisions.filter(
          (d) => d.issue === issue && d.repo === repo && d.role === roleName
        );
        // Neither roleStatus nor a pending PR is found for a plan-only
        // issue with no board record yet (issue body's plan-only-issue
        // requirement) — role name alone is shown in that case; this is
        // the intended, not an error, path.
        return { role: roleName, roleStatus, pendingPrs };
      }),
    })),
  };
}

function renderPlanSection(planData) {
  if (planData === null) return "";
  if (planData.steps.length === 0) {
    // finding #3c: explicit "0 steps" state, not a blank/omitted section.
    return `<div><strong>Plan</strong>: <span class="text-secondary">0 steps</span></div>`;
  }
  const stepLines = planData.steps.map((step) => {
    const roleParts = step.roles.map((r) => {
      const statusBadge = r.roleStatus
        ? ` <span class="badge status-neutral mono">${escapeHtml(r.roleStatus.loop_state)}/${escapeHtml(r.roleStatus.verdict)}</span>`
        : "";
      const prBadges = r.pendingPrs
        .map((d) => ` <span class="badge status-info mono">PR ${d.pr} (${escapeHtml(d.awaiting)})</span>`)
        .join("");
      return `<span class="mono">${escapeHtml(r.role)}</span>${statusBadge}${prBadges}`;
    }).join(" ‖ ");
    const doneBadge = `<span class="badge ${step.done ? "status-success" : "status-neutral"}">${step.done ? "done" : "pending"}</span>`;
    return `<div>step <span class="mono">${step.step}</span> ${doneBadge} — ${roleParts}</div>`;
  }).join("");
  return `<div><strong>Plan</strong></div>${stepLines}`;
}

let selectedIssue = null;

function findDetail(data, issue, repo) {
  return {
    decision: data.decisions.find((d) => d.issue === issue && d.repo === repo) || null,
    flow: data.flows.find((f) => f.issue === issue && f.repo === repo) || null,
    sessions: data.sessions.filter((s) => s.issue === issue && s.repo === repo),
    ledger: data.ledger.find((le) => le.issue === issue && le.repo === repo) || null,
  };
}

function renderDetailPanel(data, issue, repo) {
  if (issue == null) return "";
  const detail = findDetail(data, issue, repo);
  if (!detail.decision && !detail.flow && detail.sessions.length === 0 && !detail.ledger) {
    return `<div class="detail-panel text-secondary" id="detail-panel-heading" tabindex="-1">This issue no longer has board activity</div>`;
  }
  const planData = buildPlanSteps(detail.flow, data.decisions, issue, repo);
  return `
    <div class="detail-panel" role="region" aria-labelledby="detail-panel-heading">
      <h2 id="detail-panel-heading" tabindex="-1">Issue ${issue} — ${escapeHtml(repo)}</h2>
      ${detail.decision ? `<div>Decision: PR ${detail.decision.pr}, awaiting ${escapeHtml(detail.decision.awaiting)}</div>` : ""}
      ${detail.flow ? `<div>Stage: ${escapeHtml(detail.flow.stage)}</div>` : ""}
      ${renderPlanSection(planData)}
      ${detail.sessions.map((s) => `<div>Session: ${escapeHtml(s.role)} (${s.alive ? "alive" : "dead"})</div>`).join("")}
      ${detail.ledger ? `<div>Cost: $${detail.ledger.cost_usd_total.toFixed(2)} across ${detail.ledger.sessions} sessions</div>` : ""}
    </div>
  `;
}

// Narrow-screen (< breakpoint-lg) inline equivalent of the detail side
// panel — pure/DOM-free so it gets `node -e` coverage via the
// module.exports guard below. `contentHtml` is whatever
// `renderDetailPanel(...)` already produced; `colspan` spans every column
// of the row it's inserted after (P1-3).
function detailRowHtml(colspan, contentHtml) {
  return `<tr class="detail-row"><td colspan="${colspan}">${contentHtml}</td></tr>`;
}

// Summary-line + collapsed-`<details>` error-detail structure (P2-6) —
// pure/DOM-free so it gets `node -e` coverage via the module.exports guard
// below. Both `summaryLabel` and `detailText` are escaped: `detailText` in
// particular can be a raw provider/backend error string that may contain
// internal paths, so it stays behind the collapsed `<details>` rather than
// always-visible text.
function collapsibleDetailHtml(summaryLabel, detailText) {
  return `<details><summary>${escapeHtml(summaryLabel)}</summary><p>${escapeHtml(detailText)}</p></details>`;
}

// Selects where the detail panel's markup goes (P1-3) and marks the
// selected row for visual highlighting (P2-7). Wide layout (or the toggled
// row can't be found, e.g. it scrolled out of the current filtered view):
// renders into DETAIL_SLOT as before. Narrow layout: DETAIL_SLOT stays
// empty and the same renderDetailPanel(...) markup is inserted as a
// sibling `<tr>` immediately after the selected row, so there is exactly
// one render path/content source for both layouts (Rationale).
function applySelectionLayout(data) {
  MAIN.querySelectorAll(".selected-row").forEach((row) => row.classList.remove("selected-row"));

  if (!selectedIssue) {
    DETAIL_SLOT.innerHTML = "";
    return;
  }

  let selectedRow = null;
  let matchCount = 0;
  MAIN.querySelectorAll(".row-toggle").forEach((button) => {
    if (
      button.dataset.table === selectedIssue.sourceTable
      && Number(button.dataset.issue) === selectedIssue.issue
      && button.dataset.repo === selectedIssue.repo
    ) {
      matchCount += 1;
      selectedRow = button.closest("tr");
    }
  });
  // `(sourceTable, issue, repo)` isn't always a unique row key — the
  // Sessions table can hold more than one row per (issue, repo) (distinct
  // roles/pids), so more than one button can match here. Picking either
  // one to highlight/insert-into would be a guess that can land on a row
  // the user didn't click; treat an ambiguous match the same as "row not
  // found" below (safe DETAIL_SLOT fallback, no highlight) rather than
  // guess wrong.
  if (matchCount !== 1) {
    selectedRow = null;
  }
  if (selectedRow) {
    selectedRow.classList.add("selected-row");
  }

  const contentHtml = renderDetailPanel(data, selectedIssue.issue, selectedIssue.repo);
  if (!selectedRow || window.matchMedia(WIDE_LAYOUT_QUERY).matches) {
    DETAIL_SLOT.innerHTML = contentHtml;
  } else {
    DETAIL_SLOT.innerHTML = "";
    selectedRow.insertAdjacentHTML("afterend", detailRowHtml(selectedRow.children.length, contentHtml));
  }
}

// Repopulates the repo-filter `<select>`'s <option>s from the current
// board payload (issue #29 requirement 2 — this was previously never
// called, leaving the select stuck at just "All repos"). Preserves the
// previously-selected repo if it's still present in the new list;
// falls back to the "All repos" (`""`) option if the selected repo
// disappeared (e.g. it stopped erroring and stopped appearing, or was
// removed from config).
function updateRepoFilterOptions(data) {
  const previousValue = REPO_FILTER.value;
  const repos = repoList(data);
  REPO_FILTER.innerHTML = [`<option value="">All repos</option>`]
    .concat(repos.map((r) => `<option value="${escapeHtml(r)}">${escapeHtml(r)}</option>`))
    .join("");
  REPO_FILTER.value = repos.includes(previousValue) ? previousValue : "";
}

// Binds only to `.row-toggle` buttons (issue #36) — no longer the whole
// `tr[data-issue]` row, so an empty-cell click never opens the detail
// panel (AC3). Reads the button's own `data-issue`/`data-repo`/
// `data-table`; activating the already-expanded button closes it,
// activating any other button switches the selection.
function attachRowToggleHandlers(data) {
  MAIN.querySelectorAll(".row-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const issue = Number(button.dataset.issue);
      const repo = button.dataset.repo;
      const sourceTable = button.dataset.table;
      const wasExpanded = isRowExpanded(sourceTable, issue, repo);
      selectedIssue = wasExpanded ? null : { issue, repo, sourceTable };
      renderData(data);
      // P1-4: move focus to where the state actually changed instead of
      // leaving it on a (possibly re-created) button with no visible
      // context — closing returns focus to the row's own toggle button,
      // opening moves it onto the newly-rendered detail panel's heading.
      if (wasExpanded) {
        const reopenedButton = Array.from(MAIN.querySelectorAll(".row-toggle")).find(
          (b) => b.dataset.table === sourceTable && Number(b.dataset.issue) === issue && b.dataset.repo === repo
        );
        if (reopenedButton) reopenedButton.focus();
      } else {
        const heading = document.getElementById("detail-panel-heading");
        if (heading) heading.focus();
      }
    });
  });
}

function renderData(data) {
  const succeededRepoCount = Object.keys(data.generated_at_by_repo).length;
  if (data.errors.length > 0 && succeededRepoCount === 0) {
    renderFullError(data.errors.map((e) => `${e.repo}: ${e.message}`).join("; "));
    return;
  }

  const repoCount = Object.keys(data.generated_at_by_repo).length + data.errors.length;
  HEADER_META.textContent = `as of ${data.generated_at} — ${repoCount} repos, ${data.errors.length} errors`;

  // owner/name per repo short name (issue #34) — falsy-safe extraction
  // mirrors this file's existing defensive style (e.g. filterByRepo's
  // handling of missing keys); absent on older payloads simply yields no
  // external links (AC5), not an error.
  const ownerNameByRepo = data.owner_name_by_repo || {};

  const summary = selectSummary(data);
  SUMMARY_STRIP.innerHTML = Object.values(summary)
    .filter((s) => !(s.hideWhenZero && s.count === 0))
    .map((s) => `<span class="chip ${s.status}">${escapeHtml(s.label)}</span>`)
    .join("");

  const failedRepos = data.errors;
  if (failedRepos.length > 0 && Object.keys(data.generated_at_by_repo).length > 0) {
    const total = failedRepos.length + Object.keys(data.generated_at_by_repo).length;
    const detail = failedRepos.map((e) => `${e.repo}: ${e.message}`).join(", ");
    PARTIAL_BANNER.innerHTML = `
      <div class="partial-banner">
        ${failedRepos.length} of ${total} repos failed to load — ${collapsibleDetailHtml("Details", detail)}
        <button class="link" id="partial-retry">Retry</button>
      </div>
    `;
    document.getElementById("partial-retry").addEventListener("click", load);
  } else {
    PARTIAL_BANNER.innerHTML = "";
  }

  if (isPageEmpty(data)) {
    MAIN.innerHTML = `<div class="empty-state">No activity to show for the configured repos.</div>`;
    DETAIL_SLOT.innerHTML = "";
    MAIN.setAttribute("aria-busy", "false");
    return;
  }

  MAIN.innerHTML = `
    <section class="region">
      <h2>Decision queue</h2>
      ${renderTable(["Repo", "Issue", "PR", "Phase", "Role", "Awaiting", "Age"], decisionRows(data.decisions, ownerNameByRepo), "Nothing awaiting decision", "Decision queue")}
    </section>
    <section class="region">
      <h2>Flows</h2>
      ${renderTable(["Repo", "Issue", "Stage", "Plan", "Roles", "PRs"], flowRows(data.flows, ownerNameByRepo), "(none)", "Flows")}
    </section>
    <section class="region">
      <h2>Sessions</h2>
      ${renderTable(["Repo", "Role", "Issue", "Elapsed", "PID", "Alive", "Last activity"], sessionRows(data.sessions, ownerNameByRepo), "(none)", "Sessions")}
    </section>
    ${renderErrors(data.errors)}
    <section class="region">
      <h2>Hygiene</h2>
      ${renderHygiene(data.closure_sweep, data.unapproved_open_prs)}
    </section>
    <section class="region accounting-strip">
      <h2>Accounting</h2>
      ${renderAccounting(data.ledger, data.unattributed, ownerNameByRepo)}
    </section>
  `;
  applySelectionLayout(data);
  attachRowToggleHandlers(data);
  MAIN.setAttribute("aria-busy", "false");
}

async function load() {
  REFRESH_BUTTON.disabled = true;
  renderSkeleton();
  try {
    const res = await fetch("api/board.json");
    if (!res.ok) {
      renderFullError(`server returned ${res.status}`);
      return;
    }
    const data = await res.json();
    boardData = data;
    updateRepoFilterOptions(boardData);
    renderData(filterByRepo(boardData, REPO_FILTER.value));
  } catch (err) {
    renderFullError(err.message || String(err));
  } finally {
    REFRESH_BUTTON.disabled = false;
  }
}

// Browser-only auto-init. Guarded so this file can be `require()`d under
// Node (issue-23's dashboard.js behavior tests, test/rsb_tests/test_model.py)
// without a real DOM/fetch — `window` is always defined in a browser and
// never defined under plain Node, so this never changes browser behavior.
if (typeof window !== "undefined") {
  REFRESH_BUTTON.addEventListener("click", load);
  REPO_FILTER.addEventListener("change", () => {
    selectedIssue = null;
    renderData(filterByRepo(boardData, REPO_FILTER.value));
  });
  load();
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { ageBucket, ageBucketStatus, selectSummary, isPageEmpty, buildPlanSteps, filterByRepo, buildGithubUrl, numberLinkHtml, detailRowHtml, collapsibleDetailHtml };
}
