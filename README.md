# Crowd AI Mission Control

**Public title:** Humans in the Loop  
**Hook:** Can the crowd keep a local AI on track?

This is a QR phone-to-screen Open Day demo. Visitors scan a QR code, vote on a mission, watch a local AI propose an action, and help decide whether the proposal is on track, needs repair, needs evidence, or should fall back to a safe response.

The demo is not about “AI taking over.” It is about how IT systems keep people involved, informed, and in control.

## Core loop

```text
Crowd sets the goal
→ crowd sets the rule
→ local AI proposes
→ software checks intent, schema, evidence, and safety
→ crowd/staff accept, repair, reject, or fall back
→ big screen updates
```

## MVP routes

| Route | Purpose |
|---|---|
| `/` | Visitor phone controller |
| `/screen` | Big-screen display |
| `/staff` | Staff controls |
| `/api/vote` | Submit vote |
| `/ws` | Live updates |
| `/health` | Health/status check |
| `/replay` | Fallback/replay screen |

## Default ports

| Service | Port |
|---|---:|
| Single-app MVP | `3200` |
| QR backend/WebSocket, if split | `8200` |
| Shared model adapter, if used | `8600` |
| Replay service, if split | `8700` |
| Health/status, if split | `8800` |

## Mission deck

The highschool mission deck is:

1. **Game Studio Mission** — can the crowd keep an NPC/game helper useful without spoiling the game?
2. **Deepfake Detective / Truth Check** — can the crowd catch unsupported AI claims?
3. **Future Me Quest** — can the AI turn interests into better Open Day questions without overclaiming?
4. **Study Coach: Help or Shortcut?** — can the AI help learning without doing the thinking?
5. **Reef Rescue Mission** — can the crowd guide a reef robot while enforcing safety rules?
6. **Squad Chat Moderator** — can the AI help keep a game/community chat safe without overreacting?

See `docs/MISSION_DECK.md` for details.

## Suggested stack

For the MVP, use the simplest stack that can serve routes, state, and WebSockets reliably:

- Python + FastAPI for the local server;
- static HTML/CSS/JS for visitor, screen, and staff views;
- WebSockets for live updates, or polling as fallback;
- optional local SLM adapter only after deterministic missions work.

A Vite/React frontend can be added later if the UI becomes complex, but it is not required for the first proof of concept.

## Local setup

Install dependencies and check the fixed demo ports:

```bash
python3 -m pip install -r requirements.txt
./scripts/check_ports.sh
```

You do not need a `.env` file for normal local testing. Create one from `.env.example` only when you want persistent local overrides.

For laptop-only testing, start the app with the default localhost binding:

```bash
./scripts/start_dev.sh
```

This runs the MVP as a single FastAPI app on `127.0.0.1:3200`. Only the laptop can reach this address. After it starts, open:

- `http://127.0.0.1:3200/` for the visitor controller;
- `http://127.0.0.1:3200/screen` for the big screen;
- `http://127.0.0.1:3200/staff` for staff controls;
- `http://127.0.0.1:3200/replay` for fallback/replay mode.

Run `python3 -m pytest -q` for automated tests and `./scripts/smoke_test.sh` while the app is running for route smoke tests.

### Same-Wi-Fi phone testing

To test from a phone on the same Wi-Fi, start the app on all network interfaces:

```bash
APP_HOST=0.0.0.0 ./scripts/start_dev.sh
```

The script prints a `Phone URL`, for example:

```text
Phone URL:  http://192.168.0.136:3200/
```

Open that exact URL on the phone. Do not use `127.0.0.1` on the phone; on a phone, `127.0.0.1` means the phone itself, not the laptop.

If the phone cannot connect:

- confirm the laptop and phone are on the same non-guest Wi-Fi network;
- confirm any VPN, content filter, or router client-isolation setting is not blocking local traffic;
- on macOS, allow the terminal app, Codex, or Python in Local Network / incoming connection prompts if asked;
- confirm the console says `Starting Crowd AI Mission Control dev server on 0.0.0.0:3200.`

## Documentation map

| File | Purpose |
|---|---|
| `AGENTS.md` | Coding-agent instructions and non-negotiable demo rules |
| `docs/PROJECT_BRIEF.md` | Demo thesis, audience, and Open Day story |
| `docs/MISSION_DECK.md` | Mission concepts and phone/screen UX examples |
| `docs/UX_SPEC.md` | Visitor, screen, and staff UX structure |
| `docs/ARCHITECTURE.md` | Components, routes, state model, and validation pipeline |
| `docs/RESPONSIBLE_AI_DESIGN.md` | Research-backed responsible AI design rules |
| `docs/DATA_AND_PRIVACY.md` | Visitor privacy and data-handling defaults |
| `docs/TEST_PLAN.md` | Unit, integration, rehearsal, and go/no-go tests |
| `docs/RUNBOOK.md` | Local startup, reset, fallback, and shutdown |
| `docs/CODEX_PROMPTS.md` | Prompts for phased AI-assisted implementation |
| `docs/RESEARCH_NOTES.md` | Literature anchors and design implications |

## Definition of done for MVP

- A phone can open `/` and vote.
- `/screen` updates visibly from phone input.
- `/staff` can reset, select mission, and trigger fallback.
- The app runs on port `3200`.
- At least two missions work without AI dependency.
- The local SLM layer is optional and can be disabled.
- Every model-dependent action has deterministic fallback.
- No login, app install, personal data, or unsupervised free text is required.
