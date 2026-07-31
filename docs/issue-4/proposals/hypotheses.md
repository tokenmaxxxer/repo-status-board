# Hypotheses & pre-registered pilot design — issue #4 (web dashboard)

Status: phase-1 proposal. Scope: product-discovery only — problem
definition, hypotheses, pre-registered metrics/thresholds/decision rule,
and the resulting spec-or-kill call for whether this pilot should proceed
to interaction-design. Screens, flows, and visual design are explicitly
out of scope (next role's write surface).

## 1. Problem definition (operator's, not the tool's)

Operator (solo repo owner) currently must have a terminal open, running
`rsb` against `boards.toml`, to know: is anything waiting on me right
now, and is anything drifting/stuck? That terminal is tied to one
machine/session. The operator's actual behavior is a **glance-and-return**
check — not a working session at the dashboard — done from wherever they
happen to be (phone, another machine, mid-conversation on a different
task), several times a day while agents are running unattended.

Restated as a falsifiable user problem: *when the operator is away from
the terminal that has `rsb` open, they cannot answer "does anything need
my decision right now?" without switching context back to that terminal,
and this creates either (a) missed/delayed decisions or (b) needless
context-switches back to check when nothing needed them.*

This is a hypothesis, not an established fact — there is no usage log to
confirm it (0→1, single user, no telemetry yet per survey.md). The pilot
below is designed to falsify or confirm it cheaply.

## 2. Hypotheses (falsifiable)

**H1 (need exists):** The operator checks board state from a
non-terminal context (phone/other device/browser) at least 3x/week when
one is available, indicating real off-terminal demand rather than
theoretical convenience.

**H2 (glance sufficiency):** A single-screen, read-only web view of the
same `flows --json` data the CLI already renders is sufficient to answer
"does anything need me" — i.e., the operator does not need to switch back
to the terminal/CLI after checking the web view, for at least 80% of
checks.

**H3 (attention signal matters):** Surfacing `decision_queue` age
(bucketed/dimmed, per scout gap line) measurably reduces missed or
late phase-1/phase-2 approvals compared to today's flat/CLI-only view.
(H3 is the hardest to test cheaply — see §5, deferred unless H1/H2 pass.)

## 3. Pre-registered metrics, thresholds, decision rule

Instrument (implementation-phase requirement, noted here as a hand-off):
every web-view load timestamped, tagged with device/UA class if trivially
available; no other telemetry, no accounts, no third-party analytics —
disproportionate for a single-user pilot (per scout skip: no multi-tenant
audience accounting).

Pilot window: **14 days** from first deployed web view.

| Metric | Threshold | Maps to |
|---|---|---|
| Off-terminal views/week | ≥ 3 | H1 |
| Terminal `rsb` invocations in the 10 min following a web view | < 20% of web views | H2 |
| Median time from web-view load to render | ≤ 3s | adoption pattern (scout: 15-30s load kills adoption) |
| Weekly-active-use floor, checked at day 14 | ≥ 1 view/week sustained | KPI-graveyard kill rule (scout) |

## 4. Decision rule (pre-committed)

At day 14, evaluate in this order:
1. If weekly-active-use floor is not met (< 1 view/week) → **KILL**. No
   further role work; record and close per contract's refusal path.
2. Else if off-terminal views/week < 3 (H1 fails) → **KILL** — problem
   framing was wrong, no off-terminal demand to serve.
3. Else if H2 fails (≥ 20% of web views followed by a terminal check
   within 10 min) → **REVISE**, not kill: the single-screen view is
   insufficient: hand off to interaction-design with an explicit note on
   which information gap forced the terminal check (log the follow-up
   terminal invocation's context if feasible), rather than proceeding to
   full spec.
4. Else (weekly-use floor met, H1 and H2 both pass) → **SPEC**: proceed
   to interaction-design for issue #4's next chain step. H3 is deferred —
   test only after a working web view exists and enough decision-queue
   events accumulate to compare late/missed approvals meaningfully; not
   a gate for this pilot's continuation.

This rule is mechanical and pre-committed: no post-hoc judgment call
substitutes for it at day 14.

## 5. Explicitly out of scope for this proposal
- Which screens/routes/visual design deliver the single-screen view —
  interaction-design's write surface.
- Auth/access model for exposing `flows --json`-derived data over the
  web — a security-relevant decision that belongs to whichever role
  specs the delivery mechanism (interaction-design/ux-engineering/
  implementation), flagged here as a hand-off, not decided.
- H3's measurement design (needs a "was this late/missed" definition) —
  deferred per §4 step 4, revisit only if the pilot reaches SPEC.
