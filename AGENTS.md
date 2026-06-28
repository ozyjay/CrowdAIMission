# AGENTS.md — Crowd AI Mission Control

## Project thesis

This project is an Open Day demo called **Humans in the Loop: Can the crowd keep a local AI on track?**

The demo shows that a local small language model can be useful, fast, private/offline-capable, and cheaper to run, but it needs software engineering around it: clear goals, constrained inputs, evidence, validation, human feedback, reset, and fallback.

The AI is one component in a public interactive system. The crowd and staff remain in control.

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

## Build priorities

Build in this order:

1. Static mission screens and `/screen`, `/`, `/staff` routes.
2. QR phone-to-screen proof of concept with no AI dependency.
3. Voting round state machine.
4. Deterministic mission renderer and canned responses.
5. Validation pipeline: intent, schema, rule, evidence, safety.
6. Local SLM proposal layer with timeout and fallback.
7. Staff controls, replay mode, health checks, and smoke tests.
8. Polish, kiosk mode, and rehearsal hardening.

Do not add live AI generation before the no-AI deterministic version works.

## Required routes

Minimum routes:

- `/` — visitor phone controller.
- `/screen` — big-screen display.
- `/staff` — staff controls.
- `/api/vote` — submit vote.
- `/ws` — live updates.
- `/health` — service health.
- `/replay` — fallback/replay screen.

## Ports

Use fixed ports.

- MVP single-app port: `3200`.
- Split backend/WebSocket port, if needed later: `8200`.
- Shared model adapter, if used later: `8600`.
- Replay service, if split later: `8700`.
- Health/status service, if split later: `8800`.

Do not silently fall back to random ports in Open Day mode.

For same-Wi-Fi phone testing, start the single-app MVP with `APP_HOST=0.0.0.0 ./scripts/start_dev.sh` and use the printed `Phone URL`. Do not tell visitors or staff to use `127.0.0.1` from a phone.

## Architecture rules

- The local SLM may propose content but must not directly control state, routes, files, network, or public output.
- Canonical state must be ordinary software data.
- All model output must be schema-validated before use.
- Unknown actions, unknown assets, unsupported factual claims, malformed JSON, slow model calls, and unsafe text must fall back to deterministic content.
- A failed check should be visible as an external control state, not hidden as “AI reasoning.”

## Mission design rules

Each mission must define:

- mission title;
- public hook;
- audience pull;
- allowed goals;
- allowed rules;
- allowed actions;
- safe failure examples;
- fallback response;
- staff script;
- test cases.

Current mission deck:

1. Game Studio Mission.
2. Deepfake Detective / Truth Check.
3. Future Me Quest.
4. Study Coach: Help or Shortcut?
5. Reef Rescue Mission.
6. Squad Chat Moderator.

## Coding conventions

- Keep code simple and inspectable.
- Prefer boring, reliable dependencies.
- Prefer server-owned state over client-owned authority.
- Use environment variables for ports and hosts.
- Include tests for every new mission and every new model-output schema.
- Add or update docs when behaviour changes.
- Avoid large rewrites unless explicitly requested.

## Test expectations

Before marking a phase complete:

- run port checks;
- run unit tests;
- run smoke tests;
- confirm same-Wi-Fi phone mode starts with `APP_HOST=0.0.0.0` and prints a LAN `Phone URL`;
- confirm reset works;
- confirm fallback works;
- confirm visitor data can be cleared;
- confirm app starts on the assigned port;
- confirm `/screen`, `/`, `/staff`, `/health`, and `/replay` work.

## Agent behaviour

When asked to implement work:

1. Read `README.md`, this file, and the relevant document in `docs/`.
2. Propose a short plan first.
3. Make the smallest useful change.
4. Add or update tests.
5. Do not introduce new dependencies without explaining why.
6. Do not change the public demo thesis without updating `docs/PROJECT_BRIEF.md` and `docs/RESPONSIBLE_AI_DESIGN.md`.
7. Report changed files and test results.

Keep agent instructions concise. Put detailed design notes in `docs/`, not in this file.
