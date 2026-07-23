import os
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "manage_hotspot.sh"


def fake_network_manager(tmp_path):
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    command_log = tmp_path / "nmcli.log"
    renamed_marker = tmp_path / "duplicate-renamed"
    fake_nmcli = fake_bin / "nmcli"
    fake_nmcli.write_text(
        """#!/usr/bin/env python3
import os
import sys

args = sys.argv[1:]
with open(os.environ["FAKE_NMCLI_LOG"], "a", encoding="utf-8") as log:
    log.write(repr(args) + "\\n")

if args == ["-t", "-f", "RUNNING", "general"]:
    print("running")
elif args == ["-t", "-f", "UUID,NAME", "connection", "show"]:
    print("uuid-active:CrowdAI-Hotspot")
    if not os.path.exists(os.environ["FAKE_NMCLI_RENAMED"]):
        print("uuid-inactive:CrowdAI-Hotspot")
elif args == ["-t", "-f", "UUID,NAME", "connection", "show", "--active"]:
    print("uuid-active:CrowdAI-Hotspot")
elif args == ["-g", "UUID", "connection", "show", "--active"]:
    print("uuid-active")
elif args == ["connection", "down", "uuid", "uuid-active"]:
    print("Connection successfully deactivated")
elif args == [
    "-g", "connection.interface-name", "connection", "show", "uuid", "uuid-active"
]:
    print("wlp192s0")
elif args == ["-t", "-f", "DEVICE,TYPE", "device", "status"]:
    print("wlp192s0:wifi")
elif args == ["-g", "GENERAL.CONNECTION", "device", "show", "wlp192s0"]:
    print("CrowdAI-Hotspot")
elif args == [
    "connection", "modify", "uuid", "uuid-inactive", "connection.id",
    "CrowdAI-Hotspot-duplicate-uuid-ina"
]:
    open(os.environ["FAKE_NMCLI_RENAMED"], "w", encoding="utf-8").close()
elif args == [
    "-g", "802-11-wireless-security.key-mgmt", "connection", "show", "uuid",
    "uuid-active"
]:
    print("wpa-psk")
elif args == [
    "--show-secrets", "-g", "802-11-wireless-security.psk", "connection",
    "show", "uuid", "uuid-active"
]:
    print("existing-demo-password")
elif args[:4] == ["connection", "modify", "uuid", "uuid-active"]:
    pass
elif args == [
    "connection", "up", "uuid", "uuid-active", "ifname", "wlp192s0"
]:
    print("Connection successfully activated")
elif args == ["-g", "IP4.ADDRESS", "device", "show", "wlp192s0"]:
    print("10.42.0.1/24")
elif args == [
    "-g", "802-11-wireless.ssid", "connection", "show", "uuid", "uuid-active"
]:
    print("CrowdAI")
else:
    print(f"Unexpected nmcli arguments: {args!r}", file=sys.stderr)
    raise SystemExit(64)
"""
    )
    fake_nmcli.chmod(0o755)

    environment = os.environ.copy()
    environment["FAKE_NMCLI_LOG"] = str(command_log)
    environment["FAKE_NMCLI_RENAMED"] = str(renamed_marker)
    environment["PATH"] = f"{fake_bin}:{environment['PATH']}"
    return command_log, environment


def test_stop_targets_duplicate_profiles_by_uuid(tmp_path):
    command_log, environment = fake_network_manager(tmp_path)

    result = subprocess.run(
        ["bash", str(SCRIPT), "stop"],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 0, result.stderr
    assert "Hotspot stopped" in result.stdout
    log = command_log.read_text()
    assert "['connection', 'down', 'uuid', 'uuid-active']" in log
    assert "['connection', 'down', 'CrowdAI-Hotspot']" not in log


def test_start_preserves_and_renames_duplicate_profile(tmp_path):
    command_log, environment = fake_network_manager(tmp_path)

    result = subprocess.run(
        ["bash", str(SCRIPT), "start", "--yes"],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 0, result.stderr
    assert "Found 2 hotspot profiles" in result.stderr
    assert "Preserved duplicate uuid-inactive" in result.stderr
    assert "Offline hotspot started" in result.stdout
    assert "Phone URL: http://10.42.0.1:3200/" in result.stdout
    assert "Password: existing-demo-password" in result.stdout

    log = command_log.read_text()
    assert (
        "['connection', 'modify', 'uuid', 'uuid-inactive', 'connection.id', "
        "'CrowdAI-Hotspot-duplicate-uuid-ina']"
    ) in log
    assert "['connection', 'up', 'uuid', 'uuid-active'" in log
