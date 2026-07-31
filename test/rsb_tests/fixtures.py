"""Fixture payloads for rsb tests, including the worked example from
docs/specs/flows-schema.md §7.
"""

WORKED_EXAMPLE = {
    "schema_version": 1,
    "generated_at": "2026-07-31T08:00:00Z",
    "repo": "tokenmaxxxer/on-the-record",
    "decision_queue": [
        {
            "issue": 172,
            "pr": 201,
            "phase": 2,
            "role": "implementation",
            "opened_at": "2026-07-30T09:12:00Z",
            "age_hours": 22.8,
            "awaiting": "approve-full",
        }
    ],
    "flows": [
        {
            "issue": 172,
            "stage": "implementing",
            "stage_derived": True,
            "roles": [{"role": "implementation", "loop_state": "scope-approved", "verdict": "pending"}],
            "prs": [201],
        }
    ],
    "sessions": [
        {
            "role": "implementation",
            "issue": 172,
            "elapsed_min": 9.5,
            "pid": 48213,
            "alive": True,
            "verdict": "pending",
        }
    ],
    "ledger": [{"issue": 172, "sessions": 2, "cost_usd_total": 3.14, "outcomes": {"progressed": 1, "refused": 1}}],
    "unattributed": {"sessions": 0, "cost_usd_total": 0.0},
    "hygiene": {
        "closure_sweep": [
            {
                "issue": 170,
                "violation": "closed_without_delivered_stage",
                "detail": "issue closed while role implementation loop_state=scope-proposed",
            }
        ],
        "unapproved_open_prs": [
            {"issue": 172, "pr": 201, "role": "implementation", "opened_at": "2026-07-30T09:12:00Z"}
        ],
    },
}

EMPTY_PAYLOAD = {
    "schema_version": 1,
    "generated_at": "2026-07-31T08:00:00Z",
    "repo": "tokenmaxxxer/empty-repo",
    "decision_queue": [],
    "flows": [],
    "sessions": [],
    "ledger": [],
    "hygiene": {"closure_sweep": [], "unapproved_open_prs": []},
}

RAW_STAGE_PAYLOAD = {
    "schema_version": 1,
    "generated_at": "2026-07-31T08:00:00Z",
    "repo": "tokenmaxxxer/raw-stage",
    "decision_queue": [],
    "flows": [
        {
            "issue": 300,
            "stage": "some-unmapped-loop-state",
            "stage_derived": False,
            "roles": [{"role": "implementation", "loop_state": "some-unmapped-loop-state", "verdict": "progressed"}],
            "prs": [],
        }
    ],
    "sessions": [
        {
            "role": "implementation",
            "issue": 300,
            "elapsed_min": 1.0,
            "pid": 1,
            "alive": False,
            "verdict": "refused",
            "last_activity": None,
        }
    ],
    "ledger": [],
    "hygiene": {"closure_sweep": [], "unapproved_open_prs": []},
}

WITH_LAST_ACTIVITY_PAYLOAD = {
    "schema_version": 1,
    "generated_at": "2026-07-31T08:00:00Z",
    "repo": "tokenmaxxxer/last-activity",
    "decision_queue": [],
    "flows": [],
    "sessions": [
        {
            "role": "implementation",
            "issue": 172,
            "elapsed_min": 14.2,
            "pid": 48213,
            "alive": True,
            "verdict": "pending",
            "last_activity": {
                "ts": "2026-07-31T12:03:44Z",
                "kind": "tool_use",
                "detail": "Write roles/data-modeling.json",
            },
        }
    ],
    "ledger": [],
    "hygiene": {"closure_sweep": [], "unapproved_open_prs": []},
}
