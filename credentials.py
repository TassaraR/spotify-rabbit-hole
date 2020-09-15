# -*- coding: utf-8 -*-
import pickle
import spotipy
from spotipy.oauth2 import SpotifyOAuth

with open('creds.pickle', 'rb') as f:
    creds = pickle.load(f)
    
auth_scope = ['user-library-read',
              'user-read-currently-playing',
              'user-read-playback-state',
              'user-modify-playback-state']

SCOPE = ' '.join(auth_scope)

oauth = SpotifyOAuth(username = creds['usr'],
                     client_id = creds['cID'], 
                     client_secret = creds['cSecret'], 
                     redirect_uri = creds['rURI'], 
                     scope = SCOPE)

sp = spotipy.Spotify(auth=oauth.get_access_token(as_dict = False))