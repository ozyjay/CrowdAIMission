# Codex Prompts

Use these prompts for incremental implementation.

## MVP 0.2 — Plan only

```text
Read README.md, AGENTS.md, docs/MVP_0_2_PLAN.md, docs/UX_SPEC.md, docs/ARCHITECTURE.md, docs/API_CONTRACT.md, and docs/TEST_PLAN.md.

Create a short implementation plan for MVP 0.2. Do not code yet.

The goal is a no-AI real round loop on port 3200 with visitor, screen, staff, replay, health, state, missions, vote, and optional WebSocket routes.

Include proposed file changes, state model, tests, and fallback behaviour. Keep dependencies minimal.
```

## MVP 0.2 — Implement state and routes

```text
Implement MVP 0.2 route and state foundations.

Requirements:
- run on APP_PORT from .env, default 3200;
- provide GET /, /screen, /staff, /replay, /health, /api/state, /api/missions;
- provide POST /api/vote, /api/staff/mission, /api/staff/reset, /api/staff/mode, /api/staff/advance;
- keep state server-owned and in memory;
- no live AI calls;
- no visitor free text;
- no login or personal data;
- update scripts/smoke_test.sh if needed.

Add basic tests or smoke checks. Report changed files and test results.
```

## MVP 0.2 — Add mission deck

```text
Add deterministic mission definitions for:
1. Game Studio Mission
2. Deepfake Detective / Truth Check
3. Future Me Quest

Use docs/MISSION_DECK.md as the content source.

Each mission needs goals, rules, deterministic proposals, check outcomes, crowd decision options, fallback result, and staff script.

Add validation that mission ids and option ids are stable and unique. Add tests.
```

## MVP 0.2 — Add round loop UX

```text
Update /, /screen, and /staff to support the full MVP 0.2 round loop:
idle -> vote_goal -> vote_rule -> proposal -> checks -> crowd_decision -> result.

Visitor route should show only the current vote options.
Screen route should show the visible control pipeline.
Staff route should select mission, advance phase, reset, clear votes, and force fallback/replay.

Do not add live AI. Use deterministic proposals. Add or update tests.
```

## MVP 0.2 — Add live update mechanism

```text
Add WebSocket updates via /ws, or implement simple polling if WebSockets are not already stable.

The screen and staff views should update after a phone vote or staff action.

Do not over-engineer. If WebSockets add too much complexity, prefer polling for MVP 0.2 and document the trade-off.
```

## MVP 0.2 — Hardening pass

```text
Review the app against AGENTS.md and docs/TEST_PLAN.md.

Fix MVP 0.2 readiness gaps:
- route smoke tests pass;
- phone vote updates screen;
- staff reset works;
- fallback/replay works;
- no AI dependency;
- no free text;
- no personal data;
- fixed port 3200;
- clear documentation of what is and is not proven.

Return changed files and test results.
```

## Later — Local SLM adapter, not MVP 0.2

```text
Do not run this until MVP 0.2 is stable.

Add a local SLM adapter behind MODEL_ENABLED=false/true. The app must continue to work with MODEL_ENABLED=false.

The model may only produce structured proposal JSON. All outputs must pass validators before display. Add timeout and deterministic fallback.
```
