/* rsb web dashboard — screen-spec.md §1-§2 mapped to DOM. No build step. */

const REFRESH_BUTTON = document.getElementById("refresh-button");
const HEADER_META = document.getElementById("header-meta");
const SUMMARY_STRIP = document.getElementById("summary-strip");
const PARTIAL_BANNER = document.getElementById("partial-banner");
const MAIN = document.getElementById("main-content");
const DETAIL_SLOT = document.getElementById("detail-panel-slot");

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

/* ---- render fragments ---- */

function renderSkeleton() {
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
    <div class="error-state">
      <h1>Couldn't load board status</h1>
      <p>${escapeHtml(message)}</p>
      <button id="retry-button" class="refresh-button">Retry</button>
    </div>
  `;
  document.getElementById("retry-button").addEventListener("click", load);
}

function renderTable(headers, rows, emptyMessage) {
  if (rows.length === 0) {
    return `<div class="region-empty">${escapeHtml(emptyMessage)}</div>`;
  }
  const head = `<tr>${headers.map((h) => `<th>${escapeHtml(h)}</th>`).join("")}</tr>`;
  const body = rows.map((r) => `<tr data-issue="${r.issue}" data-repo="${escapeHtml(r.repo)}">${r.cells.join("")}</tr>`).join("");
  return `<table class="data-table"><thead>${head}</thead><tbody>${body}</tbody></table>`;
}

function decisionRows(decisions) {
  return decisions.map((d) => {
    const bucket = ageBucket(d.age_hours);
    return {
      issue: d.issue,
      repo: d.repo,
      cells: [
        `<td>${escapeHtml(d.repo)}</td>`,
        `<td class="mono">${d.issue}</td>`,
        `<td class="mono">${d.pr}</td>`,
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

function flowRows(flows) {
  return flows.map((f) => ({
    issue: f.issue,
    repo: f.repo,
    cells: [
      `<td class="mono">${f.issue}</td>`,
      `<td>${escapeHtml(f.stage)}${f.stage_derived ? "" : ' <span class="text-secondary">(raw)</span>'}</td>`,
      `<td>${planCellLabel(f.plan)}</td>`,
      `<td>${f.roles.map((r) => `<span class="badge status-neutral mono">${escapeHtml(r.role)}:${escapeHtml(r.loop_state)}</span>`).join(" ")}</td>`,
      `<td class="mono">${f.prs.join(",") || "-"}</td>`,
      `<td>${escapeHtml(f.repo)}</td>`,
    ],
  }));
}

function sessionRows(sessions) {
  return sessions.map((s) => ({
    issue: s.issue,
    repo: s.repo,
    cells: [
      `<td>${escapeHtml(s.role)}</td>`,
      `<td class="mono">${s.issue}</td>`,
      `<td class="mono">${s.elapsed_min.toFixed(1)}m</td>`,
      `<td class="mono">${s.pid}</td>`,
      `<td><span class="badge ${s.alive ? "status-success" : "status-neutral"}">${s.alive ? "alive" : "dead"}</span></td>`,
      `<td>${s.last_activity
        ? `<span class="mono">${escapeHtml(s.last_activity.ts)}</span> ${escapeHtml(s.last_activity.kind)}: ${escapeHtml(s.last_activity.detail)}`
        : '<span class="text-secondary">—</span>'}</td>`,
      `<td>${escapeHtml(s.repo)}</td>`,
    ],
  }));
}

function renderAccounting(ledger, unattributed) {
  const rows = ledger.map((le) => ({
    issue: le.issue,
    repo: le.repo,
    cells: [
      `<td class="mono">${le.issue}</td>`,
      `<td class="mono">${le.sessions}</td>`,
      `<td class="mono">$${le.cost_usd_total.toFixed(2)}</td>`,
      `<td>${Object.entries(le.outcomes).map(([k, v]) => `${escapeHtml(k)}:${v}`).join(" ")}</td>`,
      `<td>${escapeHtml(le.repo)}</td>`,
    ],
  }));
  const table = renderTable(["Issue", "Sessions", "Cost", "Outcomes", "Repo"], rows, "(none)");
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
    return `<div class="detail-panel text-secondary">This issue no longer has board activity</div>`;
  }
  const planData = buildPlanSteps(detail.flow, data.decisions, issue, repo);
  return `
    <div class="detail-panel">
      <div><strong>Issue ${issue}</strong> — ${escapeHtml(repo)}</div>
      ${detail.decision ? `<div>Decision: PR ${detail.decision.pr}, awaiting ${escapeHtml(detail.decision.awaiting)}</div>` : ""}
      ${detail.flow ? `<div>Stage: ${escapeHtml(detail.flow.stage)}</div>` : ""}
      ${renderPlanSection(planData)}
      ${detail.sessions.map((s) => `<div>Session: ${escapeHtml(s.role)} (${s.alive ? "alive" : "dead"})</div>`).join("")}
      ${detail.ledger ? `<div>Cost: $${detail.ledger.cost_usd_total.toFixed(2)} across ${detail.ledger.sessions} sessions</div>` : ""}
    </div>
  `;
}

function attachRowClickHandlers(data) {
  MAIN.querySelectorAll("tbody tr[data-issue]").forEach((row) => {
    row.addEventListener("click", () => {
      selectedIssue = { issue: Number(row.dataset.issue), repo: row.dataset.repo };
      renderData(data);
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

  const summary = selectSummary(data);
  SUMMARY_STRIP.innerHTML = Object.values(summary)
    .filter((s) => !(s.hideWhenZero && s.count === 0))
    .map((s) => `<span class="chip ${s.status}">${escapeHtml(s.label)}</span>`)
    .join("");

  const failedRepos = data.errors;
  if (failedRepos.length > 0 && Object.keys(data.generated_at_by_repo).length > 0) {
    const total = failedRepos.length + Object.keys(data.generated_at_by_repo).length;
    const detail = failedRepos.map((e) => `${escapeHtml(e.repo)}: ${escapeHtml(e.message)}`).join(", ");
    PARTIAL_BANNER.innerHTML = `
      <div class="partial-banner">
        ${failedRepos.length} of ${total} repos failed to load — ${detail}
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
    return;
  }

  MAIN.innerHTML = `
    <section class="region">
      <h2>Decision queue</h2>
      ${renderTable(["Repo", "Issue", "PR", "Phase", "Role", "Awaiting", "Age"], decisionRows(data.decisions), "Nothing awaiting decision")}
    </section>
    <section class="region">
      <h2>Flows</h2>
      ${renderTable(["Issue", "Stage", "Plan", "Roles", "PRs", "Repo"], flowRows(data.flows), "(none)")}
    </section>
    <section class="region">
      <h2>Sessions</h2>
      ${renderTable(["Role", "Issue", "Elapsed", "PID", "Alive", "Last activity", "Repo"], sessionRows(data.sessions), "(none)")}
    </section>
    ${renderErrors(data.errors)}
    <section class="region">
      <h2>Hygiene</h2>
      ${renderHygiene(data.closure_sweep, data.unapproved_open_prs)}
    </section>
    <section class="region accounting-strip">
      <h2>Accounting</h2>
      ${renderAccounting(data.ledger, data.unattributed)}
    </section>
  `;
  DETAIL_SLOT.innerHTML = selectedIssue ? renderDetailPanel(data, selectedIssue.issue, selectedIssue.repo) : "";
  attachRowClickHandlers(data);
}

async function load() {
  renderSkeleton();
  try {
    const res = await fetch("/api/board.json");
    if (!res.ok) {
      renderFullError(`server returned ${res.status}`);
      return;
    }
    const data = await res.json();
    renderData(data);
  } catch (err) {
    renderFullError(err.message || String(err));
  }
}

// Browser-only auto-init. Guarded so this file can be `require()`d under
// Node (issue-23's dashboard.js behavior tests, test/rsb_tests/test_model.py)
// without a real DOM/fetch — `window` is always defined in a browser and
// never defined under plain Node, so this never changes browser behavior.
if (typeof window !== "undefined") {
  REFRESH_BUTTON.addEventListener("click", load);
  load();
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { ageBucket, ageBucketStatus, selectSummary, isPageEmpty, buildPlanSteps };
}
