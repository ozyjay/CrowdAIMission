# MVP Status

## Current phase

**MVP 0.2 — Real Round Loop**

## Completed

### Framework Desktop / iPhone round-loop test

Status: **Core physical loop passed on 24 July 2026**

What has been proven:

- the Framework Desktop running Fedora can host the offline `CrowdAI` Wi-Fi;
- an iPhone can join using the generated Wi-Fi credentials;
- the app is reachable from the hotspot on fixed port `3200`;
- visitor voting updates the shared server state and big-screen view;
- a complete goal, rule, proposal/check, crowd-decision, result, reset, and
  fallback/replay flow works over the hotspot.

### MVP 0.1 — Local phone smoke test

Status: **Prototype smoke test passed**

What has been proven:

- the basic app/server can run locally;
- a mobile phone can connect to the app over the local network while it is running on a Mac;
- the QR / phone-to-screen foundation is viable enough to continue.

## Not yet proven

The MVP is not Open Day ready yet. The following remain unproven:

- Android phone testing;
- multiple phones connected simultaneously;
- big-screen `/screen` tested on TV or external display;
- staff `/staff` controls tested by someone other than the developer;
- local router / event network path tested;
- 60-minute or 2–3 hour burn-in;
- no-phone replay/fallback mode tested under crowd conditions.

## MVP 0.2 implementation progress

Implemented and locally verified through 24 July 2026:

- server-owned goal, rule, and crowd-decision voting;
- WebSocket state broadcasts with polling fallback;
- `/api/missions` and the required public routes on fixed port `3200`;
- separate staff controls for advance, clear votes, round reset, session clear,
  fallback, replay, and return to live mode;
- visible goal, rule, decision, and result summaries on `/screen` and `/staff`;
- deterministic Game Studio, Truth Check, and Future Me Quest mission packs;
- 36 automated tests collected, with 23 focused non-route tests passing in the
  current development environment;
- shell smoke test passing for the MVP 0.2 GET route set.

The in-process FastAPI route client currently stalls under the active Python
3.14 environment. Live route behaviour passed on the Framework/iPhone setup,
and the three-mission API result was checked directly; the route-test harness
still needs separate repair before a clean full-suite result can be recorded.

This is local software verification only. The device, display, network, operator,
and burn-in proof points below still require manual testing.

## MVP 0.2 target

MVP 0.2 should add the first meaningful interaction loop without a live AI dependency:

```text
phone vote → server state → screen update → staff reset/fallback
```

The local-AI proposal is deterministic in this phase.

## Status labels

| Phase | Status | Notes |
|---|---|---|
| MVP 0.1 — route / LAN smoke test | Passed | Phone connected to local Mac-hosted app |
| MVP 0.2 — real round loop | In progress | Core loop passed on Framework/iPhone; Android, multi-phone, display, and burn-in rehearsals remain |
| MVP 0.3 — mission deck hardening | Not started | Add more missions and stronger tests |
| MVP 0.4 — local SLM adapter | Deferred | Only after deterministic loop is reliable |
| MVP 0.5 — rehearsal hardening | Deferred | Multi-phone, router, Framework/Fedora, burn-in |

## Next action

Run Future Me Quest on the iPhone, then test Android, multiple simultaneous
phones, an external display, and a 60-minute burn-in.
