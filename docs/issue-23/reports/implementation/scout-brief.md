# Scout brief — issue #23 (plan-step rendering)

Mode: parallel (2 WebSearch calls, one turn). Stages used: 1 sweep + 1
judge point, no deepening round — saturation reached immediately (see
below). Aimed at the survey's gap: this repo has no existing UI for a
step-by-step execution plan to extend (survey §3), so the sweep targets
how comparable dashboards render ordered step lists with per-step status
and parallel grouping.

**Category must-bes** (from GitHub Actions job/step UI and CI/CD pipeline
dashboards): ordered list of steps rendered top-to-bottom in execution
order; each step carries a discrete status marker (done/running/pending)
rendered as an icon or badge, not prose; steps that can run concurrently
are visually grouped at the same position rather than interleaved into
the sequential list.

**Performance axes strong tools compete on**: (1) DAG/graph view for
complex branching dependency graphs (Buildkite's pipeline canvas) vs.
(2) flat ordered list for simple linear-with-occasional-parallel plans
(GitHub Actions' job list, default view). rsb's `plan` shape
(`{step:int, roles:[], done:bool}`, step-order integer, same-step roles
= parallel) is structurally the flat-list case, not the DAG case — no
cross-step dependency graph exists in the schema, only linear order +
same-line parallel.

**Adopt**: flat ordered step list, one row per `step`, done-state as a
checkmark/badge distinct from the role badges already used for
`flow.roles` (reuse existing `.badge`/`.status-*` tokens per survey §4);
same-step parallel roles rendered together on that step's row (matches
GitHub Actions' same-job parallel-step grouping).

**Skip**: DAG/canvas-style graph rendering (Buildkite-style) — the
schema carries no dependency-edge data to draw one, and it would be a
new visual language the rest of this dashboard's table/row-based UI
doesn't otherwise use.

**Segment fit**: rsb is an internal single-screen status dashboard, not
a pipeline-execution tool — it displays plan state, it doesn't drive
execution. Scout target was UI *pattern* (how to show ordered steps with
status), not the exemplars' execution/orchestration features, which are
out of scope by category mismatch.

**Gap line**: current state has zero step-list UI (full gap on the
must-be "ordered list with per-step status marker") but already has the
supporting primitives the pattern needs (badge/status tokens, an
established per-issue join in `renderDetailPanel`/`findDetail`) — so the
gap is narrow: assemble existing primitives into the new list shape, not
build new visual primitives.

**Judge point / saturation**: would another round change a build
decision? No — schema has no dependency graph, so the DAG-vs-list
question resolves immediately in favor of list; existing token set
already covers status marking. Stopped after stage 1.

Sources:
- https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions
- https://buildkite.com/resources/blog/visualize-your-ci-cd-pipeline-on-a-canvas/
