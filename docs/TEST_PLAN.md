# Test Plan

## Test categories

| Test type | Purpose |
|---|---|
| Unit tests | Validate mission definitions, schemas, and rule checks |
| Route tests | Confirm `/`, `/screen`, `/staff`, `/health`, `/replay` respond |
| Voting tests | Confirm votes aggregate and rounds advance correctly |
| WebSocket tests | Confirm screen updates after votes |
| Mission tests | Confirm each mission has safe success and failure examples |
| Model tests | Confirm malformed, unsafe, slow, and unsupported outputs fall back |
| Privacy tests | Confirm no personal fields are required or stored |
| Rehearsal tests | Confirm phones, QR, display, reset, and fallback work in booth conditions |

## MVP acceptance criteria

- [ ] App starts on port `3200`.
- [ ] `/` opens on phone-sized screen.
- [ ] `/screen` shows public mission state.
- [ ] `/staff` can select mission, reset, and fallback.
- [ ] `/health` returns healthy status.
- [ ] At least two missions run without AI dependency.
- [ ] Votes update the big screen.
- [ ] Staff reset clears current state.
- [ ] Replay mode works without model or phones.
- [ ] No login, app install, or personal data collection.
- [ ] No unsupervised visitor free text.

## QR readiness gate

- [ ] QR code opens on iPhone.
- [ ] QR code opens on Android.
- [ ] No login required.
- [ ] No app install required.
- [ ] New phone can join and vote in under 10 seconds.
- [ ] At least 10 test phones can connect during rehearsal.
- [ ] Big screen updates reliably.
- [ ] Staff can switch to no-phone fallback.

## Mission regression matrix

| Mission | Success case | Safe failure | Expected repair |
|---|---|---|---|
| Game Studio | Gives hint without answer | Spoils puzzle | Convert answer to hint |
| Truth Check | Flags unsupported claim | Invents event/course detail | Ask staff / neutral wording |
| Future Me | Creates useful questions | Overconfident career prediction | Offer options and questions |
| Study Coach | Explains concept | Writes final answer | Ask guiding question |
| Reef Rescue | Follows coral rule | Crosses coral | Safer route |
| Squad Chat | Allows constructive feedback | Blocks harmless message or allows toxic one | Adjust verdict/escalate |

## Model-output tests

Test that each of these falls back safely:

- invalid JSON;
- unknown action;
- unknown asset;
- unsupported factual claim;
- unsafe content;
- response too long;
- model timeout;
- empty response;
- model unavailable;
- WebSocket unavailable.

## Go/no-go for Open Day

The demo is not Open Day ready until:

- it runs for at least 60 minutes without restart;
- staff can reset in under 30 seconds;
- staff can switch to fallback in under 30 seconds;
- a non-developer can start it from cold boot;
- QR onboarding passes rehearsal;
- all active routes use the documented ports;
- all mission content has been reviewed for safety and public wording.
