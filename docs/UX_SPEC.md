# UX Specification

## Design goal

Make the human-control loop visible, fast, and understandable from a distance.

The visitor should not need to understand model internals. They should understand:

```text
People set the goal.
The local AI proposes.
Software checks.
Humans decide.
The mission updates.
```

## Public title screen

```text
Humans in the Loop
Can the crowd keep a local AI on track?

Scan. Vote. Check. Guide.
```

## Routes

| Route | Device | Purpose |
|---|---|---|
| `/` | Visitor phone | Join current mission and vote |
| `/screen` | Big screen | Public mission display |
| `/staff` | Staff laptop/local display | Select mission, reset, fallback, replay |
| `/api/vote` | API | Receive vote |
| `/ws` | WebSocket | Push mission state to phones and screen |
| `/health` | Staff/technical | Service status |
| `/replay` | Big screen | Fallback/replay mode |
| `/qr.svg` | Screen/staff asset | QR code for joining the visitor phone controller |

## Phone UX

The phone UI should be extremely simple:

1. Join current round.
2. Vote on one question.
3. Wait / see crowd status.
4. Vote on check/repair if prompted.
5. Return to next round.

### Phone principles

- Use large buttons.
- Keep each vote to 3–5 choices.
- Avoid typing in public mode.
- Show only the current mission and current vote.
- Do not require login, name, email, or phone number.
- Do not expose staff controls.

## Big-screen UX

The big screen is the main public artifact.

Recommended layout:

```text
┌────────────────────────────────────────────────────┐
│ HUMANS IN THE LOOP                                 │
│ Can the crowd keep a local AI on track?            │
├─────────────────────┬──────────────────────────────┤
│ Mission visual       │ Control pipeline             │
│                     │ PEOPLE SET THE GOAL          │
│ [map/card/canvas]    │ PEOPLE SET THE RULE          │
│                     │ LOCAL AI PROPOSED            │
│                     │ SOFTWARE CHECKED             │
│                     │ CROWD DECIDED                │
│                     │ MISSION UPDATED              │
├─────────────────────┴──────────────────────────────┤
│ QR code | current vote | round timer | fallback tag │
└────────────────────────────────────────────────────┘
```

The QR code should be generated locally and point to `/` on the same host used to open `/screen`. In rehearsal, staff should open `/screen` with the demo machine LAN address so visitors scan a phone-reachable URL.

## Staff UX

The staff UI should include:

- select mission;
- start round;
- close round;
- force result;
- reset current mission;
- clear all visitor input;
- show fallback/replay;
- toggle local AI on/off;
- trigger safe example failure;
- show health/status.

Staff controls should be local-only or protected by booth network/physical controls.

Staff UI should also show the same join QR code as the screen, so staff can test phone onboarding without using the big display.

## Round timing

Target round length: 60–120 seconds.

Example:

| Time | Activity |
|---:|---|
| 0s | Mission and QR visible |
| 15s | Vote on goal |
| 30s | Vote on rule |
| 45s | Local AI proposes |
| 60s | Checks shown |
| 75s | Crowd accepts/repairs/rejects |
| 90s | Mission updates |
| 105s | Next round starts |

## Vote types

### Goal vote

“What should the mission try to do?”

### Rule vote

“What must the local AI remember?”

### Check vote

“Is the local AI on track?”

### Repair vote

“What help does the AI need?”

Options:

- clearer goal;
- stronger rule;
- approved evidence;
- shorter response;
- ask a human;
- safe fallback.

## Fallback UX

Fallback is not a failure state. Use this copy:

```text
Live mode unavailable.
Showing a prepared mission run.
It shows the same idea in a reliable way.
```

## Accessibility and booth usability

- Use large readable text.
- Do not rely on subtle colour changes only.
- Use icons plus labels.
- Keep phone buttons thumb-sized.
- Keep big-screen states readable from 2–3 metres.
- Make reset state obvious.
