# MVP Status

## Current phase

**MVP 0.2 — Real Round Loop**

## Completed

### MVP 0.1 — Local phone smoke test

Status: **Prototype smoke test passed**

What has been proven:

- the basic app/server can run locally;
- a mobile phone can connect to the app over the local network while it is running on a Mac;
- the QR / phone-to-screen foundation is viable enough to continue.

## Not yet proven

The MVP is not Open Day ready yet. The following remain unproven:

- iPhone and Android both tested;
- multiple phones connected simultaneously;
- big-screen `/screen` tested on TV or external display;
- staff `/staff` controls tested by someone other than the developer;
- local router / event network path tested;
- Framework Desktop / Fedora 43 event image tested;
- 60-minute or 2–3 hour burn-in;
- no-phone replay/fallback mode tested under crowd conditions.

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
| MVP 0.2 — real round loop | Next | Build voting, state, screen, staff reset, replay |
| MVP 0.3 — mission deck hardening | Not started | Add more missions and stronger tests |
| MVP 0.4 — local SLM adapter | Deferred | Only after deterministic loop is reliable |
| MVP 0.5 — rehearsal hardening | Deferred | Multi-phone, router, Framework/Fedora, burn-in |

## Next action

Implement MVP 0.2 using `docs/MVP_0_2_PLAN.md`.
