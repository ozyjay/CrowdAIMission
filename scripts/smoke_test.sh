#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

APP_PORT="${APP_PORT:-3200}"
BASE_URL="http://127.0.0.1:${APP_PORT}"

required_paths=(
  "/"
  "/ping"
  "/screen"
  "/staff"
  "/health"
  "/replay"
  "/api/state"
  "/api/missions"
  "/qr.svg"
)

for path in "${required_paths[@]}"; do
  url="${BASE_URL}${path}"
  echo "Checking ${url}"
  if ! curl -fsS --max-time 2 "$url" >/dev/null; then
    echo "Smoke test failed for ${url}"
    echo "Start the app first with ./scripts/start_dev.sh or update this script if route names changed."
    exit 1
  fi
done

echo "Smoke test passed for MVP 0.2 route set."
