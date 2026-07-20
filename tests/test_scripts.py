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
