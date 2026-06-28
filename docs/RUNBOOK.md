# Runbook

## Local development startup

```bash
python3 -m pip install -r requirements.txt
./scripts/check_ports.sh
./scripts/start_dev.sh
```

PowerShell:

```powershell
python3 -m pip install -r requirements.txt
pwsh -NoProfile -File scripts/check_ports.ps1
pwsh -NoProfile -File scripts/start_dev.ps1
```

The start script launches the local FastAPI server on `127.0.0.1:3200` by default. This is laptop-only mode; it is good for route checks from the demo machine, but phones cannot reach `127.0.0.1` on the laptop.

A `.env` file is optional. Use one only when you want persistent local overrides. One-off command-line values such as `APP_HOST=0.0.0.0` are preferred for rehearsal checks.

If startup uses Xcode Python and fails with `No module named uvicorn`, pin the interpreter in `.env`:

```text
PYTHON_BIN=/Users/cpjjh/.pyenv/versions/3.12.13/bin/python3
```

With the app running, verify routes:

```bash
./scripts/smoke_test.sh
```

PowerShell:

```powershell
pwsh -NoProfile -File scripts/smoke_test.ps1
```

The smoke test includes `/qr.svg`, which should return a local SVG QR code for the visitor controller.

## Same-Wi-Fi phone startup

For phone testing on the same Wi-Fi, the server must bind to all network interfaces:

```bash
APP_HOST=0.0.0.0 ./scripts/start_dev.sh
```

PowerShell:

```powershell
$env:APP_HOST = "0.0.0.0"
pwsh -NoProfile -File scripts/start_dev.ps1
```

The script prints the local laptop URL and the phone URL:

```text
Laptop URL: http://127.0.0.1:3200/
Phone URL:  http://192.168.0.136:3200/
```

Open the printed `Phone URL` on the phone. Do not use `127.0.0.1` on the phone.

The QR code displayed on `/screen` and `/staff` points to the same visitor controller URL for the host used to load the page. For booth use, open `/screen` with the laptop LAN address, for example `http://192.168.0.136:3200/screen`, so the QR code resolves to a phone-reachable address.

## Rehearsal startup

1. Boot the demo machine.
2. Confirm display and power settings.
3. Confirm local network/router path.
4. Confirm the machine IP address.
5. Run `./scripts/check_ports.sh` or `pwsh -NoProfile -File scripts/check_ports.ps1`.
6. Start the app with `APP_HOST=0.0.0.0 ./scripts/start_dev.sh`, or set `$env:APP_HOST = "0.0.0.0"` before `pwsh -NoProfile -File scripts/start_dev.ps1`.
7. Confirm the console prints a `Phone URL` using the demo machine LAN address.
8. Open `/screen` on the big display using the LAN host URL.
9. Open `/staff` on staff machine/browser.
10. Scan the `/screen` QR code from iPhone and Android.
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
| Phone cannot join | Confirm app was started with `APP_HOST=0.0.0.0`, use printed `Phone URL`, load `/screen` by LAN URL, check Wi-Fi/router isolation | Staff-controlled mode |
| QR opens laptop-only URL | Reopen `/screen` using the LAN host, not `127.0.0.1` | Printed phone URL |
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
