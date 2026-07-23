#!/usr/bin/env python3
"""Render a standards-compatible Wi-Fi join QR code in the terminal."""

from __future__ import annotations

import sys

import qrcode


def escape_wifi_field(value: str) -> str:
    """Escape reserved characters in the common Wi-Fi QR payload format."""
    escaped = value.replace("\\", "\\\\")
    for character in ('"', ";", ",", ":"):
        escaped = escaped.replace(character, f"\\{character}")
    return escaped


def wifi_payload(ssid: str, password: str) -> str:
    """Build a WPA Wi-Fi QR payload understood by Android and iOS."""
    return (
        f"WIFI:T:WPA;S:{escape_wifi_field(ssid)};"
        f"P:{escape_wifi_field(password)};;"
    )


def main() -> int:
    values = sys.stdin.read().splitlines()
    if len(values) != 2 or not all(values):
        print("Expected SSID and password on standard input.", file=sys.stderr)
        return 2

    qr_code = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        border=2,
    )
    qr_code.add_data(wifi_payload(values[0], values[1]))
    qr_code.make(fit=True)
    qr_code.print_ascii(tty=sys.stdout.isatty(), invert=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
