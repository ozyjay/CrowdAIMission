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

for path in / /screen /staff /health /replay /qr.svg; do
  url="${BASE_URL}${path}"
  echo "Checking ${url}"
  if ! curl -fsS --max-time 2 "$url" >/dev/null; then
    echo "Smoke test failed for ${url}"
    exit 1
  fi
done

echo "Smoke test passed."
