# Scout brief — issue #27 (Actions cron + Pages deployment)

Mode: parallel, 1 sweep round, 3 angles (WebSearch), no deepening —
GitHub's own official pattern for Actions→Pages is well-established and
directly on-point, so a second round would not change any build
decision. Aimed at the survey's gap: this repo has no `.github/`
workflow at all to extend (survey §9), so the sweep targets the
canonical shape for scheduled static-site generation + Pages publish.

**Category must-bes** (from GitHub's own Actions-to-Pages docs): a
build job that assembles a static artifact directory and hands it to
`actions/upload-pages-artifact`, followed by a separate `deploy` job
gated by `needs:` that runs `actions/deploy-pages`, itself gated by a
`github-pages` `environment:` block; `schedule` (cron) combined with
`workflow_dispatch` for both automatic and manual triggering.

**Chosen performance axis**: fail-safe over build-time convenience — the
job split (build vs. deploy) plus `needs:`/`if:` gating is what makes a
failed generation step a no-op for the live site rather than requiring
a bespoke rollback mechanism, directly serving requirement 5.

**Adopt**: two-job split with success gating (deploy only runs if build
succeeded); multiple `actions/checkout` calls in one job with distinct
`repository:`/`path:` inputs for the 3-board multi-repo checkout, no
token needed since all 3 are public.

**Skip**: nothing skipped — no competing pattern surfaced; this is the
single well-established official shape, not a field with real
alternatives to weigh.

**Segment fit**: rsb is a small, single-purpose internal dashboard, not
a large multi-environment site — the generic Actions-Pages pattern
applies directly with no scaling-down needed.

**Gap line**: current state has zero `.github/` surface (full gap) but
the dashboard is already no-build static HTML+JS with relative asset
links except one absolute fetch path (survey §6) — so the gap is
narrow: add the workflow + one line of JS, not restructure the app.

**Judge point / saturation**: would another round change a build
decision? No — official docs directly answer job structure, fail-safe
gating, and multi-repo checkout; stopped after stage 1.

Sources:
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://github.com/orgs/community/discussions/25900
- https://github.com/actions/checkout ; https://github.com/orgs/community/discussions/59488
