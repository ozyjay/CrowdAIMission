#!/usr/bin/env bash
set -euo pipefail

HOTSPOT_NAME="${HOTSPOT_NAME:-CrowdAI-Hotspot}"
HOTSPOT_SSID="${HOTSPOT_SSID:-CrowdAI}"
HOTSPOT_INTERFACE="${HOTSPOT_INTERFACE:-}"
HOTSPOT_PASSWORD="${HOTSPOT_PASSWORD:-}"
APP_PORT="${APP_PORT:-3200}"

ASSUME_YES=false
ACTION=""

usage() {
  cat <<'EOF'
Manage the Crowd AI demo's offline Wi-Fi hotspot with NetworkManager.

Usage:
  ./scripts/manage_hotspot.sh start [--yes]
  ./scripts/manage_hotspot.sh stop
  ./scripts/manage_hotspot.sh restart [--yes]
  ./scripts/manage_hotspot.sh status
  ./scripts/manage_hotspot.sh help

Actions:
  start     Create or start the hotspot. Prompts for a password when first created.
  stop      Stop the hotspot without deleting its saved NetworkManager profile.
  restart   Stop and start the hotspot.
  status    Show hotspot, interface, address, and phone URL information.

Options:
  -y, --yes  Allow start to disconnect an existing Wi-Fi connection.
  -h, --help Show this help.

Optional environment variables:
  HOTSPOT_NAME       NetworkManager profile name (default: CrowdAI-Hotspot)
  HOTSPOT_SSID       Wi-Fi network name (default: CrowdAI)
  HOTSPOT_INTERFACE  Wi-Fi interface; auto-detected when unset
  HOTSPOT_PASSWORD   WPA password; prompted for when a new profile needs one
  APP_PORT           Demo web-app port (default: 3200)

The hotspot uses 2.4 GHz for broad phone compatibility and works without an
internet connection. Start the web app separately with APP_HOST=0.0.0.0.
EOF
}

fail() {
  echo "Error: $*" >&2
  exit 1
}

require_network_manager() {
  command -v nmcli >/dev/null 2>&1 ||
    fail "nmcli was not found. Install and enable NetworkManager first."

  if [ "$(nmcli -t -f RUNNING general 2>/dev/null || true)" != "running" ]; then
    fail "NetworkManager is not running."
  fi
}

profile_exists() {
  nmcli -g NAME connection show "${HOTSPOT_NAME}" >/dev/null 2>&1
}

profile_is_active() {
  nmcli -g NAME connection show --active 2>/dev/null |
    grep -Fxq "${HOTSPOT_NAME}"
}

find_wifi_interface() {
  local interface profile_interface

  if [ -n "${HOTSPOT_INTERFACE}" ]; then
    printf '%s\n' "${HOTSPOT_INTERFACE}"
    return
  fi

  if profile_exists; then
    profile_interface="$(
      nmcli -g connection.interface-name connection show "${HOTSPOT_NAME}" 2>/dev/null |
        head -n 1
    )"
    if [ -n "${profile_interface}" ] && [ "${profile_interface}" != "--" ]; then
      printf '%s\n' "${profile_interface}"
      return
    fi
  fi

  interface="$(
    nmcli -t -f DEVICE,TYPE device status |
      awk -F: '$2 == "wifi" { print $1; exit }'
  )"
  [ -n "${interface}" ] || fail "No Wi-Fi interface was found."
  printf '%s\n' "${interface}"
}

validate_interface() {
  local interface="$1"
  local device_type

  device_type="$(
    nmcli -t -f DEVICE,TYPE device status |
      awk -F: -v interface="${interface}" '$1 == interface { print $2; exit }'
  )"
  [ "${device_type}" = "wifi" ] ||
    fail "'${interface}' is not an available Wi-Fi interface."
}

prompt_for_password() {
  local first second

  if [ ! -t 0 ]; then
    fail "A password is required. Set HOTSPOT_PASSWORD for non-interactive use."
  fi

  read -r -s -p "Hotspot password (8-63 characters): " first
  echo
  read -r -s -p "Confirm hotspot password: " second
  echo

  [ "${first}" = "${second}" ] || fail "Passwords did not match."
  HOTSPOT_PASSWORD="${first}"
}

validate_password() {
  local length="${#HOTSPOT_PASSWORD}"
  if [ "${length}" -lt 8 ] || [ "${length}" -gt 63 ]; then
    fail "The hotspot password must contain 8-63 characters."
  fi
}

profile_needs_password() {
  local key_management
  key_management="$(
    nmcli -g 802-11-wireless-security.key-mgmt \
      connection show "${HOTSPOT_NAME}" 2>/dev/null |
      head -n 1
  )"
  [ -z "${key_management}" ] || [ "${key_management}" = "--" ]
}

