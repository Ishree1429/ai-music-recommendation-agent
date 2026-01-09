from __future__ import annotations
import json
from pathlib import Path
from typing import Optional, Any, Dict
from src.user_state import UserState

def get_memory_path(project_root: Path, user_id: str) -> Path:
    return project_root / "data" / "user_memory" / f"{user_id}.json"


def load_user_state(project_root: Path, user_id: str) -> UserState:
    path = get_memory_path(project_root, user_id)
    if not path.exists():
        return UserState(user_id=user_id)

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return UserState.from_dict(data)


def save_user_state(project_root: Path, state: UserState) -> Path:
    path = get_memory_path(project_root, state.user_id)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=2, ensure_ascii=False)

    return path

from typing import Any, Dict
from src.learning import update_ordered_targets, update_categorical_affinity

def apply_feedback_and_save(
    project_root: Path,
    user_id: str,
    track_row: Dict[str, Any],
    track_numeric: Dict[str, float],
    emoji: str,
) -> Path:
    
    state = load_user_state(project_root, user_id)

    state.ordered_targets = update_ordered_targets(
        ordered_targets=state.ordered_targets,
        track_numeric=track_numeric,
        emoji=emoji,
    )

    state.categorical_affinity = update_categorical_affinity(
        categorical_affinity=state.categorical_affinity,
        track=track_row,
        emoji=emoji,
    )

    state.history.append(
        {
            "track_id": track_row.get("track_id"),
            "title": track_row.get("title"),
            "emoji": emoji,
        }
    )

    return save_user_state(project_root, state)

