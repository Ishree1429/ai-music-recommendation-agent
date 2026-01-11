🎵 Music Recommendation Agent
Mood-Aware • Personality-Driven • Learning-Enabled

-->> Project Overview

This project implements an AI-driven music recommendation agent that suggests therapeutic and emotionally aligned music tracks based on:
1) User personality traits
2) Current mood
3) Past listening feedback
4) Adaptive preference learning
The system is designed to resemble a real-world recommender pipeline used in wellness and mental-health applications, with a strong focus on explainability, modularity, and incremental learning.

-->> Key Idea
Recommend music that fits not just the mood — but the person behind the mood — and explain why.
Unlike static playlists, this agent:
1) Builds a user state
2) Scores tracks using interpretable features
3) Learns from feedback over time
4) Produces human-readable explanations

-->> Project Structure

music_agent_docs/
├── data/
│   ├── user_memory/               ➢Stored feedback & learned preferences
│   ├── users/
│   │   ├── sample_user.json       ➢Single demo user
│   │   └── user_profiles.json     ➢Multiple user profiles
│   └── music_library.csv          ➢Music feature dataset
│
├── experimental/
│   └── engine_single_user_*.py    ➢Early single-user prototype (Week 2)
│
├── notes/
│   ├── music_knobs.md             ➢Feature design & tuning notes
│   └── user_persona.md            ➢Persona definitions & rationale
│
├── scripts/
│   ├── run_recommend_*.py         ➢CLI for generating recommendations
│   └── run_feedback.py            ➢CLI for simulating user feedback
│
├── src/
│   ├── config.py                  ➢Central configuration & paths
│   ├── recommender.py             ➢Core recommendation pipeline
│   ├── scoring.py                 ➢Track scoring logic
│   ├── personality_mapper.py      ➢Personality → preference mapping
│   ├── user_state.py              ➢Runtime user representation
│   ├── feedback.py                ➢Feedback processing
│   ├── learning.py                ➢Adaptive preference updates
│   └── memory_store.py            ➢Persistence layer for user memory
│
└── README.md


-->> How to Run: 
All commands should be run from the music_agent_docs/ directory.
❖ Generate music recommendations
- Example: generate recommendations for a user based on their mood.
        python -m scripts.run_recommend_v1 \ --user-id UID3 \ --mood sad
What this does:
1) Loads user profile (UID3) from data/users/user_profiles.json
2) Reads music features from data/music_library.csv
3) Applies personality + mood-aware scoring
4) Prints ranked track recommendations with explanations

❖ Provide feedback on a recommended track
- Example: user reacts positively to a recommended track.
       python -m scripts.run_feedback \ --user-id UID3 \ --track-id t_012 \ --emoji "😍"
What this does:
1) Records feedback for UID3
2) Updates preference weights (learning step)
3) Stores updated memory in data/user_memory/
4) Influences future recommendations

❖ Run recommendation again (after learning)
 - Example: 
    python -m scripts.run_recommend_v1 \ --user-id UID3 \ --mood calm
Now the recommendations are slightly different, because the system has learned from feedback.



-->> Module Responsibilities
1) src/recommender.py
- Orchestrates the full recommendation flow
- Connects user state, scoring, and learning
2) src/scoring.py
- Computes track scores using:
- mood alignment
- energy balance
- emotional tags
- personality compatibility
- Produces explainable score breakdowns
3) src/learning.py
- Updates preferences based on feedback
- Simulates online learning behavior
4) src/memory_store.py
- Persists learned preferences
- Enables personalization across runs
5) scripts/
- Entry points for running the system
- Keeps business logic out of notebooks or ad-hoc scripts

-->> Experimental Code
❖ experimental/engine_single_user_recommender.py
1) Early Week-2 prototype
2) Built for a single demo user
3) Kept intentionally for:
4) learning history
5) comparison with final architecture
6) Not used by the production CLI

-->> Notes & Design Artifacts
❖ notes/music_knobs.md
1) Documents all controllable music features
2) Explains why each feature matters
3) Shows interpretability & design thinking

❖ notes/user_persona.md
1) Defines user personas
2) Explains personality-to-music mapping logic
3) These files are not code, but they reflect system design maturity.

-->> What This Project Demonstrates
1) Recommender system fundamentals
2) Feature-based scoring (ML-style thinking)
3) Explainable AI
4) Adaptive learning via feedback loops
5) Clean Python architecture
6) CLI-driven execution
7) Clear separation of:
    - production code
    - experiments
    - documentation

-->> Future Extensions
1) Replace heuristic scoring with ML models
2) Add embeddings (audio or lyrics)
3) Integrate Spotify or streaming APIs
4) Deploy as a web or mobile service

-->> Final Note 
AI Music Recommendation Agent is an end-to-end, explainable recommendation system that demonstrates how artificial intelligence can personalize music experiences using user personality, mood signals, and feedback-driven learning.
The project focuses on:
1) Translating human emotions and personality traits into interpretable features
2) Designing a transparent scoring-based recommendation engine
3) Simulating learning and memory to adapt recommendations over time
4) Structuring the system like a real-world AI product, with clean separation between core logic, experiments, and documentation
This agent reflects practical AI system design, not just model usage — showing how data, logic, learning, and user context come together to build a personalized recommendation experience.




