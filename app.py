import streamlit as st
import streamlit.components.v1 as components

import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network

# Read data
df_interactions = pd.read_csv('data/processed_drug_interactions.csv')

# Set header title
st.title('Network visualization of drug-drug interactions')

# Add sidebar
# st.sidebar.title('Sidebar Menu')

# Define list of selection options
drug_list = ['Metformin', 'Lisinopril', 'Simvastatin', 'Warfarin']

# Implement multiselect options for users (output is a list)
selected_drugs = st.multiselect('Select drugs to visualize', drug_list)

if len(selected_drugs) == 0:
    # Show the following text upon initial site load
    st.text('Please choose at least 1 drug')
else:
    df_selected = df_interactions.loc[df_interactions['drug_1_name'].isin(selected_drugs) | df_interactions['drug_2_name'].isin(selected_drugs)]
    df_selected = df_selected.reset_index(drop=True)

    # Pyvis graph settings
    layout='barnes_hut'
    central_gravity=0.15
    node_distance=420
    spring_length=100
    spring_strength=0.15
    damping=0.96
    bgcolor, font_color = '#222222', 'white'

    G = nx.from_pandas_edgelist(df_selected, 'drug_1_name', 'drug_2_name', 'weight')

    # Initiate PyVis network object
    drug_net = Network(
                       height='450px',
                       width='100%',
                       bgcolor=bgcolor,
                       font_color=font_color,
                       notebook=True
                      )

    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)

    # Generate network with specific layout
    drug_net.repulsion(
                    node_distance=node_distance,
                    central_gravity=central_gravity,
                    spring_length=spring_length,
                    spring_strength=spring_strength,
                    damping=damping
                   )

    # Save graph as HTML file
    drug_net.save_graph('/tmp/pyvis_network_graph.html')

    # Load HTML file
    HtmlFile = open('/tmp/pyvis_network_graph.html', 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=500, width=695)

# st.button("Generate graph")
st.markdown(
    """
    <br>
    <br>
    <h6><a href="https://github.com/kennethleungty" target="_blank">Created by Kenneth Leung</a></h6>""", unsafe_allow_html=True,
)

# References
# https://github.com/napoles-uach/streamlit_network/blob/main/app.py
# https://discuss.streamlit.io/t/select-an-item-from-multiselect-on-the-sidebar/1276/2