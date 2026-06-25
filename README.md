# IndieSignal

A music discovery web app that identifies and ranks indie, folk, and singer-songwriter artists by popularity tier and genre similarity.

## What it does

- Search for artists by name using the Last.fm API
- View discovery tier labels: Underground, Emerging, Rising, or Established based on listener counts
- Browse an artist's top albums with playcount data
- See genre tags pulled from Last.fm
- Get similar artist recommendations from Last.fm
- Get ML-powered recommendations from IndieSignal's own similarity engine

## How the ML works

IndieSignal builds a content-based recommendation system using artist genre tags. When you visit an artist page, the app fetches their tags from Last.fm and stores them in a local SQLite database. It then uses TF-IDF vectorization to convert each artist's tags into a numerical vector, and cosine similarity to measure how similar each pair of artists is. The result is a ranked list of similar artists drawn from the local database.

The more artists you search for, the better the recommendations get.

## Tech stack

- Python
- Flask (web framework)
- SQLite (three-table relational database)
- Last.fm API
- scikit-learn (TF-IDF, cosine similarity)
- HTML/CSS

## How to run it

1. Clone the repository
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your Last.fm API key
6. Run the app: `python app.py`
7. Open `http://127.0.0.1:5001` in your browser

## Project structure

- `main.py` -- data pipeline: Last.fm API calls, SQLite database setup, query functions
- `app.py` -- Flask web server and route handlers
- `recommender.py` -- ML recommendation engine using TF-IDF and cosine similarity
- `templates/` -- HTML templates for each page
- `static/` -- CSS styling
