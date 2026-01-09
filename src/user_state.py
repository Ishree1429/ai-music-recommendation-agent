from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class UserState:
    user_id: str

    # Ordered numeric targets 
    ordered_targets: Dict[str, float] = field(default_factory=dict)

    # Categorical affinities 
    categorical_affinity: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "therapy_tag": {},
        "emotional_tag": {},
        "genre": {},
    })

    # explainability/debug
    history: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "ordered_targets": self.ordered_targets,
            "categorical_affinity": self.categorical_affinity,
            "history": self.history,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "UserState":
        return UserState(
            user_id=d.get("user_id", "unknown"),
            ordered_targets=d.get("ordered_targets", {}) or {},
            categorical_affinity=d.get("categorical_affinity", {
                "therapy_tag": {},
                "emotional_tag": {},
                "genre": {},
            }) or {
                "therapy_tag": {},
                "emotional_tag": {},
                "genre": {},
            },
            history=d.get("history", []) or [],
        )
