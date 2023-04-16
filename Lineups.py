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

# Define function for the first tab
def Lineups():
    st.header("Lineups")

    teams = list(all_teams.keys())
    selected_team = st.selectbox("Select a team", teams, index=0)
    st.markdown("Potential lineup against: **{0}** (click to change)".format(selected_team))


    # Define the table headers
    headers = ["Player Name", "Position", "Height(ft\"in)", "Weight(lbs)", "Info"]

    # TODO - Fill in more possible teams and their players
    # Create a list of data that contains the first row and the remaining rows with ellipses
    data_list = [data] + [{"...": "..." for _ in range(len(headers))} for _ in range(9)]

    # Create a Pandas DataFrame object from the list of data and the headers
    df = pd.DataFrame(data_list, columns=headers)

    # Display the table in Streamlit
    st.table(df)