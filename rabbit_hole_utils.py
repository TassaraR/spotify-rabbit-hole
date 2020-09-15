# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
from credentials import sp

#__all__ = ['artist_search', 'related_artists', 'top_artist_tracks', 'add_tracks_queue', 'sample', 'hierarchy_pos', 'related_graph', 'rabbitHole']

def artist_search(q):
    """Retrieves most popular artist"""
    
    artist_search = sp.search(q = q, type = 'artist')
    
    artists_info = artist_search['artists']['items']
    artists_rank = [artists['popularity'] for artists in artists_info]
    most_popular_result = artists_rank.index(max(artists_rank))
    
    return (artists_info[most_popular_result]['uri'], artists_info[most_popular_result]['name'])

def related_artists(artist_uri):
    """Returns dict (artist_uri: artist_name) for each related artist of the uri entered"""
    artists = sp.artist_related_artists(artist_uri)['artists']
    
    return {artists[i]['uri']:artists[i]['name'] for i in range(len(artists))}
    

def top_artist_tracks(artist_uri):
    """Returns dict (track_uri: song_name) with top tracks of the artist"""
    top_tracks = sp.artist_top_tracks(artist_uri)
    
    return {top_tracks['tracks'][i]['uri']:top_tracks['tracks'][i]['name'] for i in range(len(top_tracks['tracks']))}

def get_device():
    "Gets first device in the user devices list"
    
    return sp.devices()['devices'][-1]['id']

def add_tracks_queue(track_uri, device):
    """Adds tracks to the queue if the user has a device opened"""
    if type(track_uri) == str:
        sp.add_to_queue(track_uri, device)
        
    elif hasattr(track_uri,'__iter__'):
        for track in track_uri:
            sp.add_to_queue(track, device)
        
def sample(iterator,n = 2 ,seed = None):
    """Extracts n random artists/songs"""
    if seed is not None:
        random.seed(seed)
    if len(iterator) > 0 and len(iterator) < n:
        return random.sample(iterator, len(iterator))
    elif len(iterator) == 0:
        return
    return random.sample(iterator, n)

def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    """Hiearchy pos for NetworkX"""
    
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G))) #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):

        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos


    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

def related_graph(edges, labels, plot = True):
    """Displays a nx graph of the relations between parent and child artists"""
    G = nx.Graph()
    graph = [(labels[edge[0]],labels[edge[1]]) for edge in edges]
    G.add_edges_from(graph)
    G_int = nx.convert_node_labels_to_integers(G)
    edge_labels = {k:v for k,v in zip(G_int.nodes(), G.nodes())}
    
    if plot == True:
        plt.figure(figsize = (10,10))
        pos = hierarchy_pos(G_int, 0, width = 2 * math.pi, xcenter = 0)
        new_pos = {u:(r*math.cos(theta),r*math.sin(theta)) for u, (theta, r) in pos.items()}

        nx.draw(G_int, pos=new_pos, node_size = 50, node_shape="None", alpha = 0.3)
        nx.draw_networkx_nodes(G_int, pos=new_pos, nodelist = [0], node_color = 'lightgray', node_size = 400, node_shape = 'o')
        nx.draw_networkx_labels(G_int, pos = new_pos, labels = edge_labels, font_size = 8)
        x_values, y_values = zip(*new_pos.values())
        x_max, x_min = max(x_values), min(x_values)
        x_margin = (x_max - x_min) * 0.1
        plt.xlim(x_min - x_margin, x_max + x_margin)
        plt.ylim(x_min - x_margin, x_max + x_margin)
        plt.show()      
    return G


def rabbitHole(base_artist, depth = 5, n_artists = 2, tracks_per_artist = 1):
    """
    Performs a 'rabbit hole' sampling of related songs and artists

    It takes n related artists from the input artist and m of the
    top songs of those artists until the 'depth' parameter is
    satisfied
    """

    artists_visited = set()
    songs_visited = set()
    current_pool = []
    uri_relationship = []
    artists_names = {}
    
    init_artist_uri, init_artist_name = artist_search(base_artist) # tuple uri y nombre
    artists_names[init_artist_uri] = init_artist_name

    artists_visited.add(init_artist_uri)
    current_pool.append(init_artist_uri)
    
    while (len(current_pool) > 0) and (len(artists_visited) < depth):
        #fifo with list / Could've used queue.Queue instead
        artist_uri = current_pool.pop(0)
        
        related_pool = related_artists(artist_uri) # returns dict uri y nombre

        # Removes visited from pool, just URI
        filtered_related_pool = {artist_uri:related_pool[artist_uri] 
                                 for artist_uri in related_pool 
                                 if artist_uri not in artists_visited}

        sampled_related_pool = sample(filtered_related_pool.keys(), n = n_artists)
        current_pool.extend(sampled_related_pool)
        
        # gets n tracks from each artist
        for rel_artist in sampled_related_pool:
            n_songs = sample(top_artist_tracks(rel_artist).keys(), n = tracks_per_artist)
                
            songs_visited.update(n_songs)
            artists_visited.add(rel_artist)
            
            artists_names[rel_artist] = related_pool[rel_artist]

            uri_relationship.append((artist_uri, rel_artist))

            #depth -= 1
            if len(artists_visited) == depth:
                break      
   
    return list(songs_visited), artists_names, uri_relationship