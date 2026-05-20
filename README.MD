# AI Music Recommendation Agent

An explainable, learning-enabled music recommendation **agent** that personalizes therapeutic music suggestions using user personality, mood signals, and feedback loops.

Not a static playlist generator. The agent:
- Builds a per-user state
- Scores tracks using interpretable, personality-aware features
- Learns from feedback over time (adaptive preference updates)
- Produces human-readable explanations for every recommendation

---

## Why this matters

Most recommenders optimize a black-box score. This one is structured like a real-world recommendation system used in wellness and mental-health contexts — where **explainability**, **modularity**, and **incremental learning** matter as much as raw accuracy.

The architecture intentionally separates: production code (`src/`), CLI entry points (`scripts/`), early prototypes (`experimental/`), and design notes (`notes/`). The goal was to build it the way a small AI team would actually ship it.

---

## Architecture

src/
├── recommender.py        # Orchestrates the full recommendation flow
├── scoring.py            # Mood + personality + emotional-tag scoring with explainability
├── personality_mapper.py # Maps personality traits → music preferences
├── user_state.py         # Runtime user representation
├── feedback.py           # Processes user feedback signals
├── learning.py           # Adaptive preference updates (online learning)
├── memory_store.py       # Persistence layer for learned preferences
└── config.py             # Central configuration and paths
scripts/
├── run_recommend_v1.py   # CLI: generate recommendations
└── run_feedback.py       # CLI: simulate user feedback
data/
├── users/                # User profiles
├── user_memory/          # Stored feedback and learned preferences
└── music_library.csv     # Track feature dataset

---

## How to run

```bash
# Generate recommendations
python -m scripts.run_recommend_v1 --user-id UID3 --mood sad

# Give feedback on a recommended track
python -m scripts.run_feedback --user-id UID3 --track-id t_012 --emoji "😍"

# Run again — recommendations now adapt to learned preferences
python -m scripts.run_recommend_v1 --user-id UID3 --mood calm
```

---

## What this project demonstrates

- **Recommender system fundamentals** with interpretable feature-based scoring
- **Explainable AI** — every recommendation comes with a reason
- **Adaptive learning** via feedback loops and persistent memory
- **Agent-style design** — state, scoring, learning, and memory as separate, composable modules
- **Clean Python architecture** — production code, experiments, and docs cleanly separated

---

## Future extensions

- Replace heuristic scoring with learned ML models
- Add audio or lyric embeddings (FAISS-based retrieval)
- Integrate Spotify or streaming APIs
- Deploy as an inference API

---

**Built by:** [Tanushree Sharma](https://github.com/Ishree1429) — Master's in Data Science, Illinois Tech - {SOULOXY- AI Developer Intern}
