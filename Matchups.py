# Required imports
import pandas as pd
import os
import streamlit as st
from PIL import Image
import json
from pathlib import Path
import requests

# Read the play by play, players, and scores data
mavs_pbp_season = pd.read_parquet(str(Path.cwd()) + "/data/mavs_pbp_season.parquet")
all_players_data = pd.read_parquet(str(Path.cwd()) + "/data/player_data.parquet")
offensive_players = pd.read_parquet(str(Path.cwd()) + "/data/offensive_players.parquet")
defensive_players = pd.read_parquet(str(Path.cwd()) + "/data/defensive_players.parquet")

mavs_players_names = all_players_data[all_players_data['team'] == 'DAL']

# Get the team name and ids
teams_json = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
all_teams = {}
for team in teams_json:
    all_teams[team['teamName']] = team['teamId']

# image folder
image_folder = "images"

# Get the team id of a given team (string)
def get_team_id(team_name):
    return all_teams[team_name]

# Get the team abbreviation of a given team (id)
def get_team_abbrev(team_id):
    all_player_data = all_players_data[all_players_data['nbaTeamId'] == str(team_id)].reset_index()
    return all_player_data.at[0, 'team']

# Given 2 players and their teams, predict the winner of the matchup
def predict_matchup_winner(player1_name, player1_team, player2_name, player2_team):
    player1_offense = offensive_players[(offensive_players['name'] == player1_name) & (offensive_players['team'] == player1_team)]
    player1_defense = defensive_players[(defensive_players['name'] == player1_name) & (defensive_players['team'] == player1_team)]

    player2_offense = offensive_players[(offensive_players['name'] == player2_name) & (offensive_players['team'] == player2_team)]
    player2_defense = defensive_players[(defensive_players['name'] == player2_name) & (defensive_players['team'] == player2_team)]
    
    # Check if a score exists for the Mavs player
    if not player1_offense.empty:
        player1 = player1_offense
    elif not player1_defense.empty:
        player1 = player1_defense
    else:
        return ()

    # Check if a score exists for the opponent player
    if not player2_offense.empty:
        player2 = player2_offense
    elif not player2_defense.empty:
        player2 = player2_defense
    else:
        return ()

    # Calculate the win probability based on who has the higher score
    win_probability = (player1['score'].values[0] / (player1['score'].values[0] + player2['score'].values[0])) * 100

    if player1['score'].values[0] > player2['score'].values[0]:
        return player1_name, player1_team, win_probability
    else:
        return player2_name, player2_team, win_probability

def Matchups():
    st.header("⛹️ Matchups")

    #st.write(f"<span style='color: silver'><b>Select Mavericks Player</b></span>", unsafe_allow_html=True)
    selected_player_1 = st.selectbox(":orange[**Select Mavericks Player**]", mavs_players_names['name'].unique())
    #st.write(f"<span style='color: silver'><b>Select Opponent Team</b></span>", unsafe_allow_html=True)
    selected_opponent = st.selectbox(":orange[**Select Opponent Team**]", list(all_teams.keys()))
    #st.write(f"<span style='color: silver'><b>Select Opponent Player</b></span>", unsafe_allow_html=True)
    opponents_players_names = all_players_data[all_players_data['nbaTeamId'] == str(all_teams[selected_opponent])]
    selected_player_2 = st.selectbox(":orange[**Select Opponent Player**]", opponents_players_names['name'].unique())

    # TODO - Pull up selected_player_1's stats and selected_player_2's stats and run algorithmic magic on them woo
    # pit players against each other and run probability of p1 beating p2
    player1_team = get_team_abbrev(int(get_team_id('Dallas Mavericks')))

    player2_team = get_team_abbrev(int(get_team_id(selected_opponent)))

    result = predict_matchup_winner(selected_player_1, player1_team, selected_player_2, player2_team)
    if len(result) != 0:
        winner, loser, estimated_chance = result[0], result[1], result[2]
        st.subheader("Estimated winner for this matchup: {0}".format(winner))
    else:
        st.subheader("Not enough data between these 2 players to estimate a matchup")

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
            "<div style='text-align:center'><span style='color:silver; font-size: 72px;'>V</span><span "
            "style='color:silver; font-size: 72px;'>S</span></div>", unsafe_allow_html=True)

    with col3:
        st.image(fighter2_image)

    # Write Prediction
    st.subheader("Prediction")
    formatted_win_str = "{:.3f}".format(estimated_chance)
    st.write(
        f"<span style='color: silver'>{selected_player_1}</span> has a <b>{formatted_win_str}%</b> chance of beating <span style=':silver'>{selected_player_2}</span>",
        unsafe_allow_html=True)
    if estimated_chance > 50:
        image_name = "gifs/luka_win.gif"
        image_path = os.path.join(image_folder, image_name)
        st.image(image_path)
    else:
        image_name = "gifs/luka_no.gif"
        image_path = os.path.join(image_folder, image_name)
        st.image(image_path)
