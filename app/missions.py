from dataclasses import dataclass


CHECK_LABELS = {
    "pass",
    "warn",
    "fail",
    "not_required",
    "needs_human",
    "fallback_used",
}


@dataclass(frozen=True)
class Choice:
    id: str
    label: str


@dataclass(frozen=True)
class Proposal:
    action: str
    asset_id: str
    caption: str
    source_ids: tuple[str, ...]
    requires_review: bool

    def public_dict(self) -> dict[str, object]:
        return {
            "action": self.action,
            "asset_id": self.asset_id,
            "caption": self.caption,
            "source_ids": list(self.source_ids),
            "requires_review": self.requires_review,
            "label": "Controlled demo proposal",
        }


@dataclass(frozen=True)
class Mission:
    id: str
    title: str
    hook: str
    audience_pull: str
    goals: tuple[Choice, ...]
    rules: tuple[Choice, ...]
    check_options: tuple[Choice, ...]
    repair_options: tuple[Choice, ...]
    allowed_actions: tuple[str, ...]
    allowed_assets: tuple[str, ...]
    proposal: Proposal
    checks: dict[str, str]
    safe_failure_examples: tuple[str, ...]
    fallback_response: str
    staff_script: str
    test_cases: tuple[str, ...]


MISSIONS: dict[str, Mission] = {
    "game_studio": Mission(
        id="game_studio",
        title="Game Studio Mission",
        hook="Can the crowd keep a game helper useful without spoiling the game?",
        audience_pull="Highschoolers, gamers, and passersby",
        goals=(
            Choice("help_player_escape", "Help the player escape"),
            Choice("add_a_twist", "Add a twist"),
            Choice("make_npc_funnier", "Make the NPC funnier"),
            Choice("make_level_fairer", "Make the level fairer"),
            Choice("teach_mechanic", "Help the player learn the mechanic"),
        ),
        rules=(
            Choice("do_not_spoil_solution", "Do not give away the answer"),
            Choice("family_friendly", "Keep it family-friendly"),
            Choice("player_in_control", "Keep the player in control"),
            Choice("hints_not_solutions", "Give hints, not solutions"),
            Choice("keep_it_short", "Keep it short"),
        ),
        check_options=(
            Choice("use_it", "Use it"),
            Choice("too_easy", "Too easy"),
            Choice("too_vague", "Too vague"),
            Choice("spoiled_answer", "Spoiled the answer"),
            Choice("better_hint", "Ask for a better hint"),
        ),
        repair_options=(
            Choice("clearer_goal", "Clearer goal"),
            Choice("stronger_rule", "Stronger rule"),
            Choice("shorter_response", "Shorter response"),
            Choice("safe_fallback", "Safe fallback"),
        ),
        allowed_actions=("npc_hint", "npc_repair", "fallback"),
        allowed_assets=("npc_helper", "reef_lab_door", "fallback_card"),
        proposal=Proposal(
            action="npc_hint",
            asset_id="npc_helper",
            caption="Look for numbers hidden near the oxygen tanks.",
            source_ids=(),
            requires_review=False,
        ),
        checks={
            "intent": "pass",
            "schema": "pass",
            "rules": "pass",
            "evidence": "not_required",
            "safety": "pass",
        },
        safe_failure_examples=(
            "AI reveals the answer.",
            "AI ignores the chosen rule.",
            "AI invents an impossible item.",
        ),
        fallback_response="Use prepared NPC hints from a deterministic table.",
        staff_script="The crowd keeps the helper useful by choosing hints over answers.",
        test_cases=("hint_without_answer", "spoiler_repaired_to_hint"),
    ),
    "truth_check": Mission(
        id="truth_check",
        title="Deepfake Detective / Truth Check",
        hook="Can the crowd catch unsupported AI claims?",
        audience_pull="Highschoolers, teachers, and parents",
        goals=(
            Choice("check_ai_post", "Check the AI post"),
            Choice("spot_unsupported_claim", "Spot unsupported claims"),
            Choice("make_claim_neutral", "Make the claim neutral"),
            Choice("ask_for_source", "Ask for a source"),
        ),
        rules=(
            Choice("approved_facts_only", "Use approved facts only"),
            Choice("no_fake_certainty", "Do not sound certain without evidence"),
            Choice("ask_staff_for_facts", "Ask staff for course facts"),
            Choice("keep_caption_neutral", "Keep captions neutral"),
        ),
        check_options=(
            Choice("unsupported_claim", "Unsupported claim"),
            Choice("too_confident", "Too confident"),
            Choice("needs_source", "Might be real but needs source"),
            Choice("misleading_caption", "Misleading image or caption"),
            Choice("looks_okay", "Looks okay"),
        ),
        repair_options=(
            Choice("ask_for_source", "Ask for a source"),
            Choice("make_neutral", "Make it neutral"),
            Choice("ask_staff", "Ask staff"),
            Choice("remove_claim", "Remove the claim"),
            Choice("approved_facts_only", "Use approved facts only"),
        ),
        allowed_actions=("flag_claim", "neutral_repair", "fallback"),
        allowed_assets=("claim_card", "source_badge", "fallback_card"),
        proposal=Proposal(
            action="neutral_repair",
            asset_id="claim_card",
            caption=(
                "Ask staff about IT, AI, robotics, and marine technology "
                "pathways instead of treating the claim as fact."
            ),
            source_ids=(),
            requires_review=True,
        ),
        checks={
            "intent": "pass",
            "schema": "pass",
            "rules": "pass",
            "evidence": "warn",
            "safety": "pass",
        },
        safe_failure_examples=(
            "AI invents an event detail.",
            "AI claims certainty without evidence.",
            "AI turns a rumour into a fact.",
        ),
        fallback_response="Use scripted claim cards with known expected verdicts.",
        staff_script="The crowd can flag uncertainty, but staff remain the source for real facts.",
        test_cases=("unsupported_claim_flagged", "invented_fact_repaired_to_question"),
    ),
}
