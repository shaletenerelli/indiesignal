import os
import uuid
from flask import Flask, render_template, request, session, redirect, url_for
from main import search_artists, save_artists, query_artists, fetch_releases, save_releases, query_releases, fetch_similar_artists, fetch_artist_tags, save_artist_tags, query_all_artist_tags, query_artist_listeners, get_discovery_tier, fetch_artist_info, update_artist_listeners, save_favorite, remove_favorite, is_favorite, query_favorites
from recommender import get_recommendations
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return render_template("search.html", query="", artists=[])
    try:
        artists = search_artists(query, limit=5)
        save_artists(artists)
    except Exception:
        artists = []
    return render_template("search.html", query=query, artists=artists)


@app.route("/artist/<path:artist_name>")
def artist(artist_name):
    artist_name = artist_name.replace("+", " ")
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    session_id = session["session_id"]
    releases = fetch_releases(artist_name, limit=10)
    save_releases(releases)
    similar = fetch_similar_artists(artist_name, limit=5)
    tags = fetch_artist_tags(artist_name, limit=9)
    save_artist_tags(artist_name, tags)
    listeners = fetch_artist_info(artist_name)
    update_artist_listeners(artist_name, listeners)
    tier = get_discovery_tier(listeners)
    artist_tags = query_all_artist_tags()
    recommendations = get_recommendations(artist_name, artist_tags, top_n=5)
    favorited = is_favorite(session_id, artist_name)
    return render_template(
        "artist.html",
        artist_name=artist_name,
        releases=releases,
        similar=similar,
        tags=tags,
        recommendations=recommendations,
        listeners=listeners,
        tier=tier,
        favorited=favorited
    )


@app.route("/favorite/<path:artist_name>", methods=["POST"])
def toggle_favorite(artist_name):
    artist_name = artist_name.replace("+", " ")
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    session_id = session["session_id"]
    if is_favorite(session_id, artist_name):
        remove_favorite(session_id, artist_name)
    else:
        save_favorite(session_id, artist_name)
    return redirect(url_for("artist", artist_name=artist_name))


@app.route("/favorites")
def favorites():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    session_id = session["session_id"]
    artist_names = query_favorites(session_id)
    artists = []
    for name in artist_names:
        listeners = query_artist_listeners(name)
        tier = get_discovery_tier(listeners)
        artists.append({
            "name": name,
            "listeners": listeners,
            "tier": tier
        })
    return render_template("favorites.html", artists=artists)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
