# MVP 0.2 Plan — Real Round Loop

## Goal

Turn the smoke-test app into a working crowd-control loop that can be tested with a phone, a big screen, and staff controls.

MVP 0.2 should still work with **no AI model dependency**.

## User-facing thesis

> Can the crowd keep a local AI on track?

For MVP 0.2, “local AI” is represented by deterministic proposal templates. This lets the team prove the interaction design, networking, state model, staff controls, and fallback before adding a real model.

## Required deliverables

| Deliverable | Requirement |
|---|---|
| Visitor route | `/` shows current mission, phase, and tap-based options |
| Screen route | `/screen` shows the live mission state and control pipeline |
| Staff route | `/staff` selects mission, resets state, clears votes, enables fallback/replay |
| Replay route | `/replay` shows a prepared no-phone demo flow |
| Health route | `/health` returns service status |
| State API | `/api/state` returns current server-owned state |
| Missions API | `/api/missions` returns enabled mission metadata |
| Vote API | `/api/vote` records one vote for the current phase |
| Live updates | `/ws` broadcasts state changes, or polling refreshes state |
| Mission deck | At least Game Studio, Deepfake Detective, Future Me Quest |
| Tests | Smoke test routes and basic state/vote/reset behaviour |

## MVP 0.2 round flow

```text
idle
→ vote_goal
→ vote_rule
→ proposal
→ checks
→ crowd_decision
→ result
→ next round OR reset
```

Staff can force:

```text
fallback
replay
reset
mission change
```

## Visitor phone UX

The phone must only show the relevant action for the current phase.

Examples:

- choose a goal;
- choose a rule;
- decide whether the proposal is on track;
- choose repair direction.

No open free text in MVP 0.2.

## Big-screen UX

The screen should always show the visible control loop:

```text
PEOPLE SET THE GOAL
PEOPLE SET THE RULE
LOCAL AI PROPOSED
SOFTWARE CHECKED
CROWD DECIDED
MISSION UPDATED
```

For MVP 0.2, label deterministic proposals carefully in internal/dev copy. If shown publicly, use language like “prepared local-AI-style proposal” or “simulated proposal” until a live model is actually connected.

## Staff UX

`/staff` should support:

- select mission;
- start/restart round;
- advance phase if automatic timing is not implemented;
- reset round;
- clear all votes;
- force fallback;
- show replay;
- inspect current state;
- see connected client count if available.

## Mission scope

Build these first:

1. Game Studio Mission.
2. Deepfake Detective / Truth Check.
3. Future Me Quest.

Each mission must have deterministic data for:

- goals;
- rules;
- proposal examples;
- check results;
- crowd decision options;
- repaired/fallback result.

## Out of scope for MVP 0.2

Do not build these yet:

- live local SLM calls;
- open visitor text;
- user accounts;
- persistent visitor profiles;
- database persistence;
- admin authentication beyond local/staff route assumptions;
- image generation;
- real deepfake detection;
- real course/career advice.

## Acceptance tests

MVP 0.2 is complete when:

- `./scripts/check_ports.sh` passes;
- `./scripts/smoke_test.sh` passes;
- `/` loads on a phone over LAN;
- a phone vote updates `/screen`;
- `/staff` can reset state;
- `/staff` can switch missions;
- `/staff` can force `/screen` into fallback/replay;
- three missions can complete a full round;
- no route requires login, app install, personal data, or free text;
- model-enabled features can be absent or disabled.

## Manual test script

1. Start app on port `3200`.
2. Open `/screen` on desktop browser.
3. Open `/staff` on desktop browser.
4. Open `/` on phone using LAN IP.
5. Select **Game Studio Mission** in staff route.
6. Vote from phone for goal.
7. Confirm screen updates.
8. Vote from phone for rule.
9. Confirm deterministic proposal appears.
10. Vote on whether proposal is on track.
11. Confirm result screen appears.
12. Reset from staff route.
13. Repeat for Deepfake Detective and Future Me Quest.
14. Trigger replay/fallback from staff route.
15. Confirm no visitor input remains after reset.
