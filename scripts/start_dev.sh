#!/usr/bin/env bash
set -euo pipefail

ENV_APP_HOST="${APP_HOST:-}"
ENV_APP_PORT="${APP_PORT:-}"
ENV_APP_RELOAD="${APP_RELOAD:-}"
ENV_PYTHON_BIN="${PYTHON_BIN:-}"

if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [ -n "${ENV_APP_HOST}" ]; then
  APP_HOST="${ENV_APP_HOST}"
fi
if [ -n "${ENV_APP_PORT}" ]; then
  APP_PORT="${ENV_APP_PORT}"
fi
if [ -n "${ENV_APP_RELOAD}" ]; then
  APP_RELOAD="${ENV_APP_RELOAD}"
fi
if [ -n "${ENV_PYTHON_BIN}" ]; then
  PYTHON_BIN="${ENV_PYTHON_BIN}"
fi

APP_PORT="${APP_PORT:-3200}"
APP_HOST="${APP_HOST:-127.0.0.1}"
APP_RELOAD="${APP_RELOAD:-false}"
if [ -z "${PYTHON_BIN:-}" ]; then
  if [ -x ".venv/bin/python3" ]; then
    PYTHON_BIN=".venv/bin/python3"
  elif command -v pyenv >/dev/null 2>&1; then
    PYTHON_BIN="$(pyenv which python3)"
  else
    PYTHON_BIN="python3"
  fi
fi

LAN_IP="$({ ipconfig getifaddr en0 || ifconfig en0 | awk '/inet / {print $2; exit}'; } 2>/dev/null || true)"

echo "Starting Crowd AI Mission Control dev server on ${APP_HOST}:${APP_PORT}."
echo "Python: ${PYTHON_BIN}"
echo "Laptop URL: http://127.0.0.1:${APP_PORT}/"
if [ "${APP_HOST}" = "0.0.0.0" ] || [ "${APP_HOST}" = "${LAN_IP}" ]; then
  echo "Phone URL:  http://${LAN_IP:-<this-machine-LAN-IP>}:${APP_PORT}/"
else
  echo "Phone URL:  unavailable while APP_HOST=${APP_HOST}; use APP_HOST=0.0.0.0 for same-Wi-Fi phone testing."
fi

"${PYTHON_BIN}" - <<'PY' >/dev/null 2>&1 || {
import uvicorn
PY
  echo "Missing Python dependency: uvicorn."
  echo "Install dependencies with: ${PYTHON_BIN} -m pip install -r requirements.txt"
  echo "If this picked the wrong Python, set PYTHON_BIN=/path/to/python3 before running this script."
  exit 1
}

if [ "${APP_RELOAD}" = "true" ]; then
  "${PYTHON_BIN}" -m uvicorn app.main:app --host "${APP_HOST}" --port "${APP_PORT}" --reload
else
  "${PYTHON_BIN}" -m uvicorn app.main:app --host "${APP_HOST}" --port "${APP_PORT}"
fi
