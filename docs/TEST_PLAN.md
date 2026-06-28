# Test Plan — MVP 0.2

## Purpose

MVP 0.2 testing should prove the real round loop works before adding live AI.

The key question is:

> Can a phone vote through a mission, update the big screen, and can staff reset/fallback without developer intervention?

## Test levels

| Level | Purpose |
|---|---|
| Static route smoke tests | Confirm required routes respond |
| API tests | Confirm state, mission list, vote, reset, mode, and advance work |
| State-machine tests | Confirm phase transitions and reset behaviour |
| Mission tests | Confirm each mission has valid goals, rules, proposals, checks, fallback |
| Manual LAN test | Confirm phone can connect and vote |
| Staff test | Confirm non-developer can operate reset/fallback |
| Screen test | Confirm big-screen readability and updates |

## MVP 0.1 regression

Repeat the proven test:

- start app on Mac;
- connect phone over local network;
- open visitor route;
- confirm phone can interact.

## Required route smoke test

`./scripts/smoke_test.sh` should check:

- `/`
- `/screen`
- `/staff`
- `/replay`
- `/health`
- `/api/state`
- `/api/missions`

## API tests

### `/api/state`

- returns JSON;
- includes mode, mission id, phase, round id;
- does not include personal data.

### `/api/missions`

- returns enabled missions;
- includes Game Studio, Deepfake Detective, Future Me Quest;
- mission ids are stable.

### `/api/vote`

- accepts valid vote for current phase;
- rejects unknown option id;
- rejects vote for wrong phase;
- updates vote count;
- triggers screen/staff update.

### `/api/staff/reset`

- clears votes;
- clears proposal/checks/result;
- preserves or resets mission depending on scope;
- broadcasts update.

### `/api/staff/mission`

- accepts known mission id;
- rejects unknown mission id;
- resets round to idle or vote_goal.

### `/api/staff/mode`

- supports live, fallback, replay;
- rejects unknown mode.

## State-machine tests

Test transitions:

```text
idle -> vote_goal -> vote_rule -> proposal -> checks -> crowd_decision -> result
```

Test staff overrides:

```text
any phase -> fallback
any phase -> replay
any phase -> reset
```

## Mission tests

Each MVP 0.2 mission must have:

- at least 3 goal options;
- at least 3 rule options;
- at least 1 deterministic proposal;
- at least 1 safe failure example;
- at least 1 fallback result;
- check outcomes for intent, rule, evidence, safety;
- staff script.

## Manual test script

1. Start app on port `3200`.
2. Open `/screen` on desktop.
3. Open `/staff` on desktop.
4. Open `/` on phone using LAN IP.
5. Select **Game Studio Mission** in staff panel.
6. Start round.
7. Vote goal from phone.
8. Advance to rule vote.
9. Vote rule from phone.
10. Advance to proposal/check.
11. Confirm deterministic proposal and checks show on screen.
12. Vote crowd decision from phone.
13. Confirm result shows on screen.
14. Reset from staff route.
15. Repeat for Deepfake Detective and Future Me Quest.
16. Trigger fallback.
17. Trigger replay.
18. Confirm smoke test still passes.

## Multi-device test

MVP 0.2 target:

- one phone minimum;
- two phones preferred;
- iPhone + Android if available.

Later rehearsal target:

- 5 phones;
- then 10 phones;
- then local router / Framework Desktop.

## Big-screen readability test

Check:

- readable from 2–3 metres;
- active phase obvious;
- crowd choice obvious;
- checks visible but not too text-heavy;
- result visible;
- fallback message clear.

## Privacy test

Confirm:

- no login;
- no names;
- no email;
- no phone number;
- no free text;
- no persistent visitor profile;
- reset clears visible visitor state.

## MVP 0.2 go/no-go

Go if:

- route and API smoke tests pass;
- three mission rounds work;
- phone vote updates screen;
- staff reset and fallback work;
- no AI dependency is required;
- no personal data is collected.

No-go if:

- phone cannot vote reliably;
- screen does not update;
- staff cannot reset;
- fallback/replay does not work;
- free text or personal data is required;
- app chooses random ports.
