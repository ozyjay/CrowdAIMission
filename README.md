# Crowd AI Mission Control

**Public title:** Humans in the Loop  
**Hook:** Can the crowd keep a local AI on track?  
**Current phase:** MVP 0.2 — Real Round Loop

Crowd AI Mission Control is a QR phone-to-screen Open Day demo. Visitors scan a QR code, vote through short mission rounds, watch a local-AI-style proposal, and help decide whether it is on track, needs repair, needs evidence, needs a human, or should fall back to a safe response.

The demo is not about “AI taking over.” It is about how IT systems keep people involved, informed, and in control.

## Current status

MVP 0.1 smoke test is complete:

- the basic app/server ran locally;
- a mobile phone could connect to it over the local network while it was running on a Mac;
- the project is ready to move from route smoke test to real round-loop behaviour.

This does **not** yet prove Open Day readiness. The remaining proof points are: iPhone + Android, 5–10 phones, big-screen `/screen`, staff reset/fallback, local-router testing, and Framework Desktop / Fedora 43 validation.

## MVP 0.2 goal

Build the first useful no-AI round loop.

MVP 0.2 must show:

```text
Crowd sets a goal
→ crowd sets a rule
→ deterministic local-AI-style proposal appears
→ software checks intent, schema, rule, evidence, and safety
→ crowd/staff accept, repair, reject, ask for evidence, ask a human, or fall back
→ big screen updates
```

The MVP 0.2 proposal generator should be deterministic. Do **not** add live SLM calls yet.

## Required MVP 0.2 routes

| Route | Purpose | MVP 0.2 requirement |
|---|---|---|
| `/` | Visitor phone controller | Shows current mission and current vote options only |
| `/screen` | Big-screen display | Shows mission state and visible control pipeline |
| `/staff` | Staff controls | Select mission, reset, clear votes, force fallback/replay |
| `/replay` | No-phone fallback | Runs a prepared demo sequence without phones |
| `/health` | Health/status check | Returns service status and basic state |
| `/api/state` | Machine-readable state | Returns current round/session state |
| `/api/missions` | Mission list | Returns enabled mission metadata |
| `/api/vote` | Submit vote | Accepts tap-based votes only |
| `/ws` | Live updates | Pushes state updates to screen/staff/phones, if implemented |

Polling is acceptable as a temporary fallback if WebSockets are not stable yet.

## Default ports

| Service | Port |
|---|---:|
| Single-app MVP | `3200` |
| QR backend/WebSocket, if split later | `8200` |
| Shared model adapter, if used later | `8600` |
| Replay service, if split later | `8700` |
| Health/status, if split later | `8800` |

Use fixed ports. Do not silently fall back to random ports in Open Day mode.

## MVP 0.2 mission deck

Build these first:

1. **Game Studio Mission** — can the crowd keep an NPC/game helper useful without spoiling the game?
2. **Deepfake Detective / Truth Check** — can the crowd catch unsupported AI claims?
3. **Future Me Quest** — can the AI turn interests into better Open Day questions without overclaiming?

Keep these as next mission packs:

4. **Study Coach: Help or Shortcut?**
5. **Reef Rescue Mission**
6. **Squad Chat Moderator**

See `docs/MISSION_DECK.md` for content details.

## Suggested stack

For MVP 0.2, keep the simplest reliable stack:

- Python + FastAPI for the local server;
- static HTML/CSS/JS for visitor, screen, and staff routes;
- WebSockets for live updates, or short polling if that is simpler;
- in-memory server-owned state;
- deterministic proposal templates;
- no live SLM dependency.

A richer frontend can be added after the interaction model is proven.

## Local setup

```bash
cp .env.example .env
./scripts/check_ports.sh
./scripts/start_dev.sh
```

In a separate terminal:

```bash
./scripts/smoke_test.sh
```

For phone testing on a local network, bind the app to all interfaces:

```bash
APP_HOST=0.0.0.0 ./scripts/start_dev.sh
```

The script prints the current `Phone URL`. Open that URL on the phone, or scan the QR code on `/screen` or `/staff`. When `APP_HOST=0.0.0.0`, the QR code rewrites localhost to the laptop LAN address so phones do not try to open `localhost`. Do not hardcode `PUBLIC_DEMO_URL` for normal local demos.

On a Linux host using NetworkManager, the Framework Desktop can provide an
offline 2.4 GHz hotspot without Ethernet:

```bash
./scripts/manage_hotspot.sh start
APP_HOST=0.0.0.0 ./scripts/start_dev.sh
```

The hotspot script prints the phone URL. Use `status`, `stop`, or `restart` as
the first argument to manage it. See `docs/RUNBOOK.md` for configuration and
rehearsal notes.

## Documentation map

| File | Purpose |
|---|---|
| `AGENTS.md` | Coding-agent instructions and non-negotiable demo rules |
| `docs/MVP_STATUS.md` | Current prototype status and what has/has not been proven |
| `docs/MVP_0_2_PLAN.md` | Scope, deliverables, go/no-go tests for MVP 0.2 |
| `docs/PROJECT_BRIEF.md` | Demo thesis, audience, and Open Day story |
| `docs/MISSION_DECK.md` | Mission concepts and phone/screen UX examples |
| `docs/UX_SPEC.md` | Visitor, screen, staff, and replay UX structure |
| `docs/ARCHITECTURE.md` | Components, routes, state model, and validation pipeline |
| `docs/API_CONTRACT.md` | MVP 0.2 route and payload contract |
| `docs/RESPONSIBLE_AI_DESIGN.md` | Research-backed responsible AI design rules |
| `docs/DATA_AND_PRIVACY.md` | Visitor privacy and data-handling defaults |
| `docs/TEST_PLAN.md` | Unit, integration, rehearsal, and go/no-go tests |
| `docs/RUNBOOK.md` | Local startup, reset, fallback, and shutdown |
| `docs/CODEX_PROMPTS.md` | Prompts for phased AI-assisted implementation |
| `docs/RESEARCH_NOTES.md` | Literature anchors and design implications |
| `docs/CHANGELOG.md` | Documentation and project status changes |
| `docs/DOC_INDEX.md` | Suggested reading order |

## Definition of done for MVP 0.2

- `/`, `/screen`, `/staff`, `/replay`, `/health`, `/api/state`, `/api/missions`, and `/api/vote` work on port `3200`.
- A phone can open `/` and submit votes.
- `/screen` visibly updates from phone input.
- `/staff` can select mission, reset round/session, clear votes, and trigger fallback/replay.
- At least three deterministic mission packs work: Game Studio, Deepfake Detective, and Future Me Quest.
- Each mission supports goal vote, rule vote, proposal, checks, crowd decision, and result.
- No live model dependency is required.
- No login, app install, personal data, or unsupervised free text is required.
- Smoke tests pass.
- The Mac LAN test is repeated after the MVP 0.2 changes.