confirm_wifi_disconnect() {
  local interface="$1"
  local current_connection

  current_connection="$(
    nmcli -g GENERAL.CONNECTION device show "${interface}" 2>/dev/null |
      head -n 1
  )"

  if [ -z "${current_connection}" ] ||
    [ "${current_connection}" = "--" ] ||
    [ "${current_connection}" = "${HOTSPOT_NAME}" ]; then
    return
  fi

  echo "Starting the hotspot will disconnect Wi-Fi '${current_connection}'."
  if [ "${ASSUME_YES}" = true ]; then
    return
  fi
  if [ ! -t 0 ]; then
    fail "Rerun with --yes to allow the Wi-Fi disconnection."
  fi

  read -r -p "Continue? [y/N] " answer
  case "${answer}" in
    y | Y | yes | YES) ;;
    *) fail "Hotspot start cancelled." ;;
  esac
}

hotspot_address() {
  local interface="$1"
  nmcli -g IP4.ADDRESS device show "${interface}" 2>/dev/null |
    awk -F/ 'NF { print $1; exit }'
}

print_connection_details() {
  local interface="$1"
  local address
  address="$(hotspot_address "${interface}")"

  echo "Hotspot:   ${HOTSPOT_SSID}"
  echo "Profile:   ${HOTSPOT_NAME}"
  echo "Interface: ${interface}"
  if [ -n "${address}" ]; then
    echo "Address:   ${address}"
    echo "Phone URL: http://${address}:${APP_PORT}/"
  else
    echo "Address:   unavailable"
  fi
}

start_hotspot() {
  local interface="$1"
  local new_profile=false
  local needs_password=false

  validate_interface "${interface}"
  confirm_wifi_disconnect "${interface}"

  if ! profile_exists; then
    new_profile=true
    needs_password=true
  elif profile_needs_password; then
    needs_password=true
  fi

  if [ "${needs_password}" = true ] && [ -z "${HOTSPOT_PASSWORD}" ]; then
    prompt_for_password
  fi

  if [ "${new_profile}" = true ]; then
    validate_password
    nmcli connection add \
      type wifi \
      ifname "${interface}" \
      con-name "${HOTSPOT_NAME}" \
      ssid "${HOTSPOT_SSID}" >/dev/null
  fi

  nmcli connection modify "${HOTSPOT_NAME}" \
    connection.interface-name "${interface}" \
    connection.autoconnect no \
    802-11-wireless.ssid "${HOTSPOT_SSID}" \
    802-11-wireless.mode ap \
    802-11-wireless.band bg \
    ipv4.method shared \
    ipv6.method disabled

  if [ "${new_profile}" = true ] ||
    [ "${needs_password}" = true ] ||
    [ -n "${HOTSPOT_PASSWORD}" ]; then
    validate_password
    nmcli connection modify "${HOTSPOT_NAME}" \
      802-11-wireless-security.key-mgmt wpa-psk \
      802-11-wireless-security.psk "${HOTSPOT_PASSWORD}"
  fi

  nmcli connection up "${HOTSPOT_NAME}" ifname "${interface}"
  echo
  echo "Offline hotspot started."
  print_connection_details "${interface}"
  echo "Start the demo with: APP_HOST=0.0.0.0 ./scripts/start_dev.sh"
}

stop_hotspot() {
  if ! profile_exists; then
    echo "Hotspot profile '${HOTSPOT_NAME}' does not exist."
    return
  fi

  if profile_is_active; then
    nmcli connection down "${HOTSPOT_NAME}"
    echo "Hotspot stopped. Its saved profile was kept."
  else
    echo "Hotspot is already stopped."
  fi
}

show_status() {
  local interface

  if ! profile_exists; then
    echo "Hotspot profile '${HOTSPOT_NAME}' has not been created."
    echo "Run: ./scripts/manage_hotspot.sh start"
    return
  fi

  interface="$(find_wifi_interface)"
  if profile_is_active; then
    echo "Status: active"
    print_connection_details "${interface}"
  else
    echo "Status: stopped"
    echo "Profile: ${HOTSPOT_NAME}"
    echo "SSID:    ${HOTSPOT_SSID}"
  fi
}

for argument in "$@"; do
  case "${argument}" in
    start | stop | restart | status | help)
      [ -z "${ACTION}" ] || fail "Specify only one action."
      ACTION="${argument}"
      ;;
    -y | --yes)
      ASSUME_YES=true
      ;;
    -h | --help)
      ACTION="help"
      ;;
    *)
      fail "Unknown argument '${argument}'. Run with --help for usage."
      ;;
  esac
done

ACTION="${ACTION:-status}"

if [ "${ACTION}" = "help" ]; then
  usage
  exit 0
fi

require_network_manager

case "${ACTION}" in
  start)
    start_hotspot "$(find_wifi_interface)"
    ;;
  stop)
    stop_hotspot
    ;;
  restart)
    stop_hotspot
    start_hotspot "$(find_wifi_interface)"
    ;;
  status)
    show_status
    ;;
esac
