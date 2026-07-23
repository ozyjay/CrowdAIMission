from app.missions import CHECK_LABELS, MISSIONS


def test_mvp_missions_have_required_demo_content():
    assert set(MISSIONS) == {"game_studio", "truth_check", "future_me"}

    for mission in MISSIONS.values():
        assert mission.title
        assert mission.hook
        assert len(mission.goals) >= 3
        assert len(mission.rules) >= 3
        assert len(mission.check_options) >= 3
        assert mission.fallback_response
        assert mission.proposal.action in mission.allowed_actions
        assert mission.proposal.asset_id in mission.allowed_assets
        assert mission.proposal.caption
        assert set(mission.checks.values()) <= CHECK_LABELS


def test_truth_check_proposal_marks_evidence_as_warning():
    mission = MISSIONS["truth_check"]

    assert mission.proposal.requires_review is True
    assert mission.checks["evidence"] == "warn"


def test_future_me_proposal_asks_questions_without_career_guarantees():
    mission = MISSIONS["future_me"]
    proposal = mission.proposal.caption.lower()

    assert "ask staff" in proposal
    assert "?" in proposal
    assert "definitely" not in proposal
    assert "guarantee" not in proposal
    assert mission.checks["evidence"] == "not_required"
    assert "question" in mission.fallback_response.lower()
