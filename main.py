import sqlite3
import time
from pathlib import Path

import requests


BASE_URL = "https://ws.audioscrobbler.com/2.0/"
API_KEY = "46d597257c3442f9e60d64a32e2146eb"
DB_PATH = Path("data/indie_signal.db")


def search_artists(query, limit=5):
    """
    Search Last.fm for artists and return a list of artist dictionaries.
    """

    params = {
        "method": "artist.search",
        "artist": query,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }

    response = requests.get(BASE_URL, params=params)

    time.sleep(0.25)

    response.raise_for_status()

    data = response.json()

    artists = data.get("results", {}).get("artistmatches", {}).get("artist", [])

    return artists


def create_database():
    """
    Create the database file and the artists, releases, and artist_tags tables.
    """

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            musicbrainz_id TEXT UNIQUE,
            name TEXT NOT NULL,
            country TEXT,
            artist_type TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS releases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            musicbrainz_id TEXT UNIQUE,
            artist_musicbrainz_id TEXT,
            title TEXT NOT NULL,
            release_date TEXT,
            release_type TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artist_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_name TEXT NOT NULL,
            tag TEXT NOT NULL,
            UNIQUE(artist_name, tag)
        )
    """)

    connection.commit()
    connection.close()


def save_artists(artists):
    """
    Save artist dictionaries into the artists table.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for artist in artists:
        cursor.execute("""
            INSERT OR IGNORE INTO artists (
                musicbrainz_id,
                name,
                country,
                artist_type
            )
            VALUES (?, ?, ?, ?)
        """, (
            artist.get("mbid"),
            artist.get("name"),
            None,
            None
        ))

    connection.commit()
    connection.close()


def print_artists(artists):
    """
    Print artist results in the terminal.
    """

    for artist in artists:
        print("Name:", artist.get("name"))
        print("Listeners:", artist.get("listeners"))
        print("MBID:", artist.get("mbid"))
        print("---")


def print_releases(releases):
    """
    Print release results in the terminal.
    """

    for release in releases:
        print("Title:", release.get("name"))
        print("Playcount:", release.get("playcount"))
        print("MBID:", release.get("mbid"))
        print("---")


def fetch_releases(artist_name, limit=10):
    """
    Fetch top albums from Last.fm for a given artist name.
    """

    params = {
        "method": "artist.gettopalbums",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }

    response = requests.get(BASE_URL, params=params)

    time.sleep(0.25)

    response.raise_for_status()

    data = response.json()

    releases = data.get("topalbums", {}).get("album", [])

    return releases


def fetch_similar_artists(artist_name, limit=5):
    """
    Fetch similar artists from Last.fm for a given artist name.
    """

    params = {
        "method": "artist.getsimilar",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }

    response = requests.get(BASE_URL, params=params)

    time.sleep(0.25)

    response.raise_for_status()

    data = response.json()

    similar = data.get("similarartists", {}).get("artist", [])

    return similar


def fetch_artist_tags(artist_name, limit=9):
    """
    Fetch top tags from Last.fm for a given artist name.
    """

    params = {
        "method": "artist.gettoptags",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }

    response = requests.get(BASE_URL, params=params)

    time.sleep(0.25)

    response.raise_for_status()

    data = response.json()

    tags = data.get("toptags", {}).get("tag", [])

    return tags


def save_artist_tags(artist_name, tags):
    """
    Save artist tags into the artist_tags table.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for tag in tags:
        cursor.execute("""
            INSERT OR IGNORE INTO artist_tags (
                artist_name,
                tag
            )
            VALUES (?, ?)
        """, (
            artist_name,
            tag.get("name")
        ))

    connection.commit()
    connection.close()


def save_releases(releases):
    """
    Save release dictionaries into the releases table.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    for release in releases:
        cursor.execute("""
            INSERT OR IGNORE INTO releases (
                musicbrainz_id,
                artist_musicbrainz_id,
                title,
                release_date,
                release_type
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            release.get("mbid"),
            release.get("artist", {}).get("mbid"),
            release.get("name"),
            None,
            "Album"
        ))

    connection.commit()
    connection.close()


def query_artists():
    """
    Return all artists stored in the database.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT musicbrainz_id, name, country, artist_type
        FROM artists
    """)

    rows = cursor.fetchall()

    connection.close()

    artists = []

    for row in rows:
        artists.append({
            "musicbrainz_id": row[0],
            "name": row[1],
            "country": row[2],
            "artist_type": row[3]
        })

    return artists


def query_releases(artist_musicbrainz_id):
    """
    Return all releases for a given artist stored in the database.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT musicbrainz_id, title, release_date, release_type
        FROM releases
        WHERE artist_musicbrainz_id = ?
    """, (artist_musicbrainz_id,))

    rows = cursor.fetchall()

    connection.close()

    releases = []

    for row in rows:
        releases.append({
            "musicbrainz_id": row[0],
            "title": row[1],
            "release_date": row[2],
            "release_type": row[3]
        })

    return releases


def query_artist_tags(artist_name):
    """
    Return all tags for a given artist from the database.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT tag FROM artist_tags
        WHERE artist_name = ?
    """, (artist_name,))

    rows = cursor.fetchall()
    connection.close()

    return [row[0] for row in rows]


def query_all_artist_tags():
    """
    Return a dict mapping each artist name to a string of their tags.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT artist_name, tag FROM artist_tags
    """)

    rows = cursor.fetchall()
    connection.close()

    artist_tags = {}
    for artist_name, tag in rows:
        if artist_name not in artist_tags:
            artist_tags[artist_name] = []
        artist_tags[artist_name].append(tag)

    return {name: " ".join(tags) for name, tags in artist_tags.items()}


if __name__ == "__main__":
    create_database()

    artists = search_artists("Big Thief", limit=5)

    save_artists(artists)

    print_artists(artists)

    releases = fetch_releases("Big Thief", limit=10)

    save_releases(releases)

    print_releases(releases)

    print("Releases fetched and saved:", len(releases))

    print("Saved to database:", DB_PATH)