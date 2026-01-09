# src/scoring.py
from __future__ import annotations
from src.config import AFFINITY_BOOST

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

from src.config import (
    WEIGHTS,
    ENERGY_MAP,
    TEMPO_MAP,
    INTENSITY_MAP, 
    DANCEABILITY_MAP,
    LYRICS_INTENSITY_MAP,
    EMOJI_TO_SCORE, 

)


def _norm(s: Any) -> str:
    if s is None:
        return ""
    return str(s).strip().lower().replace("-", "_").replace(" ", "_")

def _split_tags(value: Any) -> List[str]:
    
    if value is None:
        return []
    text = str(value).strip()
    if not text:
        return []

    seps = [",", "|", "/", ";"]
    for sep in seps:
        text = text.replace(sep, ",")
    tokens = [_norm(t) for t in text.split(",")]
    return [t for t in tokens if t]

def _map_ordinal(value: Any, mapping: Dict[str, float]) -> float:
    key = _norm(value)
    if not key:
        return 0.5
    return float(mapping.get(key, 0.5))

def _match_score(user_pref: Any, track_value: Any) -> float:
   
    user_tags = _split_tags(user_pref) if isinstance(user_pref, (list, tuple, set)) is False else [_norm(x) for x in user_pref]
    if not user_tags:
        user_tags = _split_tags(user_pref)

    track_tags = _split_tags(track_value)

    if not track_tags:
        track_single = _norm(track_value)
        return 1.0 if (track_single and track_single in user_tags) else 0.0

    overlap = set(user_tags).intersection(set(track_tags))
    return 1.0 if overlap else 0.0

def _scaled_distance(a: float, b: float) -> float:
    a = max(0.0, min(1.0, a))
    b = max(0.0, min(1.0, b))
    return 1.0 - abs(a - b)

# scoring

@dataclass
class ScoreBreakdown:
    total: float
    parts: Dict[str, float]          
    raw_parts: Dict[str, float]     
    explanation_bits: List[str]      

