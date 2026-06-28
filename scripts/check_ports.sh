#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

APP_PORT="${APP_PORT:-3200}"

if command -v lsof >/dev/null 2>&1; then
  if lsof -iTCP:"${APP_PORT}" -sTCP:LISTEN -n -P >/dev/null 2>&1; then
    echo "Port ${APP_PORT} is already in use."
    lsof -iTCP:"${APP_PORT}" -sTCP:LISTEN -n -P || true
    echo "Stop the process or change APP_PORT deliberately. Do not use random fallback ports for Open Day mode."
    exit 1
  fi
elif command -v ss >/dev/null 2>&1; then
  if ss -ltn | awk '{print $4}' | grep -Eq ":${APP_PORT}$"; then
    echo "Port ${APP_PORT} is already in use."
    ss -ltnp | grep -E ":${APP_PORT}\b" || true
    exit 1
  fi
else
  echo "No lsof or ss found; skipping port check."
fi

echo "Port ${APP_PORT} is available."
