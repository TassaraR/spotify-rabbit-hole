import streamlit as st
import pickle
import pandas as pd
from tracks_viz import altair_scatter_plot
from graph import (create_nx_graph,
                   hierarchy_pos,
                   create_nx_bokeh)

txt_path = lambda txt: f'streamlit_app/markdown/{txt}.md'

# Page configurations
st.set_page_config(layout="wide")

title = "Spotify Artists Rabbit Hole"
title_fmt = title.lower().replace(" ", "-")
with open("streamlit_app/style.css", 'r') as f:
    fmt = f.read().format(title=title_fmt)
    fmt = f"<style>{fmt}</style>"

st.markdown(fmt, unsafe_allow_html=True)

# App Content
# Set main app title
st.title(title)

# Load text files
with open(txt_path('DESCRIPTION'), 'r') as f:
    description_txt = f.read()

with open(txt_path('GRAPH_VIZ_DESIGN'), 'r', encoding='utf-8') as f:
    graph_design_txt = f.read()

with open(txt_path('SCATTER_VIZ_DESIGN'), 'r', encoding='utf-8') as f:
    scatter_design_txt = f.read()

with open(txt_path('EXPLANATION'), 'r', encoding='utf-8') as f:
    explanation_txt = f.read()

# Begin streamlit content
st.markdown(description_txt, unsafe_allow_html=True)
with st.expander('App description & further details'):
    st.markdown(explanation_txt)
st.markdown("---")

# Section 1 - Viz graph
with st.expander('Visualization design choices'):
    st.markdown(graph_design_txt)

# load graph data
with open('sample_data/graph.pkl', 'rb') as f:
    graph_params = pickle.load(f)

songs = pd.read_csv('sample_data/songs.csv')
songs['artist_name'] = songs['artist_uri']\
                        .map(graph_params['labels'])
songs['duration_min'] = songs['duration_min'].round(2)

G = create_nx_graph(**graph_params, songs=songs)
radial_pos = hierarchy_pos(G, kind='radial')

plot_graph = create_nx_bokeh(G,
                             layout=radial_pos,
                             title="",
                             width=700,
                             height=700)

st.bokeh_chart(plot_graph, use_container_width=True)

st.markdown("---")
st.markdown('<h2>Extracted Artists Tracks</h2>', unsafe_allow_html=True)
with st.expander('Visualization design choices'):
    st.markdown(scatter_design_txt)

alt_scatter = altair_scatter_plot(songs)
st.altair_chart(alt_scatter, use_container_width=True)

st.markdown("---")
