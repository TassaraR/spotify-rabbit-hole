import random
from credentials import sp


def artist_search(q: str) -> str:
    """Retrieves most popular artist given a query"""
    
    artist_search = sp.search(q=q, type='artist')
    
    artists_info = artist_search['artists']['items']
    artists_rank = [artists['popularity'] for artists in artists_info]
    most_popular_result = artists_rank.index(max(artists_rank))
    
    return artists_info[most_popular_result]['uri'], artists_info[most_popular_result]['name']


def related_artists(artist_uri: str) -> set:
    """Returns dict (artist_uri: artist_name) for each related artist of the uri entered"""
    artists = sp.artist_related_artists(artist_uri)['artists']
    
    return {artists[i]['uri']: artists[i]['name'] for i in range(len(artists))}
    

def top_artist_tracks(artist_uri):
    """Returns dict (track_uri: song_name) with top tracks of the artist"""
    top_tracks = sp.artist_top_tracks(artist_uri)

    if not top_tracks:
        return []

    tracks = []
    for i in range(len(top_tracks['tracks'])):
        ttrack = top_tracks['tracks'][i]

        parsed_tracks = dict(artist_uri=artist_uri,
                             artist_name=[artist for artist in ttrack['artists']][0]['name'],
                             duration_min=ttrack['duration_ms'] / 1000 / 60,
                             explicit=str(ttrack['explicit']).upper(),
                             track_name=ttrack['name'],
                             popularity=ttrack['popularity'])

        tracks.append(parsed_tracks)
    return tracks


def get_device():
    """Gets first device in the user devices list"""
    
    return sp.devices()['devices'][-1]['id']


def add_tracks_queue(track_uri, device):
    """Adds tracks to the queue if the user has a device opened"""
    if type(track_uri) == str:
        sp.add_to_queue(track_uri, device)
        
    elif hasattr(track_uri, '__iter__'):
        for track in track_uri:
            sp.add_to_queue(track, device)


def sample(iterator, n=2, seed=0):
    """Extracts n random artists/songs"""
    if seed is not None:
        random.seed(seed)
    if 0 < len(iterator) < n:
        return random.sample(iterator, len(iterator))
    elif len(iterator) == 0:
        return
    return random.sample(iterator, n)


def rabbit_hole(base_artist, depth=5, n_artists=2, tracks_per_artist=1):
    """
    Performs a 'rabbit hole' sampling of related songs and artists

    It takes n related artists from the input artist and m of the
    top songs of those artists until the 'depth' parameter is
    satisfied
    """

    artists_visited = set()
    songs_visited = []
    current_pool = []
    uri_relationship = []
    artists_names = {}
    
    init_artist_uri, init_artist_name = artist_search(base_artist) # tuple uri y nombre
    artists_names[init_artist_uri] = init_artist_name
    base_songs = sample(top_artist_tracks(init_artist_uri), n=tracks_per_artist)
    songs_visited.extend(base_songs)

    artists_visited.add(init_artist_uri)
    current_pool.append(init_artist_uri)
    
    while (len(current_pool) > 0) and (len(artists_visited) < depth):
        # FIFO with list / Could've used queue.Queue instead
        artist_uri = current_pool.pop(0)
        
        related_pool = related_artists(artist_uri) # returns dict uri y nombre

        # Removes visited from pool, just URI
        filtered_related_pool = {artist_uri: related_pool[artist_uri]
                                 for artist_uri in related_pool 
                                 if artist_uri not in artists_visited}

        sampled_related_pool = sample(filtered_related_pool.keys(), n=n_artists)
        current_pool.extend(sampled_related_pool)
        
        # gets n tracks from each artist
        for rel_artist in sampled_related_pool:
            n_songs = sample(top_artist_tracks(rel_artist), n = tracks_per_artist)
                
            songs_visited.extend(n_songs)
            artists_visited.add(rel_artist)
            
            artists_names[rel_artist] = related_pool[rel_artist]

            uri_relationship.append((artist_uri, rel_artist))

            if len(artists_visited) == depth:
                break

    return artists_names, uri_relationship, songs_visited
