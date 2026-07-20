# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatcher 2.0 (Acoustic-Aware)**

---

## 2. Intended Use  

This recommender is designed to simulate how music recommendation algorithms work by taking explicit user preferences and surfacing matching tracks. 
It is intended for educational exploration to highlight how numerical and categorical data can be combined to score items. It assumes the user explicitly provides their favorite genre, favorite mood, target energy level, and an acoustic preference.

---

## 3. How the Model Works  

The model calculates a "compatibility score" for each song based on four main features: genre, mood, energy, and acousticness.
First, it checks if the song's genre perfectly matches the user's favorite genre. If it does, the song gets a large boost (+2 points). It does the exact same for mood (+2 points).
Next, it calculates an energy score. The closer the song's energy is to the user's target energy, the more points it gets (up to +1 point).
Finally, it applies an acousticness bonus. If the user likes acoustic music and the song is primarily acoustic (acousticness > 0.5), or if they dislike it and the song is not acoustic (acousticness <= 0.5), it adds a +0.5 point bonus.
All these points are added together, and the songs with the highest scores are recommended to the user.

---

## 4. Data  

The dataset is a tiny, curated catalog of 10 fictional songs. 
It represents a handful of genres including pop, lofi, rock, ambient, jazz, synthwave, and indie pop. 
Because the dataset is extremely small, there are massive gaps in musical representation. Many global genres, languages, and complex moods are completely missing from the catalog.

---

## 5. Strengths  

The model works exceptionally well for users whose tastes precisely align with the metadata tags of the catalog (e.g., someone who explicitly wants "happy pop").
Because genre and mood matches are heavily weighted, the model accurately surfaces songs that capture the exact "vibe" the user is looking for. The added acoustic preference allows users to distinguish between heavily produced vs. natural sounding tracks within the same genre.

---

## 6. Limitations and Bias 

The biggest limitation is the risk of a "filter bubble". Because the system heavily rewards exact matches on genre and mood, it consistently recommends the same type of music and traps the user in a narrow loop, never suggesting slightly different or novel genres.
Additionally, the hard threshold for acousticness (0.5) is arbitrary and might fail to represent songs that blend acoustic and electronic elements evenly. The system does not understand lyrics, audio composition, or cultural context—it strictly looks at the tags.

---

## 7. Evaluation  

The recommender was evaluated manually and via automated unit tests.
Testing against user profiles with specific acoustic preferences successfully bumped tracks that satisfied those preferences above ties. The automated tests verified that the scoring mechanism correctly sorts tracks with multiple matching attributes higher than tracks with fewer matching attributes.

---

## 8. Future Work  

To improve the model, we could introduce a "serendipity score" or randomness factor to periodically recommend a song outside the user's exact preferred genre to break the filter bubble. 
We could also incorporate more complex features like `danceability` and `valence` into the scoring algorithm to create a more holistic matching system. Modifying the acousticness scoring to be continuous rather than a hard boolean threshold would also improve nuance.

---

## 9. Personal Reflection  

Building this simulation changed how I view the music recommendations I receive daily. It made it clear that algorithms don't actually "understand" my taste; they just perform mathematical distance calculations on metadata. Seeing how a minor decision, like assigning +0.5 points for an acousticness match, can drastically alter the final ranking demonstrated how developers embed their own subjective priorities into algorithms, potentially hiding great music from the user if it falls on the wrong side of an arbitrary threshold.
