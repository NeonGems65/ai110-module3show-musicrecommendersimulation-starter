# 🎵 Music Recommender Simulation

## Project Summary

In this project, I built and explained a music recommender system that models how streaming platforms match tracks to users. 

The goal was to:
- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what the system gets right and wrong
- Reflect on how this mirrors real-world AI recommenders

This project implements a functional and object-oriented music recommender system that matches a user's taste profile to a catalog of songs.

By converting textual features (like genre and mood) and numerical/boolean features (like energy and acoustic preferences) into a compatibility score, it highlights how real-world algorithms turn data into personalized recommendations.

---

## How The System Works

The recommender system calculates a "compatibility score" between a user's preferences and each song in the catalog. 

- **Song Features Used**: We primarily use `genre`, `mood`, `energy`, and `acousticness`.
- **User Profile**: The system takes in the user's favorite genre, favorite mood, a target energy level (0.0 to 1.0), and a boolean preference for acoustic music (`likes_acoustic`).
- **Scoring Logic**:
  - Exact matches for categorical features are heavily prioritized. If the song's genre matches the user's favorite genre, it adds +2.0 to the score.
  - If the song's mood matches the user's favorite mood, it adds another +2.0.
  - For energy, we calculate the absolute difference between the user's target energy and the song's energy. A closer match yields a higher score (up to +1.0).
  - For acousticness, if the user likes acoustic music and the song is acoustic (>0.5), they get +0.5 points. Likewise, if the user doesn't like acoustic music and the song is not acoustic (<=0.5), they get +0.5 points.
- **Recommendation**: Songs are sorted in descending order based on their total score. The top `k` scoring songs are returned as recommendations along with a plain text explanation describing exactly which attributes matched.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loading songs from data/songs.csv...

Top recommendations:

Sunrise City - Score: 4.98
Because: This song matches your favorite genre (pop), and matches your mood (happy), and energy is very close to your target.

Rooftop Lights - Score: 2.96
Because: This song matches your mood (happy), and energy is very close to your target.

Gym Hero - Score: 2.87
Because: This song matches your favorite genre (pop), and energy is very close to your target.

Night Drive Loop - Score: 0.95
Because: This song energy is very close to your target.

Storm Runner - Score: 0.89
Because: This song energy is very close to your target.
```
*(Note: The sample output above is from the baseline functional implementation which primarily uses genre, mood, and energy).*

---

## Experiments You Tried

- **Weighting Categorical vs Numeric Attributes**: Initially, giving genre, mood, and energy equal weights resulted in songs with the correct energy but entirely wrong genres surfacing to the top. To fix this, genre and mood exact matches were boosted to +2.0 each, ensuring that the "vibe" strongly matches before considering energy proximity.
- **Adding Acousticness Preference**: Implemented a new preference feature (`likes_acoustic`) to filter songs based on their acoustic nature. This experiment showed how boolean preferences can act as secondary score boosters (+0.5 points) to refine results that otherwise tie in genre and mood.
- **Handling Non-Matches**: Tested providing user preferences where neither the genre nor the mood matched any song in the catalog. The system gracefully degraded, relying purely on the energy target to rank the closest sounding tracks and outputting a generic fallback explanation.

---

## Limitations and Risks

- **Filter Bubble Effect**: Because the system heavily rewards exact matches on genre and mood (+2.0 points each), it creates a strong "filter bubble" effect. A user might get trapped in a loop of only seeing the same genre, rarely discovering anything outside of their established preferences.
- **Over-Reliance on Hard Thresholds**: The acoustic preference operates on a hard threshold (0.5). A song with 0.49 acousticness is treated exactly the same as 0.0, potentially losing nuance in the musical composition.
- **Small Catalog Size**: With only a tiny dataset (10 songs), the variety is strictly limited. There isn't enough data for true serendipity or niche discovery.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender highlighted how algorithmic choices—such as the arbitrary weight assigned to a genre match versus an energy match—can fundamentally alter a user's experience. It turns subjective music tastes into a rigid mathematical ranking.

This also emphasized how algorithmic bias or unfairness can emerge unintentionally. By strongly prioritizing exact metadata matches, the system discourages exploration and traps users in filter bubbles. In real-world systems, this can lead to users never encountering diverse creators, disproportionately favoring mainstream genres at the expense of indie or less popular categories.
