from fastapi.testclient import TestClient

from app.main import app, demo_state


def setup_function():
    demo_state.reset()


def test_static_routes_and_health_respond():
    client = TestClient(app)

    for path in ["/", "/screen", "/staff", "/health", "/replay"]:
        response = client.get(path)
        assert response.status_code == 200

    health = client.get("/health").json()
    assert health == {
        "status": "healthy",
        "mode": "live",
        "app_port": 3200,
        "missions_loaded": 2,
        "model_enabled": False,
    }


def test_qr_svg_points_to_visitor_controller_for_request_host():
    client = TestClient(app, base_url="http://192.168.0.136:3200")

    response = client.get("/qr.svg")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert response.headers["cache-control"] == "no-store"
    assert "http://192.168.0.136:3200/" in response.text
    assert "<svg" in response.text
    assert response.text.index("<svg") < response.text.index("<title>")


def test_screen_and_staff_expose_qr_code_for_mobile_joining():
    client = TestClient(app)

    screen = client.get("/screen").text
    staff = client.get("/staff").text

    assert 'src="/qr.svg"' in screen
    assert "Scan to join" in screen
    assert 'src="/qr.svg"' in staff
    assert "Phone join" in staff


def test_api_state_exposes_public_shape_only():
    client = TestClient(app)

    state = client.get("/api/state").json()

    assert set(state) == {
        "session_id",
        "mission_id",
        "mission_title",
        "phase",
        "mode",
        "round",
        "question",
        "choices",
        "votes",
        "winning_choices",
        "proposal",
        "checks",
        "fallback_message",
    }
    assert "email" not in str(state).lower()
    assert "phone" not in str(state).lower()
    assert "name" not in str(state).lower()


def test_vote_endpoint_accepts_only_curated_current_choices():
    client = TestClient(app)

    response = client.post(
        "/api/vote",
        json={"vote_type": "goal", "choice_id": "help_player_escape"},
    )
    assert response.status_code == 200
    assert response.json()["votes"]["help_player_escape"] == 1

    invalid = client.post(
        "/api/vote",
        json={"vote_type": "goal", "choice_id": "personal_story"},
    )
    assert invalid.status_code == 400

    wrong_phase = client.post(
        "/api/vote",
        json={"vote_type": "rule", "choice_id": "do_not_spoil_solution"},
    )
    assert wrong_phase.status_code == 400


def test_staff_controls_select_advance_reset_and_fallback():
    client = TestClient(app)

    selected = client.post(
        "/api/staff/select-mission",
        json={"mission_id": "truth_check"},
    )
    assert selected.status_code == 200
    assert selected.json()["mission_id"] == "truth_check"

    advanced = client.post("/api/staff/advance")
    assert advanced.status_code == 200
    assert advanced.json()["phase"] == "rule_vote"

    fallback = client.post("/api/staff/fallback")
    assert fallback.status_code == 200
    assert fallback.json()["mode"] == "fallback"

    reset = client.post("/api/staff/reset")
    assert reset.status_code == 200
    assert reset.json()["phase"] == "goal_vote"
    assert reset.json()["mode"] == "live"


def test_websocket_receives_initial_public_state():
    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        initial = websocket.receive_json()
        assert initial["phase"] == "goal_vote"
        assert initial["mission_id"] in {"game_studio", "truth_check"}
        assert initial["choices"]


def test_visitor_page_has_no_free_text_inputs():
    client = TestClient(app)

    html = client.get("/").text.lower()

    assert "<textarea" not in html
    assert 'type="text"' not in html
    assert 'contenteditable="true"' not in html
    assert "email" not in html
    assert "phone number" not in html
