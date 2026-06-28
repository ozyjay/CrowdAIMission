#!/usr/bin/env bash
set -euo pipefail

PORTS=(3200 8200 8600 8700 8800)

for port in "${PORTS[@]}"; do
  if command -v lsof >/dev/null 2>&1; then
    if lsof -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then
      echo "Port $port is already in use:"
      lsof -iTCP:"$port" -sTCP:LISTEN
      exit 1
    fi
  elif command -v ss >/dev/null 2>&1; then
    if ss -ltn | awk '{print $4}' | grep -q ":$port$"; then
      echo "Port $port is already in use."
      ss -ltn | grep ":$port"
      exit 1
    fi
  else
    echo "No lsof or ss available; cannot check port $port."
  fi
  echo "Port $port OK"
done
