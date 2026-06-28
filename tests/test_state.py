import pytest

from app.state import DemoState, VoteRejected


def test_initial_public_state_matches_goal_vote_contract():
    state = DemoState()

    public = state.public_state()

    assert public["session_id"] == "current"
    assert public["mission_id"] == "game_studio"
    assert public["mission_title"] == "Game Studio Mission"
    assert public["phase"] == "goal_vote"
    assert public["mode"] == "live"
    assert public["round"] == 1
    assert public["question"] == "What should the mission try to do?"
    assert public["choices"]
    assert public["votes"] == {}
    assert public["winning_choices"] == {}
    assert public["proposal"] is None
    assert public["checks"] == {}
    assert public["fallback_message"] is None


def test_votes_aggregate_for_current_phase_only():
    state = DemoState()

    state.submit_vote("goal", "help_player_escape")
    state.submit_vote("goal", "help_player_escape")
    state.submit_vote("goal", "make_level_fairer")

    public = state.public_state()

    assert public["votes"] == {
        "help_player_escape": 2,
        "make_level_fairer": 1,
    }
    assert public["winning_choices"]["goal"] == "help_player_escape"


def test_wrong_phase_vote_is_rejected_without_mutating_state():
    state = DemoState()

    before = state.public_state()

    with pytest.raises(VoteRejected):
        state.submit_vote("rule", "do_not_spoil_solution")

    assert state.public_state() == before


def test_invalid_vote_type_and_choice_are_rejected():
    state = DemoState()

    with pytest.raises(VoteRejected):
        state.submit_vote("visitor_name", "anything")

    with pytest.raises(VoteRejected):
        state.submit_vote("goal", "not_a_curated_choice")


def test_advance_reveals_proposal_checks_and_result():
    state = DemoState()
    state.submit_vote("goal", "help_player_escape")

    state.advance()
    assert state.public_state()["phase"] == "rule_vote"

    state.submit_vote("rule", "do_not_spoil_solution")
    state.advance()
    proposal_state = state.public_state()
    assert proposal_state["phase"] == "proposal"
    assert proposal_state["proposal"]["caption"]
    assert proposal_state["checks"]["schema"] == "pass"

    state.advance()
    assert state.public_state()["phase"] == "check_vote"

    state.submit_vote("check", "spoiled_answer")
    state.advance()
    result_state = state.public_state()
    assert result_state["phase"] == "result"
    assert result_state["winning_choices"]["check"] == "spoiled_answer"


def test_reset_clears_votes_and_returns_to_goal_vote():
    state = DemoState()
    state.submit_vote("goal", "help_player_escape")
    state.advance()

    state.reset()

    public = state.public_state()
    assert public["phase"] == "goal_vote"
    assert public["votes"] == {}
    assert public["winning_choices"] == {}
    assert public["mode"] == "live"


def test_fallback_sets_public_replay_copy():
    state = DemoState()

    state.fallback()

    public = state.public_state()
    assert public["phase"] == "fallback"
    assert public["mode"] == "fallback"
    assert public["fallback_message"] == (
        "Live mode unavailable. Showing a prepared mission run. "
        "It shows the same idea in a reliable way."
    )


def test_select_mission_resets_state_to_selected_mission():
    state = DemoState()
    state.submit_vote("goal", "help_player_escape")

    state.select_mission("truth_check")

    public = state.public_state()
    assert public["mission_id"] == "truth_check"
    assert public["mission_title"] == "Deepfake Detective / Truth Check"
    assert public["phase"] == "goal_vote"
    assert public["votes"] == {}
