import os
import spotipy
from spotipy import oauth2

auth_scope = ['user-library-read',
              'user-read-currently-playing',
              'user-read-playback-state',
              'user-modify-playback-state']

SCOPE = ' '.join(auth_scope)

oauth = oauth2.SpotifyOAuth(username=os.environ["SPOTIFY_USERNAME"],
                            client_id=os.environ["SPOTIFY_CLIENT_ID"],
                            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
                            redirect_uri="http://localhost:8001/callback",
                            scope=SCOPE)

sp = spotipy.Spotify(auth_manager=oauth)
