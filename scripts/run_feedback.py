from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from src.memory_store import load_user_state, save_user_state
from src.feedback import apply_feedback


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_id", required=True)
    parser.add_argument("--track_id", required=True)
    parser.add_argument("--emoji", required=True)

    parser.add_argument("--csv_path", default="data/music_library.csv")
    parser.add_argument("--csv", default=None)  # optional alias

    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]

    rel_csv = args.csv if args.csv is not None else args.csv_path
    csv_path = project_root / rel_csv

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    if "track_id" not in df.columns:
        raise ValueError("Your CSV must contain a 'track_id' column for feedback learning.")

    match = df[df["track_id"].astype(str) == str(args.track_id)]
    if match.empty:
        raise ValueError(f"track_id '{args.track_id}' not found in CSV.")

    track = match.iloc[0].to_dict()

    state = load_user_state(project_root, args.user_id)

    before_targets = dict(getattr(state, "ordered_targets", {}) or {})
    before_cat = dict(getattr(state, "categorical_affinity", {}) or {})
    before_signals = list(getattr(state, "top_signals", []) or [])

    state = apply_feedback(state, track, args.emoji)

    after_targets = dict(getattr(state, "ordered_targets", {}) or {})
    after_cat = dict(getattr(state, "categorical_affinity", {}) or {})
    after_signals = list(getattr(state, "top_signals", []) or [])

  
    saved_path = save_user_state(project_root, state)

    print("\nOrdered targets BEFORE:", before_targets)
    print("Ordered targets AFTER :", after_targets)

    print("\nCategorical affinity BEFORE:", before_cat)
    print("Categorical affinity AFTER :", after_cat)

    print("\nTop signals BEFORE:", before_signals)
    print("Top signals AFTER :", after_signals)

    print(f"\n✅ Feedback saved for user '{args.user_id}' -> {saved_path}")

    history = getattr(state, "history", [])
    if history:
        print(f"Last event: {history[-1]}")


if __name__ == "__main__":
    main()
