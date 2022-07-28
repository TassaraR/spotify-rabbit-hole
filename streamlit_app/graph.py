import math
import networkx as nx
import numpy as np
import pandas as pd
import bokeh
from nx_layout import hierarchy_layout
from typing import List, Optional
from bokeh.io import output_file
from bokeh.plotting import from_networkx
from bokeh.models import (HoverTool, ResetTool,
                          WheelZoomTool, PanTool,
                          MultiLine, Plot,
                          ColumnDataSource, LabelSet,
                          Range1d, Circle)


def create_nx_graph(edges: List[tuple],
                    labels: dict,
                    songs: pd.DataFrame
                    ) -> nx.classes.graph.Graph:
    G = nx.Graph()
    graph = [(labels[edge[0]], labels[edge[1]])
             for edge in edges]
    G.add_edges_from(graph)

    # Add name attribute
    node_label_attr = {node: {'name': '\n'.join(node.split())} for node in G.nodes()}
    nx.set_node_attributes(G, node_label_attr)

    # Add alpha attribute
    for n, node in enumerate(G.nodes()):
        if n == 0:
            alpha = 1
        else:
            alpha = 0
        G.nodes()[node]['alpha'] = alpha

    # Add songs
    artist_2_uri = {v: k for k, v in labels.items()}
    for node in G.nodes():

        curr_artist = songs.artist_uri == artist_2_uri[node]
        curr_df = songs[curr_artist]

        for n, song in enumerate(curr_df.track_name):
            G.nodes()[node][f'track{n + 1}'] = song

    return G


def create_int_idx_graph_from_nx(G: nx.classes.graph.Graph
                                 ) -> nx.classes.graph.Graph:
    return nx.convert_node_labels_to_integers(G)


def hierarchy_pos(G: nx.classes.graph.Graph,
                  kind: str = 'radial') -> dict:
    G_int = create_int_idx_graph_from_nx(G)
    edge_labels = {k: v
                   for k, v
                   in zip(G_int.nodes(), G.nodes())}

    pos = hierarchy_layout(G_int,
                           root=0,
                           width=2 * math.pi,
                           xcenter=0)
    if kind == 'radial':
        pos = {u: (r * math.cos(theta), r * math.sin(theta))
               for u, (theta, r) in pos.items()}
    named_pos = {edge_labels[k]: v
                 for k, v in pos.items()}
    return named_pos


def create_nx_bokeh(G: nx.classes.graph.Graph,
                    title: str,
                    layout: dict,
                    width: Optional[int] = 800,
                    height: Optional[int] = 800
                    ) -> bokeh.models.plots.Plot:

    scaler = 1.3
    x_layout, y_layout = zip(*layout.values())
    x_range = np.array([min(x_layout), max(x_layout)]) * scaler
    y_range = np.array([min(y_layout), max(y_layout)]) * scaler
    plot = Plot(width=width,
                height=height,
                x_range=Range1d(*x_range),
                y_range=Range1d(*y_range)
                )
    plot.title.text = title
    plot.title.align = "center"

    tracks = [(f"Track {i + 1}", f"@track{i + 1}") for i in range(3)]
    hover = HoverTool(tooltips=[("Artist", "@index"), *tracks])
    reset = ResetTool()
    wheel_zoom = WheelZoomTool()
    pan = PanTool()
    tools = [hover, reset, wheel_zoom, pan]
    plot.add_tools(*tools)
    plot.toolbar.active_drag = pan
    plot.toolbar.active_scroll = wheel_zoom
    plot.toolbar_location = 'below'  # above

    graph = from_networkx(G, layout)
    graph.node_renderer.glyph = Circle(size=80,
                                       fill_color="#1DB954",
                                       fill_alpha='alpha',
                                       line_alpha=0)
    graph.edge_renderer.glyph = MultiLine(line_color="lightgray",
                                          line_alpha=0.2,
                                          line_width=1)
    plot.outline_line_color = None
    plot.background_fill_alpha = 0
    plot.border_fill_alpha = 0

    source = ColumnDataSource({'x': x_layout,
                               'y': y_layout,
                               'name': list(layout.keys())})
    labels = LabelSet(x='x', y='y', text='name',
                      text_font_size="10pt",
                      text_align='center',
                      y_offset=-6,
                      source=source,
                      text_color='white')

    plot.renderers.append(labels)
    plot.renderers.append(graph)
    output_file("../interactive_graphs.html")

    return plot
