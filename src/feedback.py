from __future__ import annotations
from typing import Dict, Any
from src.config import EMOJI_TO_SCORE, LEARNING_RATE
from src.user_state import UserState

from src.learning import update_ordered_targets, update_categorical_affinity
from src.config import ENERGY_MAP, TEMPO_MAP, DANCEABILITY_MAP, INTENSITY_MAP, LYRICS_INTENSITY_MAP


ORDERED_KEYS = ["energy", "tempo", "danceability", "intensity_type", "lyrics_intensity"]


def emoji_to_reward(emoji: str) -> int:
    if emoji not in EMOJI_TO_SCORE:
        raise ValueError(f"Unknown emoji '{emoji}'. Allowed: {list(EMOJI_TO_SCORE.keys())}")
    return int(EMOJI_TO_SCORE[emoji])


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def _safe_float(x: Any) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0




def _to_num(v: Any, m: Dict[str, float], default: float = 0.5) -> float:
    if v is None:
        return default
    key = str(v).strip().lower()
    return float(m.get(key, default))


def _track_numeric(track: Dict[str, Any]) -> Dict[str, float]:
    return {
        "energy": _to_num(track.get("energy"), ENERGY_MAP),
        "tempo": _to_num(track.get("tempo"), TEMPO_MAP),
        "danceability": _to_num(track.get("danceability"), DANCEABILITY_MAP),
        "intensity_type": _to_num(track.get("intensity_type"), INTENSITY_MAP),
        "lyrics_intensity": _to_num(track.get("lyrics_intensity"), LYRICS_INTENSITY_MAP),
    }


def apply_feedback(state, track: Dict[str, Any], emoji: str):
    
    if state.ordered_targets is None:
        state.ordered_targets = {}
    if state.categorical_affinity is None:
        state.categorical_affinity = {}
    if state.history is None:
        state.history = []
   
    if not hasattr(state, "top_signals") or state.top_signals is None:
        state.top_signals = []

    # 1) Update categorical affinity (genre/tag learning)
    state.categorical_affinity = update_categorical_affinity(
        categorical_affinity=state.categorical_affinity,
        track=track,
        emoji=emoji,
    )

    signals = []
    for field in ["genre", "therapy_tag"]:
        weights = state.categorical_affinity.get(field, {})
        if isinstance(weights, dict) and weights:
            top = sorted(weights.items(), key=lambda x: x[1], reverse=True)
            for name, val in top[:2]:
                # keep only meaningful positive preferences
                try:
                    if float(val) > 0.05:
                        signals.append(str(name))
                except Exception:
                    continue
    state.top_signals = signals[:4]

    track_num = _track_numeric(track)
    state.ordered_targets = update_ordered_targets(
        ordered_targets=state.ordered_targets,
        track_numeric=track_num,
        emoji=emoji,
    )

    state.history.append(
        {
            "track_id": track.get("track_id"),
            "title": track.get("title", ""),
            "emoji": emoji,
        }
    )

    return state
