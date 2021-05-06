from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from key import SPOTIFY_ID, SPOTIFY_SECRET

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: \n")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, "html.parser")
song_names = [song.getText() for song in soup.find_all(class_="chart-element__information__song")]

# ranks = [rank.getText() for rank in soup.find_all(class_="chart-element__rank__number")]
# artists = [artist.getText() for artist in soup.find_all(class_="chart-element__information__artist")]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com/callback/",
        client_id=SPOTIFY_ID,
        client_secret=SPOTIFY_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

# Search Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Create a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

# Add songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
