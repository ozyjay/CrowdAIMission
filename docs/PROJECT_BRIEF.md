# Project Brief — Humans in the Loop

## Working title

**Humans in the Loop: Can the crowd keep a local AI on track?**

## Short public pitch

Scan in, vote on a mission, watch a local AI propose what to do, and help decide whether it is useful, safe, factual, or off track.

## The IT@JCU story

This demo shows that AI is not just a chatbot. IT professionals design the systems around AI: networks, interfaces, local services, real-time updates, data handling, validation, privacy, reset, and fallback.

The local AI is useful because it can be fast, private/offline-capable, and cheaper to run, but it has limits. The demo makes those limits visible and shows how people, rules, evidence, and software checks keep the system useful.

## Core thesis

Local AI can support productive work when humans remain in the loop and the surrounding software system keeps the model on track.

## What the crowd does

The crowd acts as the human control layer:

1. chooses the mission;
2. sets the goal;
3. sets the rule or constraint;
4. evaluates the local AI proposal;
5. decides whether to accept, repair, reject, ask for evidence, ask a human, or fall back.

## What the AI does

The local SLM proposes a bounded response, action, hint, caption, or repair. It never directly controls public state.

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
Intent ✓  Schema ✓  Safety ✓  Evidence ?

CROWD DECIDED
Repair it

MISSION UPDATED
...
```

## What this is not

This is not:

- a generic AI art demo;
- an open chatbot;
- a truth-by-majority voting game;
- a claim that human-AI teams are always better;
- a claim that local models are automatically correct or safe.

## Success criteria

A visitor should understand within 30 seconds that:

- the AI is local and limited;
- people give it direction;
- software checks its proposal;
- humans can reject or repair it;
- fallback is part of responsible design.
