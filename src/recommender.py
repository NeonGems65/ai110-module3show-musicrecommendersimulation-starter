from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = []
        for song in self.songs:
            score = 0.0
            if user.favorite_genre == song.genre:
                score += 2.0
            if user.favorite_mood == song.mood:
                score += 2.0
            
            energy_diff = abs(user.target_energy - song.energy)
            score += max(0.0, 1.0 - energy_diff)
            
            if user.likes_acoustic and song.acousticness > 0.5:
                score += 0.5
            elif not user.likes_acoustic and song.acousticness <= 0.5:
                score += 0.5

            scored.append((song, score))
            
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if user.favorite_genre == song.genre:
            reasons.append(f"matches your favorite genre ({song.genre})")
        if user.favorite_mood == song.mood:
            reasons.append(f"matches your mood ({song.mood})")
        
        energy_diff = abs(user.target_energy - song.energy)
        if energy_diff < 0.2:
            reasons.append("energy is very close to your target")
            
        if user.likes_acoustic and song.acousticness > 0.5:
            reasons.append("has the acoustic feel you like")
        elif not user.likes_acoustic and song.acousticness <= 0.5:
            reasons.append("avoids high acousticness as you prefer")

        if not reasons:
            return "This song doesn't strongly match your specific preferences."
            
        explanation = "This song " + ", and ".join(reasons) + "."
        return explanation[0].upper() + explanation[1:]

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if user_prefs.get('genre') == song['genre']:
        score += 2.0
        reasons.append(f"matches your favorite genre ({song['genre']})")
    
    if user_prefs.get('mood') == song['mood']:
        score += 2.0
        reasons.append(f"matches your mood ({song['mood']})")

    if 'energy' in user_prefs:
        energy_diff = abs(user_prefs['energy'] - song['energy'])
        energy_score = max(0.0, 1.0 - energy_diff)
        score += energy_score
        if energy_score > 0.8:
            reasons.append("energy is very close to your target")

    if not reasons:
        reasons.append("doesn't strongly match your preferences")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        if reasons == ["doesn't strongly match your preferences"]:
            explanation = "This song doesn't strongly match your preferences."
        else:
            explanation = "This song " + ", and ".join(reasons) + "."
            explanation = explanation[0].upper() + explanation[1:]
        scored_songs.append((song, score, explanation))
    
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
