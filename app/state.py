from collections import Counter
from dataclasses import dataclass, field
from threading import RLock

from app.missions import Choice, MISSIONS, Mission


FALLBACK_MESSAGE = (
    "Live mode unavailable. Showing a prepared mission run. "
    "It shows the same idea in a reliable way."
)
REPLAY_MESSAGE = (
    "Showing a prepared mission run. "
    "It shows the same control loop without requiring phone votes."
)

PHASE_VOTE_TYPES = {
    "goal_vote": "goal",
    "rule_vote": "rule",
    "check_vote": "check",
}

PHASES = (
    "goal_vote",
    "rule_vote",
    "proposal",
    "check_vote",
    "result",
    "fallback",
    "replay",
)
VALID_MODES = {"live", "fallback", "replay"}
VALID_VOTE_TYPES = {"goal", "rule", "check", "repair"}


class VoteRejected(ValueError):
    """Raised when a vote is not valid for the current public state."""


@dataclass
class DemoState:
    mission_id: str = "game_studio"
    phase: str = "goal_vote"
    mode: str = "live"
    round: int = 1
    votes: dict[str, Counter[str]] = field(default_factory=dict)
    winning_choices: dict[str, str] = field(default_factory=dict)
    _lock: RLock = field(default_factory=RLock, init=False, repr=False)

    @property
    def mission(self) -> Mission:
        return MISSIONS[self.mission_id]

    def public_state(self) -> dict[str, object]:
        with self._lock:
            vote_type = PHASE_VOTE_TYPES.get(self.phase)
            choices = self._choices_for_phase()
            selections = {
                "goal": self._winning_choice_dict("goal", self.mission.goals),
                "rule": self._winning_choice_dict("rule", self.mission.rules),
                "decision": self._winning_choice_dict("check", self.mission.check_options),
            }
            return {
                "session_id": "current",
                "mission_id": self.mission.id,
                "mission_title": self.mission.title,
                "phase": self.phase,
                "mode": self.mode,
                "round": self.round,
                "question": self._question_for_phase(),
                "choices": [self._choice_dict(choice) for choice in choices],
                "votes": dict(self.votes.get(vote_type, Counter())) if vote_type else {},
                "winning_choices": dict(self.winning_choices),
                "selections": selections,
                "proposal": self._proposal_for_phase(),
                "checks": (
                    dict(self.mission.checks)
                    if self.phase in {"proposal", "check_vote", "result"}
                    else {}
                ),
                "result": self._result_for_phase(selections),
                "fallback_message": self._mode_message(),
            }

    def submit_vote(self, vote_type: str, choice_id: str) -> dict[str, object]:
        with self._lock:
            self._validate_vote(vote_type, choice_id)
            bucket = self.votes.setdefault(vote_type, Counter())
            bucket[choice_id] += 1
            self.winning_choices[vote_type] = self._winning_choice(vote_type)
            return self.public_state()

    def advance(self) -> dict[str, object]:
        with self._lock:
            if self.phase == "goal_vote":
                self.phase = "rule_vote"
            elif self.phase == "rule_vote":
                self.phase = "proposal"
            elif self.phase == "proposal":
                self.phase = "check_vote"
            elif self.phase == "check_vote":
                self.phase = "result"
            elif self.phase == "result":
                self.round += 1
                self.phase = "goal_vote"
                self.votes.clear()
                self.winning_choices.clear()
            elif self.phase in {"fallback", "replay"}:
                self.mode = "live"
                self.phase = "goal_vote"
            return self.public_state()

    def reset(self, scope: str = "round") -> dict[str, object]:
        with self._lock:
            if scope not in {"round", "session"}:
                raise VoteRejected(f"Unsupported reset scope: {scope}")
            self.phase = "goal_vote"
            self.mode = "live"
            if scope == "session":
                self.round = 1
            self.votes.clear()
            self.winning_choices.clear()
            return self.public_state()

    def clear_votes(self) -> dict[str, object]:
        with self._lock:
            self.votes.clear()
            self.winning_choices.clear()
            return self.public_state()

    def fallback(self) -> dict[str, object]:
        return self.set_mode("fallback")

    def set_mode(self, mode: str) -> dict[str, object]:
        with self._lock:
            if mode not in VALID_MODES:
                raise VoteRejected(f"Unsupported mode: {mode}")
            self.mode = mode
            self.phase = "goal_vote" if mode == "live" else mode
            return self.public_state()

    def select_mission(self, mission_id: str) -> dict[str, object]:
        with self._lock:
            if mission_id not in MISSIONS:
                raise VoteRejected(f"Unknown mission: {mission_id}")
            self.mission_id = mission_id
            return self.reset(scope="session")

    def _validate_vote(self, vote_type: str, choice_id: str) -> None:
        if vote_type not in VALID_VOTE_TYPES:
            raise VoteRejected(f"Unsupported vote type: {vote_type}")
        expected_vote_type = PHASE_VOTE_TYPES.get(self.phase)
        if vote_type != expected_vote_type:
            raise VoteRejected(f"Cannot vote for {vote_type} during {self.phase}")
        valid_choices = {choice.id for choice in self._choices_for_phase()}
        if choice_id not in valid_choices:
            raise VoteRejected(f"Unsupported choice: {choice_id}")

    def _winning_choice(self, vote_type: str) -> str:
        counts = self.votes.get(vote_type, Counter())
        return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]

    def _choices_for_phase(self) -> tuple[Choice, ...]:
        if self.phase == "goal_vote":
            return self.mission.goals
        if self.phase == "rule_vote":
            return self.mission.rules
        if self.phase == "check_vote":
            return self.mission.check_options
        return ()

    def _question_for_phase(self) -> str:
        if self.phase == "goal_vote":
            return "What should the mission try to do?"
        if self.phase == "rule_vote":
            return "What must the local AI remember?"
        if self.phase == "proposal":
            return "Controlled proposal and software checks"
        if self.phase == "check_vote":
            return "Is the local AI on track?"
        if self.phase == "result":
            return "Crowd decision and mission update"
        if self.phase == "replay":
            return "Prepared replay mode"
        return "Replay/fallback mode"

    def _proposal_for_phase(self) -> dict[str, object] | None:
        if self.phase in {"proposal", "check_vote", "result", "fallback", "replay"}:
            proposal = self.mission.proposal.public_dict()
            proposal["goal"] = self._winning_choice_dict("goal", self.mission.goals)
            proposal["rule"] = self._winning_choice_dict("rule", self.mission.rules)
            return proposal
        return None

    def _winning_choice_dict(
        self, vote_type: str, choices: tuple[Choice, ...]
    ) -> dict[str, str] | None:
        winning_id = self.winning_choices.get(vote_type)
        if winning_id is None and self.mode in {"fallback", "replay"}:
            return self._choice_dict(choices[0])
        if winning_id is None:
            return None
        choice = next((item for item in choices if item.id == winning_id), None)
        return self._choice_dict(choice) if choice else None

    def _result_for_phase(self, selections: dict[str, object]) -> dict[str, object] | None:
        if self.phase in {"fallback", "replay"}:
            return {
                "decision": selections["decision"],
                "message": self.mission.fallback_response,
            }
        if self.phase != "result":
            return None
        decision = selections["decision"]
        decision_label = (
            decision["label"] if isinstance(decision, dict) else "No decision recorded"
        )
        return {
            "decision": decision,
            "message": (
                f"Crowd decision: {decision_label}. "
                "The prepared mission response remains under human control."
            ),
        }

    def _mode_message(self) -> str | None:
        if self.mode == "fallback":
            return FALLBACK_MESSAGE
        if self.mode == "replay":
            return REPLAY_MESSAGE
        return None

    @staticmethod
    def _choice_dict(choice: Choice) -> dict[str, str]:
        return {"id": choice.id, "label": choice.label}
