# Architecture — MVP 0.2

## Current architecture target

MVP 0.2 is a single local web app running on port `3200`.

```text
Visitor phones  ─┐
                 ├── HTTP/WebSocket ── Local app on :3200 ── Big screen
Staff browser   ─┘                         │
                                           └── in-memory mission state
```

No live model is required for MVP 0.2.

## Components

| Component | Purpose |
|---|---|
| Visitor UI | Tap-based controller for the current mission phase |
| Screen UI | Big-screen visualisation of the round state |
| Staff UI | Mission select, reset, fallback/replay, state inspection |
| State store | Server-owned in-memory session and vote state |
| Mission deck | Static mission definitions and deterministic proposal templates |
| Proposal generator | Deterministic MVP stand-in for local AI proposal |
| Validator | Intent, schema, rule, evidence, and safety checks |
| Broadcaster | WebSocket or polling state updates |
| Replay mode | No-phone fallback sequence |

## Server-owned state

Visitor clients must not own authoritative state. They submit votes only.

Suggested shape:

```json
{
  "mode": "live",
  "mission_id": "game-studio",
  "round_id": 3,
  "phase": "vote_rule",
  "goal_choice_id": "escape_reef_lab",
  "rule_choice_id": null,
  "proposal": null,
  "checks": [],
  "crowd_decision_id": null,
  "votes": {
    "vote_goal": {
      "escape_reef_lab": 5,
      "find_lost_robot": 2
    },
    "vote_rule": {}
  },
  "client_count": 3,
  "updated_at": "2026-06-28T10:42:00+10:00"
}
```

## Phase transitions

```text
idle
  ↓ staff start
vote_goal
  ↓ staff next / timer
vote_rule
  ↓ staff next / timer
proposal
  ↓ generated deterministic proposal
checks
  ↓ validator result
crowd_decision
  ↓ staff next / timer
result
  ↓ reset or next round
vote_goal
```

Staff can force transition to:

```text
fallback
replay
idle
```

## Required routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Visitor phone UI |
| `/screen` | GET | Big-screen UI |
| `/staff` | GET | Staff controls |
| `/replay` | GET | Prepared fallback route |
| `/health` | GET | Health check |
| `/api/state` | GET | Current state |
| `/api/missions` | GET | Mission deck summary |
| `/api/vote` | POST | Submit vote |
| `/api/staff/mission` | POST | Select active mission |
| `/api/staff/reset` | POST | Reset round/session |
| `/api/staff/mode` | POST | live/fallback/replay |
| `/api/staff/advance` | POST | Advance phase manually |
| `/ws` | WebSocket | Broadcast state updates |

See `docs/API_CONTRACT.md`.

## Proposal generation in MVP 0.2

Use deterministic templates. Example:

```json
{
  "proposal_id": "game_spoiler_001",
  "action": "give_hint",
  "text": "The door code is 4821.",
  "intended_failure": "rule_break",
  "requires_evidence": false
}
```

This proposal then goes through the same validator that a future model output would use.

## Validation checks

Checks should return explicit labels:

```json
[
  {"check": "intent", "status": "partial", "message": "Related to the chosen goal."},
  {"check": "rule", "status": "fail", "message": "Gives away the answer."},
  {"check": "evidence", "status": "not_required", "message": "No factual claim."},
  {"check": "safety", "status": "pass", "message": "Public-safe."}
]
```

Allowed statuses:

- `pass`
- `partial`
- `warn`
- `fail`
- `not_required`
- `needs_human`
- `fallback_used`

## WebSocket vs polling

Preferred:

```text
state changes → broadcast over /ws → screen/staff/phones update
```

Acceptable MVP fallback:

```text
screen/staff/phones poll /api/state every 1–2 seconds
```

Do not block MVP 0.2 on WebSocket polish.

## Future local SLM architecture

Not in MVP 0.2.

Later:

```text
mission state → local SLM adapter → structured proposal JSON → validator → screen
```

Rules for future model layer:

- feature-flagged;
- timeout quickly;
- deterministic fallback;
- schema validation before use;
- no direct public rendering of raw model output;
- no direct state mutation by model output.

## Persistence

MVP 0.2 should use in-memory state only.

Do not add a database unless there is a clear need.

## Logs

Logs should be technical and non-identifying:

- route hit;
- phase transition;
- mission id;
- vote counts;
- validation status;
- errors.

Do not log names, phone numbers, emails, raw free text, or device identifiers.
