# AGENTS.md — Crowd AI Mission Control

## Project thesis

This project is an Open Day demo called **Humans in the Loop: Can the crowd keep a local AI on track?**

The demo shows that a local small language model can be useful, fast, private/offline-capable, and cheaper to run, but it needs software engineering around it: clear goals, constrained inputs, evidence, validation, human feedback, reset, and fallback.

The AI is one component in a public interactive system. The crowd and staff remain in control.

## Current implementation phase

**MVP 0.2 — Real Round Loop**

MVP 0.1 is already proven at smoke-test level: a mobile phone could connect to the local app running on a Mac.

MVP 0.2 must add a real, no-AI round loop:

1. visitor vote on goal;
2. visitor vote on rule;
3. deterministic local-AI-style proposal;
4. visible software checks;
5. crowd decision vote;
6. screen update;
7. staff reset/fallback.

Do **not** add live SLM calls in MVP 0.2.

## Non-negotiable public-demo rules

- Do not collect names, phone numbers, emails, logins, or identifiable visitor data.
- Do not store visitor audio or video.
- Do not enable unsupervised open free text in visitor-phone UI.
- Prefer tap-based controls, short rounds, curated choices, and deterministic fallback.
- Do not claim to show private model reasoning.
- Do not say “the AI is thinking,” “the AI is always correct,” or “the AI solved this by itself.”
- Every live mode needs a replay/fallback mode.
- Every mission needs reset, clear session, and safe fallback paths.
- Staff must be able to operate the demo without developer-only terminal knowledge.
- A model-like proposal in MVP 0.2 is deterministic. Do not imply it is live AI in public copy unless live AI is actually enabled and labelled correctly.

## MVP 0.2 build priorities

Build in this order:

1. Route stability for `/`, `/screen`, `/staff`, `/replay`, `/health`, `/api/state`, `/api/missions`, and `/api/vote`.
2. Server-owned round state machine.
3. WebSocket or polling updates to `/screen` and `/staff`.
4. Staff controls: select mission, reset, clear votes, force fallback/replay.
5. Deterministic mission definitions for Game Studio, Deepfake Detective, and Future Me Quest.
6. Deterministic proposal generator and validation checks.
7. Smoke tests and one-phone LAN test.
8. Documentation update with actual launch/test results.

Only after MVP 0.2 is stable should the project add a local SLM adapter.

## Required routes

Minimum routes:

- `/` — visitor phone controller.
- `/screen` — big-screen display.
- `/staff` — staff controls.
- `/replay` — fallback/replay screen.
- `/health` — service health.
- `/api/state` — current round/session state.
- `/api/missions` — enabled mission metadata.
- `/api/vote` — submit tap-based vote.
- `/ws` — live state updates if using WebSockets.

## Ports

Use fixed ports.

- MVP single-app port: `3200`.
- Split backend/WebSocket port, if needed later: `8200`.
- Shared model adapter, if used later: `8600`.
- Replay service, if split later: `8700`.
- Health/status service, if split later: `8800`.

Do not silently fall back to random ports in Open Day mode.

## Architecture rules

- Canonical state must be owned by the server, not the browser.
- Visitor clients submit votes only; they do not authoritatively set mission state.
- The local SLM, when added later, may propose content but must not directly control state, routes, files, network, or public output.
- All proposal output must pass through the same validation pipeline, even if deterministic.
- Unknown actions, unknown assets, unsupported factual claims, malformed JSON, slow model calls, and unsafe text must fall back to deterministic content.
- Failed checks should be visible as external control state, not hidden as “AI reasoning.”

## MVP 0.2 state-machine expectations

Use a small explicit phase enum, for example:

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

Every phase should have:

- a visible screen state;
- a visitor-phone state;
- a staff-control state;
- a reset path.

## Mission design rules

Each mission must define:

- mission id;
- mission title;
- public hook;
- audience pull;
- allowed goals;
- allowed rules;
- allowed crowd decisions;
- deterministic proposal examples;
- check outcomes;
- safe failure examples;
- fallback response;
- staff script;
- test cases.

MVP 0.2 missions:

1. Game Studio Mission.
2. Deepfake Detective / Truth Check.
3. Future Me Quest.

## Coding conventions

- Keep code simple and inspectable.
- Prefer boring, reliable dependencies.
- Prefer explicit state transitions over clever implicit behaviour.
- Use environment variables for ports and hosts.
- Include tests for every new mission and state transition.
- Add or update docs when behaviour changes.
- Avoid large rewrites unless explicitly requested.

## Test expectations

Before marking MVP 0.2 complete:

- run port checks;
- run unit tests if present;
- run smoke tests;
- confirm reset works;
- confirm fallback/replay works;
- confirm visitor data can be cleared;
- confirm app starts on port `3200`;
- confirm `/screen`, `/`, `/staff`, `/health`, `/replay`, `/api/state`, and `/api/missions` work;
- confirm at least one phone can vote over LAN;
- record what has not yet been tested.

## Agent behaviour

When asked to implement work:

1. Read `README.md`, this file, `docs/MVP_0_2_PLAN.md`, `docs/UX_SPEC.md`, `docs/ARCHITECTURE.md`, and `docs/API_CONTRACT.md`.
2. Propose a short plan first.
3. Make the smallest useful change.
4. Add or update tests.
5. Do not introduce new dependencies without explaining why.
6. Do not add live AI or free text unless explicitly requested and documented.
7. Report changed files and test results.

Keep agent instructions concise. Put detailed design notes in `docs/`, not in this file.
