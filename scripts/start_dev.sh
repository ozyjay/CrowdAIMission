#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

APP_HOST="${APP_HOST:-127.0.0.1}"
APP_PORT="${APP_PORT:-3200}"

if [ -f "app/main.py" ]; then
  echo "Starting FastAPI app on ${APP_HOST}:${APP_PORT}"
  exec python -m uvicorn app.main:app --host "${APP_HOST}" --port "${APP_PORT}" --reload
fi

if [ -f "main.py" ]; then
  echo "Starting FastAPI app on ${APP_HOST}:${APP_PORT}"
  exec python -m uvicorn main:app --host "${APP_HOST}" --port "${APP_PORT}" --reload
fi

if [ -f "package.json" ]; then
  echo "package.json found. Running npm dev script. Ensure it respects APP_PORT=${APP_PORT}."
  exec npm run dev
fi

echo "No recognised app entrypoint found."
echo "Expected one of: app/main.py, main.py, package.json."
echo "Create the MVP app scaffold, then rerun this script."
exit 1
