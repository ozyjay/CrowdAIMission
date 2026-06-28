# UX Spec — MVP 0.2

## UX goal

Visitors should understand the interaction in under 10–20 seconds:

> Scan in, vote, see the big screen change, and help keep the local AI on track.

MVP 0.2 should feel like a working crowd-control loop, not a collection of static pages.

## Screens

| Screen | Route | Audience | Purpose |
|---|---|---|---|
| Visitor phone | `/` | Visitors | Vote through the current mission phase |
| Big screen | `/screen` | Passersby | Show mission state and visible control loop |
| Staff panel | `/staff` | Staff / developer | Select mission, reset, fallback, inspect state |
| Replay | `/replay` | Everyone | Prepared no-phone fallback loop |
| Health | `/health` | Staff / developer | Service status |

## Shared state phases

Use a small explicit phase model:

```text
idle
vote_goal
vote_rule
proposal
checks
crowd_decision
result
fallback
replay
```

## Visitor phone UX

### Idle phase

Show:

```text
Humans in the Loop
Can the crowd keep a local AI on track?

Current mission: Game Studio Mission
Waiting for the next vote…
```

### Vote goal phase

Show:

```text
What should the helper do?

[Help the player escape]
[Help find a lost robot]
[Help solve a puzzle]
[Help avoid a trap]
```

After vote:

```text
Vote received.
Watch the big screen.
```

### Vote rule phase

Show:

```text
What rule should keep the AI on track?

[Do not give away the answer]
[Keep it fair]
[Make it funny, not mean]
[Ask the player a question]
```

### Proposal/check phase

Show:

```text
The local AI is proposing.
Watch the big screen.
```

In MVP 0.2, this is deterministic and should be treated as a prepared proposal.

### Crowd decision phase

Show:

```text
Is the local AI on track?

[Use it]
[Repair it]
[Needs evidence]
[Ask a human]
[Use fallback]
```

### Result phase

Show:

```text
Round complete.
The crowd kept the AI on track.
```

## Big-screen UX

The big screen must be readable from booth distance.

Use large sections:

```text
PEOPLE SET THE GOAL
Help the player escape the reef lab

PEOPLE SET THE RULE
Do not give away the answer

LOCAL AI PROPOSED
“The door code is 4821.”

SOFTWARE CHECKED
Intent: partial
Rule: fail
Evidence: not required
Safety: pass

CROWD DECIDED
Repair it

MISSION UPDATED
Give a hint instead
```

## Big-screen design rules

- Show one primary state at a time.
- Use large text and obvious labels.
- Show vote counts only after vote submission or after the round closes, to reduce herding.
- Do not show raw hidden prompts or model internals.
- Do not claim to show private model reasoning.
- If MVP uses deterministic proposals, avoid public wording that implies live AI generation.

## Staff panel UX

Staff controls should be simple and explicit.

Required controls:

```text
Mission
[Game Studio] [Deepfake Detective] [Future Me Quest]

Round
[Start / Next phase] [Reset round] [Clear votes]

Mode
[Live] [Fallback] [Replay]

Danger zone
[Clear session state]
```

Status panel:

```text
Mode: live
Mission: game-studio
Phase: vote_rule
Connected clients: 3
Votes this phase: 7
Last reset: 10:42 AM
```

## Replay UX

Replay mode should be a prepared loop that does not require phones.

It should show:

```text
Live voting unavailable.
Showing a prepared run.

This shows the same idea in a reliable way:
people set the goal, local AI proposes, software checks, humans decide.
```

## Fallback UX

Fallback is not a failure state. It is a public-safe mode.

Use:

```text
Live mode is unavailable right now.
Showing a prepared demo run.
```

Avoid:

```text
The AI crashed.
```

## MVP 0.2 round timing

Manual staff advancement is acceptable for MVP 0.2.

Suggested timing once automated:

| Phase | Suggested duration |
|---|---:|
| Vote goal | 15–20 seconds |
| Vote rule | 15–20 seconds |
| Proposal/check reveal | 10 seconds |
| Crowd decision | 15–20 seconds |
| Result | 10–15 seconds |

## Accessibility / booth readability

- Large buttons on phones.
- Avoid tiny QR or tiny screen text.
- High contrast.
- Do not require typing.
- Do not require accounts.
- Allow visitors who do not scan to understand the big screen.

## MVP 0.2 UX acceptance

- A new visitor can understand what to tap without staff explanation.
- The big screen makes the crowd contribution visible.
- Staff can reset without terminal commands.
- Replay mode still communicates the thesis.
