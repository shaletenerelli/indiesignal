# IndieSignal

A music discovery web app that helps you find emerging indie, folk, and singer-songwriter artists.

## What it does

- Search for artists by name using the Last.fm API
- View listener counts to gauge popularity
- Browse an artist's top albums with playcount data
- Stores all data in a local SQLite database

## Tech stack

- Python
- Flask (web framework)
- SQLite (database)
- Last.fm API
- HTML/CSS

## How to run it

1. Clone the repository
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Add your Last.fm API key to `main.py`
6. Run the app: `python app.py`
7. Open `http://127.0.0.1:5001` in your browser

## Project structure

- `main.py` -- data pipeline: API calls, database setup, query functions
- `app.py` -- Flask web server and routes
- `templates/` -- HTML templates for each page