from __future__ import annotations

WEIGHTS = {
    "therapy_tag": 1.6,
    "emotional_tag": 1.2,
    "energy": 1.0,
    "tempo": 1.0,
    "genre": 1.3,
    "lyrics_intensity": 0.8,
    "danceability": 0.9,
    "intensity_type": 0.8,   
}

ENERGY_MAP = {
    "low": 0.0,
    "medium": 0.5,
    "high": 1.0,
}

TEMPO_MAP = {
    "slow": 0.0,
    "medium": 0.5,
    "fast": 1.0,
}

INTENSITY_MAP = {
    "ambient": 0.0, 
    "soft_piano": 0.2,
    "EDM_drops": 0.5, 
    "heavy_metal": 1.0, 
}
DANCEABILITY_MAP = {
    "low": 0.0,
    "medium": 0.5,
    "high": 1.0,
}


LYRICS_INTENSITY_MAP = {
    "instrumental": 0.0,
    "neutral_lyrics": 0.5, 
    "uplifting_positive_lyrics": 1.0, 
}


EMOJI_TO_SCORE = {
    "😍": 2,
    "😃": 1,
    "😐": 0,
    "🙁": -1,
    "😡": -2
}


LEARNING_RATE = 0.10

BLEND_ALPHA = 0.70

AFFINITY_BOOST = 0.20
