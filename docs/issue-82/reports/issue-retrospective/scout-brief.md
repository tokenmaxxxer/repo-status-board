# Scout brief — issue #82

Mode: 2 angles, batched-sequential (no parallel dispatch mechanism needed
for 2 low-depth angles; both resolved within stage 1). Stages used: 1
(sweep only — judge point 1 found no mismatch worth a deepening round;
saturation reached immediately, see below). Wall-clock: well under the
3min budget.

## Angle 1 — internal exemplar: earlier issue-retrospective records

Result: **none exist** (`find docs -iname '*retrospective*'` empty; see
survey.md). No recurred-prediction check is possible against a prior
internal record, because there is no prior record. This is itself the
finding this angle was aimed at: the repo has never before asked "did we
predict this failure," so any prediction latent in earlier
conformance-review/execution-observation findings (see below) was never
carried forward as a *retrospective* lesson — only as a per-issue Open
finding routed to a specific downstream role.

## Angle 2 — external exemplar: blameless postmortem practice

Must-bes extracted (Kano, from Google SRE / industry postmortem
practice):
- Root-cause analysis must dig past the surface trigger to systemic
  contributors — "tooling gaps, ambiguous runbooks, insufficient
  automation, missing tests, or unclear ownership" are the named example
  categories, and spec/requirement ambiguity is the same shape of
  contributor.
- Action items need a named owner (not "the team") to have any chance of
  being completed.
- The postmortem's purpose is systemic, not individual: "understand what
  systemic factors led to the incident... without indicting any
  individual or team."

Performance axis this repo's chain already meets: contributing-factor
framing over single-cause attribution — conformance-review's finding 5
already names the contradiction as a property of the issue text (three
mutually inconsistent AC/요구사항/범위밖 clauses), not a person's mistake,
and routes it to "the issue author" as a role, not a name.

Performance axis this repo's chain does NOT yet meet: the named-owner
action-item discipline exists ad hoc per finding (conformance-review's
findings 1-6 each carry `addressed_to:`) but there is no standing gate
that runs *before* an issue like #44 is authored, checking that its own
AC/요구사항/범위밖 sections do not contradict each other. Every gate in the
chain so far is downstream-of-authoring (conformance-review catches it
after the artifact ships).

Pattern to adopt: contributing-factors framing (already present in this
repo's own conformance-review role — no import needed).
Pattern to (consciously) not adopt: postmortem's "immediate mitigation vs.
long-term fix" two-tier action item split — issue #82's action items are
advisory-only per this role's contract and never gate landing, so a
mitigation/long-term split adds structure this role's own contract does
not use; noted as considered and skipped, not silently dropped.

Sources:
- https://postmortems.pagerduty.com/culture/blameless/
- https://sre.google/sre-book/postmortem-culture/
- https://rootly.com/incident-postmortems

## Judge point 1 / saturation

Both angles converge on one gap: no pre-authoring consistency check for
AC/요구사항/범위밖ections exists on this repo, and the chain's only defense
is a downstream review role plus a follow-up requirements-engineering
issue. A second deepening round would not change this — the gap is
already convergent across the one internal and one external angle
available. Stopped at stage 1.

## Gap line

Field must-be already met: contributing-factors framing (not
single-cause), owner-named routing of findings. Field must-be missing:
a gate applied at spec-authoring time, before implementation — every
existing check in this repo's chain runs after the artifact exists.