def score_track(
    user_music_prefs: Dict[str, Any],
    track: Dict[str, Any],
) -> ScoreBreakdown:
    parts: Dict[str, float] = {}
    raw: Dict[str, float] = {}
    why: List[str] = []

    # ordered targets (numeric)
    ordered = user_music_prefs.get("ordered_targets") or {}

    trk_energy = _map_ordinal(track.get("energy"), ENERGY_MAP)
    trk_tempo = _map_ordinal(track.get("tempo"), TEMPO_MAP)
    trk_dance = _map_ordinal(track.get("danceability"), DANCEABILITY_MAP)
    trk_intensity = _map_ordinal(track.get("intensity_type"), INTENSITY_MAP)
    trk_lyrics = _map_ordinal(track.get("lyrics_intensity"), LYRICS_INTENSITY_MAP)

    tgt_energy = float(ordered.get("energy", 0.5))
    tgt_tempo = float(ordered.get("tempo", 0.5))
    tgt_dance = float(ordered.get("danceability", 0.5))
    tgt_intensity = float(ordered.get("intensity_type", 0.5))
    tgt_lyrics = float(ordered.get("lyrics_intensity", 0.5))

    def closeness(a: float, b: float) -> float:
        return max(0.0, 1.0 - abs(a - b))

    raw_energy = closeness(trk_energy, tgt_energy)
    raw["energy"] = raw_energy
    parts["energy"] = raw_energy * WEIGHTS.get("energy", 1.0)
    if raw_energy >= 0.8:
        why.append("energy closely matches your preference")

    raw_tempo = closeness(trk_tempo, tgt_tempo)
    raw["tempo"] = raw_tempo
    parts["tempo"] = raw_tempo * WEIGHTS.get("tempo", 1.0)
    if raw_tempo >= 0.8:
        why.append("tempo fits what you need right now")

    raw_dance = closeness(trk_dance, tgt_dance)
    raw["danceability"] = raw_dance
    parts["danceability"] = raw_dance * WEIGHTS.get("danceability", 1.0)
    if raw_dance >= 0.8:
        why.append("danceability aligns well")

    raw_intensity = closeness(trk_intensity, tgt_intensity)
    raw["intensity_type"] = raw_intensity
    parts["intensity_type"] = raw_intensity * WEIGHTS.get("intensity_type", 1.0)
    if raw_intensity >= 0.8:
        why.append("intensity style is a good fit")

    raw_lyrics = closeness(trk_lyrics, tgt_lyrics)
    raw["lyrics_intensity"] = raw_lyrics
    parts["lyrics_intensity"] = raw_lyrics * WEIGHTS.get("lyrics_intensity", 1.0)
    if raw_lyrics >= 0.8:
        why.append("lyrics intensity fits your style")

    # categorical match (0/1)
    raw_therapy = _match_score(user_music_prefs.get("therapy_tag"), track.get("therapy_tag"))
    raw["therapy_tag"] = raw_therapy
    parts["therapy_tag"] = raw_therapy * WEIGHTS.get("therapy_tag", 1.0)
    if raw_therapy == 1.0:
        why.append("therapy goal matches (focus/sleep/anxiety relief)")

    raw_emotion = _match_score(user_music_prefs.get("emotional_tag"), track.get("emotional_tag"))
    raw["emotional_tag"] = raw_emotion
    parts["emotional_tag"] = raw_emotion * WEIGHTS.get("emotional_tag", 1.0)
    if raw_emotion == 1.0:
        why.append("emotional vibe matches your mood")

    raw_genre = _match_score(user_music_prefs.get("genre"), track.get("genre"))
    raw["genre"] = raw_genre
    parts["genre"] = raw_genre * WEIGHTS.get("genre", 1.0)
    if raw_genre == 1.0:
        why.append("genre matches your taste")

    # ---------- memory ----------
    memory = user_music_prefs.get("memory", {}) or {}
    affinity = memory.get("categorical_affinity", {}) or {}

    # repeat penalty (exploration)
    history = (memory.get("history") or [])
    seen_ids = {h.get("track_id") for h in history if isinstance(h, dict)}

    if track.get("track_id") in seen_ids:
        parts["repeat_penalty"] = -0.25
        why.insert(0, "you've seen this before, so we're ranking it slightly lower")
    else:
        parts["repeat_penalty"] = 0.0

    # categorical affinity bonus
    affinity_bonus = 0.0
    affinity_bits: List[str] = []

    for cat_key in ["therapy_tag", "emotional_tag", "genre"]:
        track_val = _norm(track.get(cat_key))
        if not track_val:
            continue

        score_map = affinity.get(cat_key, {}) or {}
        raw_aff = float(score_map.get(track_val, 0.0))

        norm_aff = max(-1.0, min(1.0, raw_aff / 5.0))
        delta = AFFINITY_BOOST * norm_aff
        affinity_bonus += delta

        if norm_aff >= 0.4:
            affinity_bits.append(f"you often like {track_val} ({cat_key})")
        elif norm_aff <= -0.4:
            affinity_bits.append(f"you usually avoid {track_val} ({cat_key})")

    parts["memory_affinity_bonus"] = affinity_bonus

    # learning explanation
    final_why: List[str] = []
    if affinity_bits:
        final_why.append(affinity_bits[0])
    elif ordered:
        final_why.append("based on your past feedback, your recommendations are adapting over time")

    personality_line = user_music_prefs.get("personality_line")
    if personality_line:
        final_why.append(str(personality_line)) 

    mood_line = user_music_prefs.get("mood_line")
    if mood_line:
        final_why.append(str(mood_line))

    if not final_why:
        final_why = ["overall closest match for you"]
    
    why = final_why[:3]
    total = sum(parts.values())

        
    return ScoreBreakdown(total=total, parts=parts, raw_parts=raw, explanation_bits=why)

