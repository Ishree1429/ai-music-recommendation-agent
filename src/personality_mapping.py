PERSONALITY_MUSIC_PREFS = {
    "social_orientation": {
        "introvert": {
            "energy": {"low" : 2, "medium": 1, "high": -2}, 
            "danceability": {"low": 2, "medium": 0, "high": -2},
            "violence_style": {
                "ambient": 2, 
                "soft_piano": 2, 
                "edm_drops": -1, 
                "heavy_metal": -2,
            },
            "lyrics_intensity": {
                "instrumental": 2, 
                "neutral_lyrics": 1, 
                "uplifting_positive_lyrics": 0, 
            },
            "Emotional_tag": {
                    "calm": 2,
                    "uplifting": 1,
                    "sad" : 0, 
            }, 
        },
        "ambivert": {
                "energy": {"low": 1, "medium": 2, "high": 1},
            "danceability": {"low": 1, "medium": 2, "high": 1},
            "violence_style": {
                "ambient": 1,
                "soft_piano": 1,
                "edm_drops": 1,
                "heavy_metal": -1,
            },
            "lyrics_intensity": {
                "instrumental": 1,
                "neutral_lyrics": 1,
                "uplifting_positive_lyrics": 1,
            },
            "emotional_tag": {
                "calm": 1,
                "uplifting": 2,
                "sad": 0,
            },
            "therapy_tag": {
                "anxiety_relief": 1,
                "focus": 2,
                "sleep": 0,
                "mood_boost": 2,
            },
        },
        "extrovert": {
          "energy": {"low": -1, "medium": 1, "high": 2},
            "danceability": {"low": -1, "medium": 1, "high": 2},
            "violence_style": {
                "ambient": 0,
                "soft_piano": 0,
                "edm_drops": 2,
                "heavy_metal": 1,
            },
            "lyrics_intensity": {
                "instrumental": 0,
                "neutral_lyrics": 1,
                "uplifting_positive_lyrics": 2,
            },
            "emotional_tag": {
                "calm": 0,
                "uplifting": 2,
                "sad": -1,
            },
            "therapy_tag": {
                "anxiety_relief": 0,
                "focus": 1,
                "sleep": -1,
                "mood_boost": 2,
            },
        },
    },
    "structure_preference": {
          "structured": {
                "tempo": {"slow": 1, "medium": 2, "fast": 0},
            "genre": {
                "soft_indie": 1,
                "chillhop": 2,
                "cinematic_sountracks": 2,
                "gentle_experimental": 0,    
          },
          "lyrics_intensity": {
                  "instrumental": 2,
                "neutral_lyrics": 1,
                "uplifting_positive_lyrics": 1,
            },
            "therapy_tag": {
                "anxiety_relief": 2,
                "focus": 2,
                "sleep": 1,
                "mood_boost": 0,
            },
        },
        "flexible": { 
             "tempo": {"slow": 1, "medium": 1, "fast": 1},
            "genre": {
                "soft_indie": 1,
                "chillhop": 1,
                "cinematic_sountracks": 0,
                "gentle_experimental": 2,  
            },
            "lyrics_intensity": {
                "instrumental": 1,
                "neutral_lyrics": 1,
                "iplifting__positive_lyrics": 2,
            },
            "therapy_tag": {
                "anxiety_relief": 1,
                "focus": 1,
                "sleep": 0,
                "mood_boost": 2,
            },
        },
    "motivation_style" : {
        "growth_oriented": {
            "therapy_tag": {
                "anxiety_relief": 1,
                "focus": 2,      
                "sleep": 0,
                "mood_boost": 1,
            },
             "genre": {
               "soft_indie": 1,
                "chillhop": 2,
                "cinematic_sountracks": 2,
                "gentle_experimental": 1,
            },
            "lyrics_intensity": {
                "instrumental": 2,
                "neutral_lyrics": 1,
                "uplifting_positive_lyrics": 1,
            },
        },
        "outcome_oriented": {
               "therapy_tag": {
                "anxiety_relief": 0,
                "focus": 2,     
                "sleep": -1,
                "mood_boost": 2,
            },
            "energy": {"low": 0, "medium": 2, "high": 1},
            "tempo": {"slow": 0, "medium": 2, "fast": 1},
        },
    },
    "emotional_style": {
        "calm_resilient": {
            "energy": {"low": 1, "medium": 2, "high": 1},
            "emotional_tag": {
                "calm": 1,
                "uplifting": 2,
                "sad": 0,
            },
            "violence_style": {
                "ambient": 1,
                "soft_piano": 1,
                "edm_drops": 1,
                "heavy_metal": 0,
            },
        },
        "sensitive_stress_prone": {
         "energy": {"low": 2, "medium": 1, "high": -2},
            "emotional_tag": {
                "calm": 2,
                "uplifting": 1,
                "sad": -1,
            },
            "therapy_tag": {
                "anxiety_relief": 2,
                "focus": 1,
                "sleep": 2,
                "mood_boost": 1,
            },
            "violence_style": {
                "ambient": 2,
                "soft_piano": 2,
                "edm_drops": -1,
                "heavy_metal": -2,
            },
            "lyrics_intensity": {
                "instrumental": 2,
                "neutral_lyrics": 1,
                "upliftin_gpositive_lyrics": 1,
            },
        },
    },     
    "thinking_style" : {
        "analytical_logical": {
            "lyrics_intensity": {
                "instrumental": 2,   
                "neutral_lyrics": 1,
                "uplifting_positive_lyrics": 0,
            },
            "genre": {
                "soft_indie": 0,
                "chillhop": 2,
                "cinematic_sountracks": 2,
                "gentle_experimental": 0,
            },
            "therapy_tag": {
                "anxiety_relief": 1,
                "focus": 2,
                "sleep": 0,
                "mood_boost": 0,
            },
            "tempo": {"slow": 1, "medium": 2, "fast": 0},
        },
        "creative_imaginative" : {
              "lyrics_intensity": {
                "instrumental": 1,
                "neutral_lyrics": 1,
                "uplifting_positive_lyrics": 2,
            },
            "genre": {
                "soft_indie": 2,
                "chillhop": 1,
                "cinematic_sountracks": 1,
                "gentle_experimental": 2,
            },
            "therapy_tag": {
                "anxiety_relief": 1,
                "focus": 1,
                "sleep": 0,
                "mood_boost": 2,
            },
            "tempo": {"slow": 1, "medium": 1, "fast": 1},
        },
    },
    "learning_style" : {
        "visual": {
            "genre": {
                "soft_indie": 0,
                "chillhop": 1,
                "cinematic_sountracks": 2,        
                "gentle_experimental": 1,
            },
            "lyrics_intensity": {
                "instrumental": 2,
                "neutral_lyrics": 1,
                "uplifting_positive_lyrics": 0,
            },
        },
        "auditory" : {
            "lyrics_intensity": {
                "instrumental": 0,
                "neutral_lyrics": 1,
                "upliftng_positive_lyrics": 2,        
            },
            "emotional_tag": {
                "calm": 1,
                "uplifting": 2,
                "sad": 0,
            },
        },
        "reading_writing" : {
               "lyrics_intensity": {
                "instrumental": 2,
                "neutral_lyrics": 1,
                "uplifting_positive_lyrics": 0,
            },
            "therapy_tag": {
                "anxiety_relief": 1,
                "focus": 2,
                "sleep": 0,
                "mood_boost": 0,
            },
        },
        "kinesthetic": {
                "energy": {"low": 0, "medium": 1, "high": 2},
            "danceability": {"low": 0, "medium": 1, "high": 2},
            "tempo": {"slow": 0, "medium": 1, "fast": 2},
            "therapy_tag": {
                "anxiety_relief": 0,
                "focus": 1,
                "sleep": -1,
                "mood_boost": 2,
            },
        },
    },
    "risk_novelty_orientation" : {
           "stability_seeker" : { 
                  "genre": {
                "soft_indie": 2,
                "chillhop": 2,
                "cinematic_sountracks": 1,
                "gentle_experimental": -1,
            },
            "tempo": {"slow": 1, "medium": 2, "fast": 0},
            "violence_style": {
                "ambient": 2,
                "soft_piano": 2,
                "edm_drops": -1,
                "heavy_metal": -2,
            },
        },
        "novelty_seeker" : {
               "genre": {
                "soft_indie": 1,
                "chillhop": 1,
                "cinematic_sountracks": 1,
                "gentle_experimental": 2,  # likes new / unusual
            },
            "tempo": {"slow": 0, "medium": 1, "fast": 2},
            "violence_style": {
                "ambient": 0,
                "soft_piano": 0,
                "edm_drops": 2,
                "heavy_metal": 1,
            },
        },
    },
    "values_orientation" : {
        "individualist" : {
            "genre": {
                "soft_indie": 2,
                "chillhop": 1,
                "cinematic_sountracks": 1,
                "gentle_experimental": 1,
            },
            "lyrics_intensity": {
                "instrumental": 1,
                "neutral_lyrics": 1,
                "uplifting_positive_lyrics": 2,
            },
        },
        "collectivist" : {
            "energy": {"low": 0, "medium": 2, "high": 1},
            "danceability": {"low": 0, "medium": 1, "high": 2},
            "emotional_tag": {
                "calm": 0,
                "uplifting": 2,
                "sad": -1,
            },
            "therapy_tag": {
                "anxiety_relief": 0,
                "focus": 1,
                "sleep": 0,
                "mood_boost": 2,
            },
        },
    },
},
}
