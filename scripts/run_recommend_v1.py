# run_recommend_v1.py
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.recommender import recommend_from_user_profile_dict
from src.memory_store import load_user_state


def _load_users(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        users = []
        for user_id, payload in data.items():
            payload = dict(payload)
            payload["user_id"] = payload.get("user_id", user_id)
            users.append(payload)
        return users

    raise ValueError("user_profiles.json must be a list or dict.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default="data/music_library.csv")
    parser.add_argument("--profiles_path", default="data/users/user_profiles.json")
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--mood", default=None)  # Week 4 mood input
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]

    music_csv_path = str(project_root / args.csv_path)
    user_profiles_path = str(project_root / args.profiles_path)

    users = _load_users(user_profiles_path)

    for user in users:
        user_id = user.get("firebase_uid", "unknown")
        user["user_id"] = user_id
        user_name = (user.get("user_profile") or {}).get("name", "")


        recs = recommend_from_user_profile_dict(
            music_csv_path=music_csv_path,
            user_profile=user,
            top_k=args.top_k,
            mood_level=args.mood,   
            )

        print("\n" + "=" * 40)
        print(f"USER: {user_id} | {user_name} | mood={args.mood or 'none'}")
        print("=" * 40)
        print("\n=== TOP RECOMMENDATIONS ===")
        for i, r in enumerate(recs, 1):
            print(f"\n{i}. {r.track_id} | {r.title}")
            print(f"   score: {r.score:.3f}")
            print(f"   why: {r.reason}")


if __name__ == "__main__":
    main()





        