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
APP_RELOAD="${APP_RELOAD:-true}"

if [ -z "${PYTHON_BIN:-}" ]; then
  if [ -x ".venv/bin/python3" ]; then
    PYTHON_BIN=".venv/bin/python3"
  elif command -v pyenv >/dev/null 2>&1; then
    PYTHON_BIN="$(pyenv which python3)"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  else
    PYTHON_BIN="python"
  fi
fi

echo "Python: ${PYTHON_BIN}"
if ! "${PYTHON_BIN}" -c "import uvicorn" >/dev/null 2>&1; then
  echo "Missing Python dependency: uvicorn."
  echo "Install dependencies with: ${PYTHON_BIN} -m pip install -r requirements.txt"
  echo "If this picked the wrong Python, set PYTHON_BIN=/path/to/python3 in .env."
  exit 1
fi

LAN_IP="$({ ipconfig getifaddr en0 || ifconfig en0 | awk '/inet / {print $2; exit}'; } 2>/dev/null || true)"

echo "Laptop URL: http://127.0.0.1:${APP_PORT}/"
if [ "${APP_HOST}" = "0.0.0.0" ] || [ "${APP_HOST}" = "${LAN_IP}" ]; then
  echo "Phone URL:  http://${LAN_IP:-<this-machine-LAN-IP>}:${APP_PORT}/"
else
  echo "Phone URL:  unavailable while APP_HOST=${APP_HOST}; use APP_HOST=0.0.0.0 for same-Wi-Fi phone testing."
fi

if [ -f "app/main.py" ]; then
  echo "Starting FastAPI app on ${APP_HOST}:${APP_PORT}"
  if [ "${APP_RELOAD}" = "true" ]; then
    exec "${PYTHON_BIN}" -m uvicorn app.main:app --host "${APP_HOST}" --port "${APP_PORT}" --reload
  fi
  exec "${PYTHON_BIN}" -m uvicorn app.main:app --host "${APP_HOST}" --port "${APP_PORT}"
fi

if [ -f "main.py" ]; then
  echo "Starting FastAPI app on ${APP_HOST}:${APP_PORT}"
  if [ "${APP_RELOAD}" = "true" ]; then
    exec "${PYTHON_BIN}" -m uvicorn main:app --host "${APP_HOST}" --port "${APP_PORT}" --reload
  fi
  exec "${PYTHON_BIN}" -m uvicorn main:app --host "${APP_HOST}" --port "${APP_PORT}"
fi

if [ -f "package.json" ]; then
  echo "package.json found. Running npm dev script. Ensure it respects APP_PORT=${APP_PORT}."
  exec npm run dev
fi

echo "No recognised app entrypoint found."
echo "Expected one of: app/main.py, main.py, package.json."
echo "Create the MVP app scaffold, then rerun this script."
exit 1
