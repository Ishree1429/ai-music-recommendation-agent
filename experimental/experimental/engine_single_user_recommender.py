import pandas as pd 
from music_agent_docs.src.personality_mapping import PERSONALITY_MUSIC_PREFS

def score_track(track, user_personality):
    score = 0
    
    for trait, details in user_personality.items():
        answer = details["answer"]
        
        if trait in PERSONALITY_MUSIC_PREFS:
            mapping = PERSONALITY_MUSIC_PREFS[trait]
            if answer in mapping:
                prefs = mapping[answer]
                
                
                for knob, expected_values in prefs.items():
                    if knob in track and str(track[knob]).lower() in expected_values:
                        score += 1

    return score

def recommend_music(user_json, csv_path="music_library.csv"):
    df = pd.read_csv(csv_path)
    user_personality = user_json["Personality"]

    df["score"] = df.apply(lambda row: score_track(row, user_personality), axis=1)
    df = df.sort_values(by="score", ascending=False)

    recommendations = df.head(5)

    return recommendations
