# API Contract — MVP 0.2

This is the working route and payload contract for MVP 0.2.

## GET `/health`

Returns service health.

Example:

```json
{
  "ok": true,
  "service": "crowd-ai-mission-control",
  "phase": "vote_goal",
  "mission_id": "game-studio",
  "mode": "live"
}
```

## GET `/api/missions`

Returns enabled mission summaries.

Example:

```json
{
  "missions": [
    {
      "id": "game-studio",
      "title": "Game Studio Mission",
      "hook": "Can the crowd keep a game helper useful without spoiling the game?",
      "enabled": true
    }
  ]
}
```

## GET `/api/state`

Returns current public state.

Example:

```json
{
  "mode": "live",
  "mission_id": "game-studio",
  "mission_title": "Game Studio Mission",
  "round_id": 3,
  "phase": "vote_rule",
  "goal_choice_id": "escape_reef_lab",
  "rule_choice_id": null,
  "proposal": null,
  "checks": [],
  "crowd_decision_id": null,
  "vote_options": [
    {"id": "no_spoilers", "label": "Do not give away the answer"},
    {"id": "keep_fair", "label": "Keep it fair"}
  ],
  "votes": {
    "no_spoilers": 4,
    "keep_fair": 2
  }
}
```

## POST `/api/vote`

Submits a vote for the current phase.

Request:

```json
{
  "phase": "vote_rule",
  "option_id": "no_spoilers"
}
```

Response:

```json
{
  "ok": true,
  "accepted": true,
  "message": "Vote received. Watch the big screen."
}
```

Rules:

- Reject votes for the wrong phase.
- Reject unknown option ids.
- Do not require login.
- Do not collect names or phone numbers.
- Session-level duplicate limiting is optional for MVP 0.2.

## POST `/api/staff/mission`

Selects active mission.

Request:

```json
{
  "mission_id": "deepfake-detective"
}
```

Response:

```json
{
  "ok": true,
  "mission_id": "deepfake-detective",
  "phase": "idle"
}
```

## POST `/api/staff/reset`

Resets state.

Request:

```json
{
  "scope": "round"
}
```

Allowed scopes:

- `round`
- `session`

Response:

```json
{
  "ok": true,
  "scope": "round",
  "phase": "vote_goal"
}
```

## POST `/api/staff/mode`

Switches live/fallback/replay.

Request:

```json
{
  "mode": "fallback"
}
```

Allowed modes:

- `live`
- `fallback`
- `replay`

## POST `/api/staff/advance`

Manually advances to next phase.

Request:

```json
{}
```

Response:

```json
{
  "ok": true,
  "previous_phase": "vote_rule",
  "phase": "proposal"
}
```

## WebSocket `/ws`

Pushes state update events.

Example message:

```json
{
  "type": "state",
  "state": {
    "mode": "live",
    "mission_id": "game-studio",
    "phase": "crowd_decision"
  }
}
```

If WebSockets are unstable, the client can poll `/api/state` instead.

## Error response pattern

Use clear errors:

```json
{
  "ok": false,
  "error": "invalid_option",
  "message": "That option is not available for the current phase."
}
```

Recommended error codes:

- `invalid_phase`
- `invalid_option`
- `unknown_mission`
- `invalid_mode`
- `not_ready`
- `server_error`
