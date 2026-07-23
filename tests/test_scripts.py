import os
import subprocess
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"


def test_powershell_scripts_exist_for_local_setup():
    for name in ["check_ports.ps1", "start_dev.ps1", "smoke_test.ps1"]:
        assert (SCRIPTS_DIR / name).exists()


def test_powershell_scripts_mirror_fixed_ports_and_routes():
    check_ports = (SCRIPTS_DIR / "check_ports.ps1").read_text()
    smoke_test = (SCRIPTS_DIR / "smoke_test.ps1").read_text()
    start_dev = (SCRIPTS_DIR / "start_dev.ps1").read_text()

    for port in ["3200", "8200", "8600", "8700", "8800"]:
        assert port in check_ports

    for route in ["/", "/screen", "/staff", "/health", "/replay", "/api/missions", "/qr.svg"]:
        assert route in smoke_test

    assert "APP_HOST" in start_dev
    assert "0.0.0.0" in start_dev
    assert "Phone URL" in start_dev
    assert "PYTHON_BIN" in start_dev
    assert "pyenv" in start_dev
    assert "python3" in start_dev


def test_linux_hotspot_script_has_safe_demo_defaults():
    hotspot_script = SCRIPTS_DIR / "manage_hotspot.sh"

    assert hotspot_script.exists()
    assert hotspot_script.stat().st_mode & 0o111

    script = hotspot_script.read_text()
    assert 'HOTSPOT_SSID="${HOTSPOT_SSID:-CrowdAI}"' in script
    assert 'APP_PORT="${APP_PORT:-3200}"' in script
    assert "802-11-wireless.band bg" in script
    assert "ipv4.method shared" in script
    assert "802-11-wireless-security.key-mgmt wpa-psk" in script
    assert "od -An -N12 -tx1 /dev/urandom" in script
    assert 'connection show uuid "${profile_uuid}"' in script
    assert "normalise_duplicate_profiles" in script
    assert "render_wifi_qr.py" in script


def test_linux_hotspot_help_does_not_require_network_manager():
    result = subprocess.run(
        ["bash", str(SCRIPTS_DIR / "manage_hotspot.sh"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Manage the Crowd AI demo's offline Wi-Fi hotspot" in result.stdout
    assert "HOTSPOT_INTERFACE" in result.stdout
    assert "./scripts/manage_hotspot.sh qr" in result.stdout


def test_start_dev_command_environment_overrides_dotenv(tmp_path):
    (tmp_path / ".env").write_text(
        "APP_HOST=127.0.0.1\n"
        "APP_PORT=9999\n"
        "APP_RELOAD=true\n"
    )
    fake_python = tmp_path / "python3"
    fake_python.write_text("#!/usr/bin/env bash\nexit 0\n")
    fake_python.chmod(0o755)

    environment = os.environ.copy()
    environment.update(
        {
            "APP_HOST": "0.0.0.0",
            "APP_PORT": "3200",
            "APP_RELOAD": "false",
            "PYTHON_BIN": str(fake_python),
        }
    )
    result = subprocess.run(
        ["bash", str(SCRIPTS_DIR / "start_dev.sh")],
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Laptop URL: http://127.0.0.1:3200/" in result.stdout
    assert "Phone URL:" in result.stdout
    assert "unavailable while APP_HOST" not in result.stdout
