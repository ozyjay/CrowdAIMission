# Codex / Coding-Agent Prompts

Use these prompts one phase at a time. Do not ask for all phases in one prompt.

## Phase 0 — Plan and scaffold

```text
Read README.md, AGENTS.md, docs/PROJECT_BRIEF.md, docs/UX_SPEC.md, and docs/ARCHITECTURE.md.

Create a short implementation plan for the MVP of Crowd AI Mission Control. Do not code yet. The MVP must run locally, use port 3200, provide /, /screen, /staff, /health, and /replay routes, and work without any AI model dependency.

Keep dependencies minimal. Include proposed file changes, tests, and fallback behaviour.
```

## Phase 1 — Static routes

```text
Implement the smallest working local app with static routes: /, /screen, /staff, /health, and /replay. Do not add model calls. Do not add open visitor text. Use port 3200 from environment variables.

Add tests or a smoke test that verifies each route responds. Update README if launch commands change.
```

## Phase 2 — Voting loop

```text
Add a simple voting round state machine for one mission. Visitor phones submit button votes. The screen shows current mission, current vote, and result. Staff can reset the round.

Keep all state server-owned. Add tests for vote counting and reset.
```

## Phase 3 — Mission deck

```text
Add mission definitions for Game Studio Mission and Deepfake Detective / Truth Check using docs/MISSION_DECK.md. Each mission must include goals, rules, check options, safe failure examples, and fallback responses.

Do not add local AI yet. Use deterministic proposals. Add mission tests.
```

## Phase 4 — Big-screen control pipeline

```text
Update /screen to show the visible control pipeline: PEOPLE SET THE GOAL, PEOPLE SET THE RULE, LOCAL AI PROPOSED, SOFTWARE CHECKED, CROWD DECIDED, MISSION UPDATED.

This must show external controller state only, not private model reasoning. Add a replay/fallback display state.
```

## Phase 5 — Validation pipeline

```text
Implement proposal validation: schema validity, action whitelist, asset whitelist, intent match, rule check, evidence-needed flag, and safety status. Model output is still optional; deterministic proposals must pass through the same validator.

Add tests for invalid JSON, unknown action, unknown asset, rule failure, unsupported factual claim, and fallback.
```

## Phase 6 — Optional local SLM adapter

```text
Add a local SLM adapter behind a feature flag. The app must still work with MODEL_ENABLED=false. Model calls must timeout quickly and fall back to deterministic templates. The model may only propose structured JSON matching the approved proposal schema.

Do not let model output publish directly. Add tests for timeout, malformed output, and safe fallback.
```

## Phase 7 — Staff and rehearsal hardening

```text
Improve /staff with mission select, reset, clear state, show fallback, model on/off, and health status. Add or update scripts/check_ports.sh and scripts/smoke_test.sh so a staff member can verify the demo before rehearsal.

Update docs/RUNBOOK.md with final launch and recovery steps.
```

## Phase 8 — Polish and go/no-go

```text
Review the app against docs/TEST_PLAN.md and AGENTS.md. Fix any public-demo readiness gaps. Ensure no login, no personal data collection, no unsupervised free text, fixed ports, working fallback, and clear reset.

Return changed files and test results.
```