def build_user_music_prefs_from_personality(
    personality_profile: Dict[str, Any],
    mood_level: Optional[str] = None,
) -> Dict[str, Any]:

    # Final output dict
    user_music_prefs: Dict[str, Any] = {}
    if "Personality" in personality_profile and isinstance(personality_profile["Personality"], dict):
        personality_profile = personality_profile["Personality"]

    emo_style = _norm(
        (personality_profile.get("Emotional_Style") or {}).get("answer", "")
    )
    if "stress" in emo_style or "sensitive" in emo_style:
        user_music_prefs["energy"] = "low"
        user_music_prefs["tempo"] = "slow"
        user_music_prefs["emotional_tag"] = "calm"
        user_music_prefs["therapy_tag"] = "anxiety_relief"
        user_music_prefs["intensity_type"] = "ambient"
        user_music_prefs["lyrics_intensity"] = "instrumental"

    thinking_style = _norm(
        (personality_profile.get("Thinking_Style") or {}).get("answer", "")
    )
    if "creative" in thinking_style or "imaginative" in thinking_style:
        user_music_prefs["genre"] = "cinematic_soundtracks"
        user_music_prefs["emotional_tag"] = user_music_prefs.get("emotional_tag", "uplifting")

    # mood -----if 
    if mood_level:
        ml = _norm(mood_level)
        if ml in {"anxious", "stress", "stressed"}:
            user_music_prefs["therapy_tag"] = "anxiety_relief"
            user_music_prefs["emotional_tag"] = "calm"
        elif ml in {"sad", "low"}:
            user_music_prefs["therapy_tag"] = "mood_boost"
            user_music_prefs["emotional_tag"] = "uplifting"
        elif ml in {"focus", "focused"}:
            user_music_prefs["therapy_tag"] = "focus"
            user_music_prefs["lyrics_intensity"] = "instrumental"

   #new - for 
    user_music_prefs.setdefault("ordered_targets", {})
    ordered = user_music_prefs["ordered_targets"]
    def ans(trait: str) -> str:
        v = personality_profile.get(trait, {})
        if isinstance(v, dict):
            return str(v.get("answer", "")).strip()
        return str(v).strip()
    social = ans("Social_Orientation").lower()
    thinking = ans("Thinking_Style").lower()
    emotional = ans("Emotional_Style").lower()
    learning = ans("Learning_Style").lower()
    
    if social == "introvert":
        user_music_prefs["personality_line"] = (
        "because you’re more introverted, calmer tracks suit you better"
    )
    elif social == "extrovert":
        user_music_prefs["personality_line"] = (
        "because you’re more extroverted, higher-energy tracks fit you well"
    )
    elif social == "ambivert":
        user_music_prefs["personality_line"] = (
        "because you’re balanced socially, moderate energy tracks fit well"
    )
    if mood_level:
        ml = _norm(mood_level)
    if ml in {"anxious", "stress", "stressed"}:
        user_music_prefs["mood_line"] = (
            "since you’re feeling anxious, this leans toward calm / anxiety relief"
        )
    elif ml in {"sad", "low"}:
        user_music_prefs["mood_line"] = (
            "since you’re feeling low, this leans toward uplifting / mood boost"
        )
    elif ml in {"focus", "focused"}:
        user_music_prefs["mood_line"] = (
            "since you want focus, this leans toward instrumental / low-distraction tracks"
        )
    elif ml in {"sleep", "rest"}:
        user_music_prefs["mood_line"] = (
            "since you want sleep, this leans toward softer / sleep-friendly tracks"
        )
    ordered.setdefault("energy", 0.5)
    ordered.setdefault("tempo", 0.5)
    ordered.setdefault("danceability", 0.5)
    ordered.setdefault("intensity_type", 0.4)
    ordered.setdefault("lyrics_intensity", 0.5)
    
    if social == "introvert":
        ordered["energy"] = 0.25
        ordered["tempo"] = 0.30
        ordered["danceability"] = 0.25
    elif social == "extrovert":
        ordered["energy"] = 0.75
        ordered["tempo"] = 0.70
        ordered["danceability"] = 0.80
    elif social == "ambivert":
        ordered["energy"] = 0.55
        ordered["tempo"] = 0.55
        ordered["danceability"] = 0.55
    
    if thinking in {"analytical", "logical"}:
        ordered["lyrics_intensity"] = 0.45
        ordered["intensity_type"] = 0.35
    elif thinking in {"creative", "intuitive", "holistic"}:
        ordered["lyrics_intensity"] = 0.60
        ordered["intensity_type"] = 0.50

    if emotional in {"rational", "balanced"}:
        ordered["intensity_type"] = min(0.45, ordered["intensity_type"])
    elif emotional in {"expressive", "empathetic"}:
        ordered["intensity_type"] = max(0.55, ordered["intensity_type"])

    if learning == "visual":
        ordered["intensity_type"] = max(0.50, ordered["intensity_type"])
        return user_music_prefs
