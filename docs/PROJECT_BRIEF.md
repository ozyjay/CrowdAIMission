# Project Brief — Humans in the Loop

## Working title

**Humans in the Loop: Can the crowd keep a local AI on track?**

## Short public pitch

Scan in, vote on a mission, watch a local AI proposal, and help decide whether it is useful, safe, factual, or off track.

## Current build phase

**MVP 0.2 — Real Round Loop**

The initial local-network smoke test has worked: a mobile phone could connect to the app running on a Mac. The next step is a real round loop with voting, screen update, staff reset, and replay/fallback.

## The IT@JCU story

This demo shows that AI is not just a chatbot. IT professionals design the systems around AI: networks, interfaces, local services, real-time updates, data handling, validation, privacy, reset, and fallback.

The local AI is useful because it can be fast, private/offline-capable, and cheaper to run, but it has limits. The demo makes those limits visible and shows how people, rules, evidence, and software checks keep the system useful.

## Core thesis

Local AI can support productive work when humans remain in the loop and the surrounding software system keeps the model on track.

## What the crowd does

The crowd acts as the human control layer:

1. chooses or joins a mission;
2. sets the goal;
3. sets the rule or constraint;
4. evaluates the local-AI-style proposal;
5. decides whether to accept, repair, reject, ask for evidence, ask a human, or fall back.

## What the AI does

In the final concept, a local SLM proposes a bounded response, action, hint, caption, or repair.

In MVP 0.2, this is represented by deterministic proposal templates so the team can test the interaction safely before adding a live model.

The AI or proposal generator never directly controls public state.

## What the software does

The application checks:

- intent match;
- schema validity;
- rule compliance;
- evidence requirements;
- public safety;
- timeout and fallback.

## What the big screen shows

The big screen should make the control loop visible:

```text
PEOPLE SET THE GOAL
...

PEOPLE SET THE RULE
...

LOCAL AI PROPOSED
...

SOFTWARE CHECKED
...

CROWD DECIDED
...

MISSION UPDATED
...
```

This is external system state, not private model reasoning.

## Primary audiences

### Highschoolers

Use missions that feel relevant to games, online truth, schoolwork, future choices, and creative tech.

### Parents and carers

Use missions that show accuracy, privacy, evidence, and when the system should ask staff rather than guess.

### Kids and passersby

Use visual missions such as Reef Rescue or Game Studio to create an immediate hook.

## MVP 0.2 mission focus

Build three highschool-friendly missions first:

1. **Game Studio Mission** — useful game helper without spoiling the game.
2. **Deepfake Detective / Truth Check** — unsupported AI claims and evidence checks.
3. **Future Me Quest** — turning interests into better Open Day questions without overclaiming.

## Public wording

Use:

> People set the goal, the local AI proposes, and the software checks before the result is used.

Use:

> This shows the system’s control state, not private model reasoning.

Avoid:

> The AI is thinking.

Avoid:

> The crowd makes the AI correct.

## Why this is not just an image demo

The visual output is only the surface. The point is the system around the model:

- QR onboarding;
- local network service;
- phone controller;
- big-screen state;
- staff controls;
- evidence and safety checks;
- reset and fallback;
- local model constraints.

## MVP 0.2 success statement

MVP 0.2 succeeds if a phone can guide a complete mission round, the screen updates visibly, staff can reset and replay, and the whole loop works with deterministic content and no AI dependency.
