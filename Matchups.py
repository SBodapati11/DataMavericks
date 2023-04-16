# Required imports
import numpy as np
import pandas as pd
import os
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
from nba_api.stats.endpoints import shotchartdetail
import json
from pathlib import Path
import requests

mavs_pbp_season = pd.read_parquet(str(Path.cwd()) + "/data/mavs_pbp_season.parquet")
all_players_data = pd.read_parquet(str(Path.cwd()) + "/data/player_data.parquet")

mavs_players_names = all_players_data[all_players_data['team'] == 'DAL']

teams_json = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
all_teams = {}
for team in teams_json:
    all_teams[team['teamName']] = team['teamId']
del all_teams['Dallas Mavericks']

# image folder
image_folder = "images"

def Matchups():
    st.header("Matchups")

    st.write(f"<span style='color: blue'><b>Select Mavericks Player</b></span>", unsafe_allow_html=True)
    selected_player_1 = st.selectbox(" ", mavs_players_names['name'].unique())
    st.write(f"<span style='color: red'><b>Select Opponent Team</b></span>", unsafe_allow_html=True)
    selected_opponent = st.selectbox(" ", list(all_teams.keys()))
    st.write(f"<span style='color: red'><b>Select Opponent Player</b></span>", unsafe_allow_html=True)
    opponents_players_names = all_players_data[all_players_data['nbaTeamId'] == str(all_teams[selected_opponent])]
    selected_player_2 = st.selectbox(" ", opponents_players_names['name'].unique())

    # TODO - Pull up selected_player_1's stats and selected_player_2's stats and run algorithmic magic on them woo
    # pit players against each other and run probability of p1 beating p2
    player_one_id = all_players_data[all_players_data['name'] == selected_player_1].reset_index().at[0, 'nbaId']
    mavs_id = all_players_data[all_players_data['name'] == selected_player_1].reset_index().at[0,'nbaTeamId']
    player_two_id = all_players_data[all_players_data['name'] == selected_player_2].reset_index().at[0,'nbaId']
    opp_id = all_players_data[all_players_data['name'] == selected_player_2].reset_index().at[0,'nbaTeamId']

    st.subheader("Historical Matchup")


    estimated_chance = 49

    # after doing that, put them next to each other using an automatically pulled image
    image_name = "{0}.png".format(selected_player_1.split()[0].lower())
    image_path = os.path.join(image_folder, image_name)
    fighter1_image = Image.open(image_path)

    # TODO - Make the second fighter automatic
    image_2_name = "teams_logos/{0}.png".format(selected_opponent.split()[-1].lower())
    image_2_path = os.path.join(image_folder, image_2_name)
    fighter2_image = Image.open(image_2_path)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.image(fighter1_image)

    with col2:
        st.markdown(
            "<div style='text-align:center'><span style='color:blue; font-size: 72px;'>V.</span><span "
            "style='color:red; font-size: 72px;'>S.</span></div>", unsafe_allow_html=True)

    with col3:
        st.image(fighter2_image)

    # Write Prediction
    st.subheader("Prediction")
    st.write(
        f"<span style='color: blue'>{selected_player_1}</span> has a <b>{str(estimated_chance)}%</b> chance of beating <span style='color: red'>{selected_player_2}</span>",
        unsafe_allow_html=True)
    if estimated_chance > 50:
        image_name = "gifs/luka_muscle.gif"
        image_path = os.path.join(image_folder, image_name)
        st.image(image_path)
    else:
        image_name = "gifs/luka_no.gif"
        image_path = os.path.join(image_folder, image_name)
        st.image(image_path)
