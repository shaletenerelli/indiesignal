import time
from main import create_database, search_artists, save_artists, fetch_artist_tags, save_artist_tags, fetch_artist_info, update_artist_listeners

SEED_ARTISTS = [
    "Big Thief", "Phoebe Bridgers", "Adrianne Lenker", "Bon Iver", "Sufjan Stevens",
    "Fleet Foxes", "Iron & Wine", "Joanna Newsom", "Sharon Van Etten", "Angel Olsen",
    "Julien Baker", "Lucy Dacus", "boygenius", "Frightened Rabbit", "The National",
    "Pinegrove", "Hovvdy", "Camp Cope", "Palehound", "Hand Habits",
    "Florist", "Lomelda", "Squirrel Flower", "Waxahatchee", "Molly Burch",
    "Bedouine", "Weyes Blood", "Hozier", "Novo Amor", "Mt. Joy",
    "Lord Huron", "Gregory Alan Isakov", "The Tallest Man on Earth",
    "Jose Gonzalez", "Nick Drake", "Elliott Smith", "Alex G", "Car Seat Headrest",
    "Snail Mail", "Soccer Mommy", "Clairo", "beabadoobee", "Men I Trust",
    "Still Woozy", "Rex Orange County", "Cavetown", "Omar Apollo", "Hippo Campus",
    "Flyte", "Aldous Harding", "Julia Jacklin", "Courtney Barnett",
    "Stella Donnelly", "Haley Heynderickx", "Faye Webster", "Caroline Polachek",
    "Japanese Breakfast", "Girlpool", "Bellows", "Half Waif", "Saintseneca",
    "Radical Face", "The Milk Carton Kids", "Over the Rhine", "Caamp",
    "Watchhouse", "The Head and the Heart", "The Lumineers", "Mumford and Sons",
    "Vampire Weekend", "Wilco", "Dawes", "The War on Drugs", "Kurt Vile",
    "Phosphorescent", "Josh Ritter", "Andrew Bird", "Mandolin Orange",
    "Strand of Oaks", "Kevin Morby", "William Tyler", "Steve Gunn",
    "Ryley Walker", "Cass McCombs", "Real Estate", "Yo La Tengo",
    "Mazzy Star", "Low", "Jason Molina", "Gillian Welch", "Neko Case",
    "Bonnie Prince Billy", "Damien Jurado", "Pedro the Lion", "Denison Witmer"
]


def seed():
    print("Creating database...")
    create_database()
    seen = set()
    artists_to_seed = []
    for name in SEED_ARTISTS:
        if name not in seen:
            seen.add(name)
            artists_to_seed.append(name)
    print(f"Seeding {len(artists_to_seed)} artists...")
    for i, artist_name in enumerate(artists_to_seed):
        print(f"[{i+1}/{len(artists_to_seed)}] {artist_name}")
        try:
            results = search_artists(artist_name, limit=1)
            if results:
                save_artists(results)
            tags = fetch_artist_tags(artist_name, limit=9)
            save_artist_tags(artist_name, tags)
            listeners = fetch_artist_info(artist_name)
            update_artist_listeners(artist_name, listeners)
        except Exception as e:
            print(f"  Error: {e}")
        import time
        time.sleep(0.5)
    print("Done. Database seeded.")


if __name__ == "__main__":
    seed()
