from collections import Counter
from dataclasses import dataclass, field
from threading import RLock

from app.missions import Choice, MISSIONS, Mission


FALLBACK_MESSAGE = (
    "Live mode unavailable. Showing a prepared mission run. "
    "It shows the same idea in a reliable way."
)

PHASE_VOTE_TYPES = {
    "goal_vote": "goal",
    "rule_vote": "rule",
    "check_vote": "check",
}

PHASES = ("goal_vote", "rule_vote", "proposal", "check_vote", "result", "fallback")
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
                "proposal": self._proposal_for_phase(),
                "checks": dict(self.mission.checks) if self.phase in {"proposal", "check_vote", "result"} else {},
                "fallback_message": FALLBACK_MESSAGE if self.mode == "fallback" else None,
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
            elif self.phase == "fallback":
                self.mode = "live"
                self.phase = "goal_vote"
            return self.public_state()

    def reset(self) -> dict[str, object]:
        with self._lock:
            self.phase = "goal_vote"
            self.mode = "live"
            self.round = 1
            self.votes.clear()
            self.winning_choices.clear()
            return self.public_state()

    def fallback(self) -> dict[str, object]:
        with self._lock:
            self.phase = "fallback"
            self.mode = "fallback"
            return self.public_state()

    def select_mission(self, mission_id: str) -> dict[str, object]:
        with self._lock:
            if mission_id not in MISSIONS:
                raise VoteRejected(f"Unknown mission: {mission_id}")
            self.mission_id = mission_id
            return self.reset()

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
        return "Replay/fallback mode"

    def _proposal_for_phase(self) -> dict[str, object] | None:
        if self.phase in {"proposal", "check_vote", "result", "fallback"}:
            return self.mission.proposal.public_dict()
        return None

    @staticmethod
    def _choice_dict(choice: Choice) -> dict[str, str]:
        return {"id": choice.id, "label": choice.label}
