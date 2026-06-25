import sqlite3
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DB_PATH = Path("data/indie_signal.db")


def get_all_artists():
    """
    Return all artists from the database.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name FROM artists
    """)

    rows = cursor.fetchall()
    connection.close()

    return [row[0] for row in rows]


def build_similarity_model(artist_tags):
    """
    Build a cosine similarity matrix from artist tag strings.
    artist_tags is a dict mapping artist name to a string of tags.
    """

    names = list(artist_tags.keys())
    tag_strings = list(artist_tags.values())

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(tag_strings)
    similarity = cosine_similarity(matrix)

    return names, similarity


def get_recommendations(target_artist, artist_tags, top_n=5):
    """
    Return the top N most similar artists to the target artist.
    """

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
        if names[i] != target_artist and score > 0:
            recommendations.append({
                "name": names[i],
                "score": round(float(score), 3)
            })
        if len(recommendations) >= top_n:
            break

    return recommendations