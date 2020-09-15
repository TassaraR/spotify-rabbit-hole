# -*- coding: utf-8 -*-
from rabbit_hole_utils import rabbitHole, related_graph, add_tracks_queue, get_device
import argparse



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("artist", type = str, help="Input the name of the desired artist")
    parser.add_argument("-t","--total", type = int, default = 5, help="Total related artists")
    parser.add_argument("-r","--related", type = int, default = 2, help="number of related artists per artist")
    parser.add_argument("-s","--songs", type = int, default = 1, help="number of songs per artist")
    parser.add_argument("-p","--plot", type = bool, default = False, help="plot graph of related artists")
    
    args = parser.parse_args()
    print()

    tracks, artists, uri_rel = rabbitHole(args.artist, depth = args.total+1, n_artists = args.related, tracks_per_artist = args.songs)
    
    graph = related_graph(uri_rel, artists, plot = args.plot)
    
    artist_key = {}
    for k in {x[0] for x in graph.edges()}:
        artist_key[k] = []
    for k,v in graph.edges():
        artist_key[k].append(v)
      
    print(f'Artists: ({len(artist_key)}) ~ {len(artist_key)-1} + Input:')
    print(', '.join(graph.nodes))
    print('-'*20*args.related)    
    for k in artist_key:
        print(f'{k}:\n\t-{(", ".join(artist_key[k]))}')
    print('-'*20*args.related)
    print(f'Total Songs: {len(tracks)}')
    
    add_to_queue = None
    
    while add_to_queue not in {'Y','y','N','n'}:
        add_to_queue = input('Add songs to queue? Y/N?')
        if add_to_queue in {'Y','y'}:
            print('Adding Tracks...')
            try:
                add_tracks_queue(tracks, get_device())
            except IndexError:
                print('No Active Device found\nExiting...')
                exit(-1)
            exit(0)
        elif add_to_queue in {'N','n'}:
            print('Exiting...')
            exit(0)
            
        
    