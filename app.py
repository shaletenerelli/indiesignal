from flask import Flask, render_template, request
from main import search_artists, save_artists, query_artists, fetch_releases, save_releases, query_releases, fetch_similar_artists

app = Flask(__name__)


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
    releases = fetch_releases(artist_name, limit=10)
    save_releases(releases)
    similar = fetch_similar_artists(artist_name, limit=5)
    return render_template("artist.html", artist_name=artist_name, releases=releases, similar=similar)


if __name__ == "__main__":
    app.run(debug=True, port=5001)