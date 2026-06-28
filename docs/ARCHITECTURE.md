# Technical Architecture

## MVP architecture

Use a single local app first.

```text
Visitor phones  →  /              ┐
Big screen      →  /screen        ├─ FastAPI local server on :3200
Staff UI        →  /staff         │
Votes           →  /api/vote      │
Join QR         →  /qr.svg        │
Live updates    →  /ws            ┘
```

The app should run without a model. Local SLM support is an optional layer added after deterministic rounds work.

## Components

| Component | Responsibility |
|---|---|
| Mission controller | Owns mission state and round transitions |
| Vote aggregator | Counts votes and chooses round result |
| Proposal engine | Deterministic template first, local SLM later |
| Validation pipeline | Checks intent, schema, rules, evidence, and safety |
| Renderer | Updates screen state from approved mission state |
| QR renderer | Generates a local SVG join code for `/` on the request host |
| Staff controls | Reset, fallback, mission select, clear state |
| Replay mode | Prepared run for no-phone/no-model fallback |
| Health endpoint | Basic readiness and status |

## State ownership

The server owns authoritative state.

Phones submit votes only. Phones do not own mission state, selected winner, model output, or screen content.

## Mission state model

```json
{
  "session_id": "current",
  "mission_id": "game_studio",
  "round": 3,
  "phase": "checking",
  "goal": "help_player_escape",
  "rule": "do_not_spoil_solution",
  "votes": {
    "use_it": 4,
    "repair": 9,
    "reject": 1
  },
  "proposal": {
    "action": "npc_hint",
    "asset_id": "npc_helper",
    "caption": "Look for numbers hidden near the oxygen tanks.",
    "source_ids": [],
    "requires_review": false
  },
  "checks": {
    "intent": "pass",
    "schema": "pass",
    "rules": "pass",
    "evidence": "not_required",
    "safety": "pass"
  },
  "mode": "live"
}
```

## Proposal schema

All AI/model proposals must be parsed into a schema like:

```json
{
  "action": "string_enum",
  "asset_id": "string_enum",
  "caption": "short_string",
  "source_ids": ["string"],
  "requires_review": true
}
```

Unknown enum values are rejected.

## Validation pipeline

```text
Raw proposal
→ parse JSON
→ schema validation
→ mission action whitelist
→ asset whitelist
→ intent check against winning vote
→ rule check
→ evidence check if factual claim exists
→ safety check
→ approve, repair, review, or fallback
```

## Local SLM rules

The local SLM may:

- write a short caption;
- choose one approved action;
- suggest one repair;
- classify a canned example;
- propose a hint within constraints.

The local SLM may not:

- execute code;
- change vote totals;
- control routes;
- alter staff settings;
- invent factual claims without evidence;
- publish directly to screen without validation.

## Suggested file layout for implementation

```text
app/
  main.py
  config.py
  state.py
  missions/
    base.py
    game_studio.py
    truth_check.py
    future_me.py
    study_coach.py
    reef_rescue.py
    squad_chat.py
  proposals/
    templates.py
    local_slm.py
    schemas.py
  validation/
    intent.py
    rules.py
    evidence.py
    safety.py
  static/
    phone.html
    screen.html
    staff.html
    styles.css
    app.js
  tests/
    test_missions.py
    test_validation.py
    test_routes.py
```

## Port plan

| Mode | Port |
|---|---:|
| Single local app | `3200` |
| Split QR backend/WebSocket, if needed later | `8200` |
| Shared model adapter | `8600` |
| Replay service | `8700` |
| Health/status service | `8800` |

## Offline-first design

The application must remain demonstrable when:

- local model runtime is unavailable;
- Wi-Fi has no internet;
- visitor phones cannot join;
- QR scanning is unavailable;
- WebSocket fails;
- model output is malformed;
- model output is slow.

Fallback order:

1. live local SLM;
2. deterministic template proposal;
3. staff-controlled mode;
4. replay mode;
5. static explainer screen.

The QR route must not depend on an external QR service. It should generate a local SVG so the demo works on a private or offline booth network.
