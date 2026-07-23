import subprocess
import sys
from pathlib import Path

from scripts.render_wifi_qr import escape_wifi_field, wifi_payload


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "render_wifi_qr.py"


def test_wifi_payload_escapes_reserved_characters():
    assert escape_wifi_field('Crowd;AI: "Demo",\\') == (
        'Crowd\\;AI\\: \\"Demo\\"\\,\\\\'
    )
    assert wifi_payload("CrowdAI", "demo:password") == (
        "WIFI:T:WPA;S:CrowdAI;P:demo\\:password;;"
    )


def test_wifi_qr_renders_from_standard_input_without_echoing_password():
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input="CrowdAI\nprivate-demo-password\n",
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stdout.strip()
    assert "private-demo-password" not in result.stdout
