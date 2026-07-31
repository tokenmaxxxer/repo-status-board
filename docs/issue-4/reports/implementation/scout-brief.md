# Scout brief — implementation stack (issue #4)

Angle run: single web-search agent (stack comparison), 1 stage — the only
open build decision left by design-system.md/screen-spec.md is the
frontend implementation stack; everything else (tokens, layout, states)
is frozen. Batched-sequential fallback not needed; single-angle question,
parallel fan-out would have been overkill for one decision.

Gap line: screen-spec.md and design-system.md fully specify layout,
tokens, and states but explicitly leave "implementation (`src/`)" out of
scope — the stack choice is this role's own open decision.

Must-bes (from comparable no-build internal dashboards): static-file
servable, zero bundler, fetch() + DOM render, state-switch render
function (loading/empty/error/data) rather than per-state templates.

Adopt: plain HTML/CSS/vanilla JS, `fetch()` against a JSON endpoint,
`setInterval` polling loop, single render function keyed on payload
presence/absence/error.

Skip: htmx (targets server-rendered HTML fragment endpoints; our source
is a CLI's JSON stdout, not a templating backend — no benefit) and
React/Vite (build tooling unjustified for one route, one operator,
read-only, per screen-spec.md's single-screen scope).

Segment fit: matches — this is exactly the "few components, single page,
internal tool" case vanilla JS sources recommend over a framework.

Sources:
- https://dev.to/arkhan/why-vanilla-javascript-is-making-a-comeback-in-2025-4939
- https://getconvertor.com/building-lightweight-tools-without-frameworks-vanilla-js-for-everyday-tasks/
- https://medium.com/@michaelpreston515/how-i-built-a-real-time-dashboard-from-scratch-using-vanilla-javascript-no-frameworks-f93f3dce98a9
- https://hamy.xyz/blog/2024-07_htmx-polling-example
- https://medium.com/codex/building-real-time-dashboards-with-fastapi-and-htmx-01ea458673cb
