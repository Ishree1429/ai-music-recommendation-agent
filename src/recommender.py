# src/recommender.py
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.scoring import (
    build_user_music_prefs_from_personality,
    score_track,
    ScoreBreakdown,
)

from src.memory_store import load_user_state
from src.config import BLEND_ALPHA



def load_music_library_csv(csv_path: str | Path) -> List[Dict[str, Any]]:
    csv_path = Path(csv_path)
    rows: List[Dict[str, Any]] = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
                        row = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
                        for num_k in ["energy", "tempo", "danceability", "lyrics_intensity"]:
                             if num_k in row and row[num_k] != "":
                                try:
                                    row[num_k] = float(row[num_k])
                                except Exception:
                                    pass
                        rows.append(row)

    return rows


def load_json(path: str | Path) -> Dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# Output object
@dataclass
class Recommendation:
    track_id: str
    title: str
    artist: str
    score: float
    reason: str
    debug: Dict[str, Any]

# for memory
def blend_user_prefs_with_memory(
    base_prefs: Dict[str, Any],
    learned_targets: Dict[str, float],
    alpha: float = BLEND_ALPHA,
) -> Dict[str, Any]:

    if not learned_targets:
        return base_prefs

    blended = dict(base_prefs)
    base_targets = blended.get("ordered_targets", {}) or {}
    out_targets = dict(base_targets)

    for k, learned_v in learned_targets.items():
        if k in base_targets:
            out_targets[k] = alpha * float(base_targets[k]) + (1.0 - alpha) * float(learned_v)
        else:
            out_targets[k] = float(learned_v)

    blended["ordered_targets"] = out_targets
    return blended

# scoring + ranking
def recommend_tracks(
    music_library: List[Dict[str, Any]],
    user_music_prefs: Dict[str, Any],
    top_k: int = 5,
) -> List[Recommendation]:

    scored: List[Tuple[float, Dict[str, Any], ScoreBreakdown]] = []

    for track in music_library:
        breakdown = score_track(user_music_prefs, track)
        scored.append((breakdown.total, track, breakdown))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    results: List[Recommendation] = []

    for total, track, breakdown in top:
        results.append(
            Recommendation(
                track_id=str(track.get("track_id", "")),
                title=track.get("title", ""),
                artist=track.get("artist", ""),
                score=float(total),
                reason="; ".join(breakdown.explanation_bits[:3]),
                debug={
                    "parts": getattr(breakdown, "parts", {}),
                    "raw_parts": getattr(breakdown, "raw_parts", {}),
                },
            )
        )

    return results



def recommend_from_personality_json(
    music_csv_path: str | Path,
    personality_json_path: str | Path,
    mood_level: Optional[str] = None,
    top_k: int = 5,
) -> List[Recommendation]:

    library = load_music_library_csv(music_csv_path)
    profile = load_json(personality_json_path)
    user_profile = profile.get("user_profile") or profile
    base_prefs = build_user_music_prefs_from_personality(
         user_profile,
         mood=mood_level,
    )




    user_id = profile.get("firebase_uid") or "default_user"

    project_root = Path(__file__).resolve().parents[1]
    state = load_user_state(project_root, user_id)

    user_prefs = blend_user_prefs_with_memory(base_prefs, state.ordered_targets)
    user_prefs["memory"] = {
        "categorical_affinity": state.categorical_affinity,
        "history": state.history,
    }

    return recommend_tracks(library, user_prefs, top_k)


# Multiple users
def recommend_from_user_profile_dict(
    music_csv_path: str | Path,
    user_profile: Dict[str, Any],
    mood_level: Optional[str] = None,
    top_k: int = 5,
) -> List[Recommendation]:

    library = load_music_library_csv(music_csv_path)

    user_id = user_profile.get("firebase_uid") or "default_user"

    base_prefs = build_user_music_prefs_from_personality(
    user_profile.get("user_profile") or user_profile,
    mood_level=mood_level,
)
    if not isinstance(base_prefs, dict):
         base_prefs = {
              "ordered_targets": {
                   "energy": 0.5,
                   "tempo": 0.5,
                   "danceability": 0.5,
                   "intensity_type": 0.5,
                   "lyrics_intensity": 0.5,
                   },
                   "therapy_tag": None,
                   "emotional_tag": None,
                   "genre": None, 
                   "personality_line": None,
                   "mood_line": None,
                   "categorical_defaults": {},
                   "explanation_context": {},
                   "memory": {},
                   }


    project_root = Path(__file__).resolve().parents[1]
    state = load_user_state(project_root, user_id)

    user_prefs = blend_user_prefs_with_memory(base_prefs, state.ordered_targets or {})

    user_prefs["memory"] = {
        "categorical_affinity": state.categorical_affinity,
        "history": state.history,
        "top_signals": getattr(state, "top_signals", []) or [],
    }

    return recommend_tracks(library, user_prefs, top_k)
