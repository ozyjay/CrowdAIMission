# Runbook — MVP 0.2

## Goal

Run the local round-loop demo with minimal live debugging.

## Start sequence

### 1. Configure environment

```bash
cp .env.example .env
```

For local-only desktop testing:

```env
APP_HOST=127.0.0.1
APP_PORT=3200
PUBLIC_DEMO_URL=
```

For phone testing on the same local network:

```env
APP_HOST=0.0.0.0
APP_PORT=3200
PUBLIC_DEMO_URL=
```

Do not hardcode the LAN URL in `.env` for normal demos. The start script prints the current `Phone URL`. When `APP_HOST=0.0.0.0`, the QR code rewrites localhost to the laptop LAN address so phones do not try to open `localhost`.

### 2. Check ports

```bash
./scripts/check_ports.sh
```

### 3. Start app

```bash
./scripts/start_dev.sh
```

### 4. Open routes

Desktop:

```text
http://127.0.0.1:3200/screen
http://127.0.0.1:3200/staff
```

Phone:

```text
Use the Phone URL printed by the start script.
```

### Offline Framework Desktop hotspot

On Fedora or another Linux system using NetworkManager, the Desktop can host
the demo network without Ethernet or internet access:

```bash
./scripts/manage_hotspot.sh start
APP_HOST=0.0.0.0 ./scripts/start_dev.sh
```

The first start generates a strong WPA password and saves it in a NetworkManager
profile. It then shows a terminal QR code, which visitors can scan to
join the Wi-Fi without typing the password. The hotspot uses 2.4 GHz for broad
phone compatibility. Starting it disconnects any Wi-Fi network currently using
that adapter; the script asks for confirmation before doing so.

Useful commands:

```bash
./scripts/manage_hotspot.sh status
./scripts/manage_hotspot.sh qr
./scripts/manage_hotspot.sh restart
./scripts/manage_hotspot.sh stop
```

Configuration can be supplied with environment variables:

```bash
HOTSPOT_SSID=CrowdAI \
HOTSPOT_INTERFACE=wlp1s0 \
./scripts/manage_hotspot.sh start
```

`HOTSPOT_NAME`, `HOTSPOT_SSID`, `HOTSPOT_INTERFACE`, `HOTSPOT_PASSWORD`, and
`APP_PORT` are supported. Normally, leave `HOTSPOT_PASSWORD` unset and let the
script generate it. If a fixed override is necessary, avoid putting it in
`.env` or shell history.

Phones may warn that the network has no internet. Choose to remain connected.
Disable VPNs and mobile-data auto-switching if a phone cannot open the printed
URL. If Fedora's firewall blocks the app, allow TCP port `3200` only on the
hotspot's NetworkManager/firewalld zone rather than disabling the firewall.

The Wi-Fi QR code joins the hotspot only. After joining, visitors open the
separate phone URL printed by the script, normally `http://10.42.0.1:3200/`.

If interrupted starts have created more than one `CrowdAI-Hotspot` profile,
the next `start` keeps the active or most recently used profile and renames the
others with a `-duplicate-<uuid>` suffix. This preserves their settings while
removing NetworkManager's ambiguous-name warnings.

### 5. Smoke test

In another terminal:

```bash
./scripts/smoke_test.sh
```

## Staff operating flow

1. Open `/staff`.
2. Select mission.
3. Start round.
4. Watch phone votes arrive.
5. Advance phase if manual advancement is enabled.
6. Reset round when complete.
7. Switch to fallback/replay if phones fail.

## Standard reset

Use this whenever the screen becomes stale or confusing:

1. Press **Reset round** in `/staff`.
2. Confirm votes are cleared.
3. Confirm `/screen` returns to mission start.
4. Invite visitors to vote again.

## Standard fallback

Use if phones cannot connect or voting breaks:

1. Press **Fallback** or **Replay** in `/staff`.
2. Keep the big screen running a prepared loop.
3. Use public wording:

> “Live voting is unavailable right now, so we’re showing a prepared demo run. It shows the same idea in a reliable way.”

Avoid:

> “The AI crashed.”

## MVP 0.2 public explanation

Use:

> “Scan in and vote. The crowd sets the goal, the local AI proposal is checked by software rules, and people decide whether to use, repair, or reject it.”

If using deterministic proposals in MVP 0.2, say internally or in dev demos:

> “This MVP uses prepared proposals so we can test the interaction before adding a live local model.”

## Troubleshooting

| Problem | First action | Fallback |
|---|---|---|
| Phone cannot open URL | Open `http://<phone-url-host>:3200/ping` on the phone. If it does not show `pong`, check Wi-Fi, guest network/client isolation, VPN, and firewall. | Use `/replay` |
| Phone opens but vote fails | Check `/api/state` and `/api/vote` | Use staff-controlled round |
| Screen does not update | Refresh `/screen`; check WebSocket/polling | Use `/replay` |
| Staff route broken | Restart app when visitor flow allows | Use static replay route |
| Port conflict | Stop conflicting process; do not randomise port | Delay live mode |
| Mission state messy | Reset round/session | Switch mission or replay |

## Shutdown

1. Stop dev server.
2. Clear temporary state if needed.
3. Record test results.
4. Note device/browser/network issues.

## Test notes to capture

- date/time;
- host machine;
- LAN IP;
- phone model/browser;
- route tested;
- whether vote updated screen;
- whether staff reset worked;
- whether fallback worked;
- any latency or connection issues.
