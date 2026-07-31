# Scout brief — issue #4 (web dashboard pilot)

Mode: parallel fan-out, 2 angles in one batch (Agent tool), 1 sweep stage,
no deepening round — findings converged across both angles (bucketing +
threshold-based attention, plus adoption/kill signals), so stopped at
judge point 1 (further rounds unlikely to change build decisions). Total
elapsed ~1min.

## Angle 1 — multi-repo/CI status & PR-queue dashboards (Graphite, actions/stale, PR-radar)
- Must-be: bucket into "needs decision" vs "waiting on others" rather than
  one flat list — matches how a queue is actually scanned.
- Must-be: staleness threshold is a tunable knob (actions/stale default
  60d), not hardcoded — but signaled via *visual de-emphasis* (dim/gray),
  not hard alerts, to keep cognitive load low for a glance-and-return use.
- Performance axis: time-to-glance (can the operator tell "anything need
  me?" in a few seconds) beats completeness of data shown.

## Angle 2 — internal ops-dashboard adoption/kill research
- Must-be: one accountable owner + narrow audience correlates with real
  uptake; unowned "metrics for everyone" dashboards go unopened.
- Must-be: load/render speed matters directly — 15-30s loads cause
  abandonment before value is ever seen.
- Kill signal in the wild: weekly-active-viewer floor (roughly ≥1
  view/week by the intended viewer) is a common pre-registered retirement
  threshold; below it, the KPI/dashboard is retired rather than left to
  rot ("KPI graveyard").

## Gap line
`rsb`/flows-schema already has the *data* for bucketing (decision_queue
`awaiting`/`age_hours`) and for time-to-glance framing (single-screen
render already exists in CLI form). What's missing, per the survey: (1)
no staleness/attention threshold applied anywhere yet, (2) no
pre-registered success/kill rule exists for the web delivery itself — this
is the gap this issue's proposal must fill.

## Adopt / skip
- Adopt: single-viewer (solo operator), glance-time framing; a simple
  age-threshold-based dim/highlight cue on `decision_queue` items, sized
  to this repo's own approval-latency norms rather than an arbitrary SLA.
- Skip: SLA/p90 review-time analytics, multi-tenant/audience accounting —
  built for team scale, not proportionate to one operator's fleet.

Sources:
- https://graphite.com/guides/github-pr-dashboard
- https://github.com/withgraphite/docs/blob/main/guides/graphite-dashboard/using-the-review-queue.md
- https://github.com/actions/stale
- https://www.deployhq.com/blog/pr-radar-vs-github-notifications-vs-email-track-pull-requests
- https://medium.com/@bhumikaavula90/stop-building-dashboards-nobody-uses-why-most-analytics-deliverables-fail-and-how-to-design-for-b5d751a36ad3
- https://www.clicdata.com/blog/dashboard-adoption-plan/
- https://www.sigmacomputing.com/blog/kpi-graveyard-useless-metrics
