import sqlite3
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DB_PATH = Path("data/indie_signal.db")


def get_all_artists():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM artists")
    rows = cursor.fetchall()
    connection.close()
    return [row[0] for row in rows]


def build_similarity_model(artist_tags):
    names = list(artist_tags.keys())
    tag_strings = list(artist_tags.values())
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(tag_strings)
    similarity = cosine_similarity(matrix)
    return names, similarity


def get_recommendations(target_artist, artist_tags, top_n=5):
    if target_artist not in artist_tags:
        return []
    names, similarity = build_similarity_model(artist_tags)
    if target_artist not in names:
        return []
    index = names.index(target_artist)
    scores = list(enumerate(similarity[index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    recommendations = []
    for i, score in scores:
        if names[i].lower() != target_artist.lower() and score > 0:
            recommendations.append({
                "name": names[i],
                "score": str(round(float(score) * 100)) + "%"
            })
        if len(recommendations) >= top_n:
            break
    return recommendations


def get_taste_recommendations(favorite_artists, artist_tags, top_n=10):
    """
    Build a taste profile from a list of favorite artists and recommend
    similar artists not already in the favorites list.
    """
    if not favorite_artists or not artist_tags:
        return []

    combined_tags = " ".join([
        artist_tags[name]
        for name in favorite_artists
        if name in artist_tags
    ])

    if not combined_tags.strip():
        return []

    favorites_lower = [f.lower() for f in favorite_artists]

    all_names = list(artist_tags.keys())
    all_tag_strings = list(artist_tags.values())

    all_names.append("__taste_profile__")
    all_tag_strings.append(combined_tags)

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(all_tag_strings)
    similarity = cosine_similarity(matrix)

    profile_index = len(all_names) - 1
    scores = list(enumerate(similarity[profile_index]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i, score in scores:
        name = all_names[i]
        if name == "__taste_profile__":
            continue
        if name.lower() in favorites_lower:
            continue
        if score > 0:
            recommendations.append({
                "name": name,
                "score": str(round(float(score) * 100)) + "%"
            })
        if len(recommendations) >= top_n:
            break

    return recommendations
