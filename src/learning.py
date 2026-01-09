from __future__ import annotations

from typing import Any, Dict

from .config import EMOJI_TO_SCORE, LEARNING_RATE

ORDERED_KEYS = ["energy", "tempo", "danceability", "intensity_type", "lyrics_intensity"]
CATEGORICAL_KEYS = ["therapy_tag", "emotional_tag", "genre"]

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def update_ordered_targets(
    ordered_targets: Dict[str, float],
    track_numeric: Dict[str, float],
    emoji: str,
) -> Dict[str, float]:
   
    s = EMOJI_TO_SCORE.get(emoji, 0)
    if s == 0:
        return ordered_targets

    # normalize to [-1, 1]
    direction = max(-1.0, min(1.0, s / 2.0))

    out = dict(ordered_targets or {})
    for k in ORDERED_KEYS:
        if k not in track_numeric:
            continue

        old = float(out.get(k, 0.5))
        tv = float(track_numeric[k])

    
        new = old + (LEARNING_RATE * direction) * (tv - old)
        out[k] = clamp01(new)

    return out

def update_categorical_affinity(
    categorical_affinity: Dict[str, Dict[str, float]],
    track: Dict[str, Any],
    emoji: str,
) -> Dict[str, Dict[str, float]]:
    
    s = EMOJI_TO_SCORE.get(emoji, 0)
    if s == 0:
        return categorical_affinity

    out: Dict[str, Dict[str, float]] = {}
    for k, m in (categorical_affinity or {}).items():
        out[k] = dict(m)

    for cat_key in CATEGORICAL_KEYS:
        v = (track.get(cat_key) or "").strip().lower()
        if not v:
            continue
        out.setdefault(cat_key, {})
        out[cat_key][v] = float(out[cat_key].get(v, 0.0)) + float(s)

    return out
