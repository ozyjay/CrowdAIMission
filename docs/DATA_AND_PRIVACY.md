# Data and Privacy

## Default position

Do not collect personal information.

For MVP 0.2:

- no login;
- no app install;
- no names;
- no email addresses;
- no phone numbers;
- no open visitor free text;
- no visitor audio;
- no visitor video;
- no persistent visitor profiles.

## What may be stored in memory

MVP 0.2 may keep transient in-memory state:

- mission id;
- round id;
- current phase;
- vote counts;
- deterministic proposal id;
- validation check labels;
- current mode: live/fallback/replay.

This should clear on reset or server restart.

## Logs

Logs should be technical and non-identifying.

Allowed examples:

```text
phase changed: vote_rule -> proposal
mission selected: game-studio
vote accepted: phase=vote_goal option=escape_reef_lab
fallback enabled
```

Avoid logging:

- IP addresses unless required for debugging and removed before public use;
- device identifiers;
- user agent strings unless required temporarily for cross-device debugging;
- raw visitor text;
- any personal details.

## Phone sessions

For MVP 0.2, a simple anonymous browser session is acceptable if needed for duplicate-vote limiting.

Keep it non-identifying:

- random session token;
- no account;
- no name;
- no long-term persistence.

Duplicate-vote limiting is optional for MVP 0.2.

## Staff route

Do not expose `/staff` as a visitor-facing QR target.

For local rehearsal, staff route may be protected by physical/network controls. Before public deployment, decide whether a simple PIN or local-only restriction is needed.

## Reset requirements

Reset must clear:

- current votes;
- chosen goal/rule;
- proposal;
- checks;
- crowd decision;
- public result text if inappropriate or stale.

## Public sign text

Suggested QR sign:

> Scan to control the shared demo. No login is required. Please do not enter personal information.

Since MVP 0.2 has no free text, this should be easy to satisfy.
