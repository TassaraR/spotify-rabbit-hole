import streamlit as st
import pickle
import pandas as pd
from graph import (create_nx_graph,
                   hierarchy_pos,
                   create_nx_bokeh)

# Config page format
st.set_page_config(layout="wide")

title = "Spotify Artists Rabbit Hole"
title_fmt = title.lower().replace(" ", "-")

with open("streamlit_app/style.css", 'r') as f:
    fmt = f.read().format(title=title_fmt)
    fmt = f"<style>{fmt}</style>"

st.markdown(fmt, unsafe_allow_html=True)
st.title(title)

# Content
with open('sample_data/graph.pkl', 'rb') as f:
    graph_params = pickle.load(f)

songs = pd.read_csv('sample_data/songs.csv')
songs['artist_name'] = songs['artist_uri']\
                        .map(graph_params['labels'])

G = create_nx_graph(**graph_params, songs=songs)
radial_pos = hierarchy_pos(G, kind='radial')

plot_graph = create_nx_bokeh(G,
                             layout=radial_pos,
                             title="",
                             width=700,
                             height=700)

ct = st.container()
ct.bokeh_chart(plot_graph, use_container_width=True)
st.markdown("---")

# st.dataframe(songs)
