# Runbook

## Local development startup

```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
./scripts/check_ports.sh
./scripts/start_dev.sh
```

The start script launches the local FastAPI server on port `3200` unless `APP_HOST` or `APP_PORT` are deliberately changed in `.env`.

With the app running, verify routes:

```bash
./scripts/smoke_test.sh
```

For phone testing on the same Wi-Fi, start the app with:

```bash
APP_HOST=0.0.0.0 ./scripts/start_dev.sh
```

Then open the visitor controller on the phone using the demo machine LAN address, for example `http://192.168.0.136:3200/`.

## Rehearsal startup

1. Boot the demo machine.
2. Confirm display and power settings.
3. Confirm local network/router path.
4. Confirm the machine IP address.
5. Update `PUBLIC_DEMO_URL` in `.env` if needed.
6. Run `./scripts/check_ports.sh`.
7. Start the app.
8. Open `/screen` on the big display.
9. Open `/staff` on staff machine/browser.
10. Test `/` from iPhone and Android.
11. Run one mission round.
12. Trigger reset.
13. Trigger replay/fallback.

## Staff operation

Use the staff page to:

- select mission;
- start/close round;
- force next phase;
- reset current mission;
- clear visitor state;
- turn model mode on/off;
- show replay mode;
- show health status.

## Standard visitor explanation

> Scan the QR code and vote. The crowd sets the goal, the local AI proposes what to do, and the system checks whether it stayed on track. If it goes wrong, people can repair or reject it.

## Standard fallback wording

> Live mode is unavailable right now, so we’re showing a prepared mission run. It shows the same idea in a reliable way.

## Troubleshooting

| Problem | First action | Fallback |
|---|---|---|
| Phone cannot join | Check URL/IP and router | Staff-controlled mode |
| Phone joins but vote fails | Check `/health`, reload phone route | Replay mode |
| Screen does not update | Refresh `/screen`, check WebSocket | Polling or replay |
| Model times out | Disable model mode | Deterministic templates |
| Bad model output | Use validator fallback | Canned repair |
| Inappropriate output | Reset immediately | Replay mode |
| Port conflict | Stop and run port check | Do not randomise port |

## Shutdown

1. Switch screen to safe ending or replay slide.
2. Stop local services.
3. Clear visitor state.
4. Save any non-identifying event notes.
5. Shut down machine and router.
