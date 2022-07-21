import os
import pickle
import argparse
import pandas as pd
from pathlib import Path
from spotify import rabbit_hole


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("artist", type=str, help="Base artist")
    parser.add_argument("-t", "--max-artists", type=int, default=4, help="Max. Artists to retrieve")
    parser.add_argument("-r", "--n-related", type=int, default=2, help="Number of related artists per artist")
    parser.add_argument("-s", "--n-tracks", type=int, default=1, help="Number of songs per artist")
    parser.add_argument("-o", "--output-dir", type=str, default='.', help="Output directory")

    args = parser.parse_args().__dict__
    args = {k.replace("-", "_"): v
            for k, v in args.items()}

    artist_names, uri_related, top_tracks = rabbit_hole(base_artist=args['artist'],
                                                        depth=args['max_artists'] + 1,
                                                        n_artists=args['n_related'],
                                                        tracks_per_artist=args['n_tracks'])

    Path(args["output_dir"]).mkdir(parents=True, exist_ok=True)

    graph_params = dict(edges=uri_related,
                        labels=artist_names)
    graph_params_output_path = os.path.join(args["output_dir"], "graph.pkl")

    with open(graph_params_output_path, "wb") as f:
        pickle.dump(graph_params, f)

    top_tracks = pd.DataFrame(top_tracks)
    top_tracks_output_path = os.path.join(args["output_dir"], "songs.csv")
    top_tracks.to_csv(top_tracks_output_path, index=False)
