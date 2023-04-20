# Required imports
import pandas as pd
import streamlit as st
import json
from pathlib import Path
import requests
from collections import defaultdict
from itertools import product

mavs_pbp_season = pd.read_parquet(str(Path.cwd()) + "/data/mavs_pbp_season.parquet")
all_players_data = pd.read_parquet(str(Path.cwd()) + "/data/player_data.parquet")

mavs_players_names = all_players_data[all_players_data['team'] == 'DAL']

teams_json = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
all_teams = {}
for team in teams_json:
    all_teams[team['teamName']] = team['teamId']
del all_teams['Dallas Mavericks']

lineups = pd.read_parquet(str(Path.cwd()) + "/data/lineups.parquet")

offensive_players = pd.read_parquet(str(Path.cwd()) + "/data/offensive_players.parquet")
defensive_players = pd.read_parquet(str(Path.cwd()) + "/data/defensive_players.parquet")

# Get the position of a given player
def get_positions(player_name):
    positions = all_players_data[all_players_data['name'] == player_name].reset_index()
    unique_pos = list(positions['startPos'].unique())
    unique_pos.remove("")
    return unique_pos

def get_team_id(team_name):
    return all_teams[team_name]

def get_team_abbrev(team_id):
    all_player_data = all_players_data[all_players_data['nbaTeamId'] == str(team_id)].reset_index()
    return all_player_data.at[0, 'team']

# Define function for the first tab
def Lineups():
    st.header("🏀 Lineups")

    teams = list(all_teams.keys())
    selected_team = st.selectbox("Select an opponent to create possible roster against", teams, index=0)
    st.markdown("Optimal lineups against: **{0}**".format(selected_team))
    st.caption("_Click to sort and display by the highest strengths_")

    team_abbrev = get_team_abbrev(int(get_team_id(selected_team)))

    team_lineups = lineups[lineups['team'] == team_abbrev].reset_index()
    highest_length = 0
    for i in range(len(team_lineups.index)):
        highest_length = max(highest_length, len(team_lineups.at[i,'lineup']))
    player_cols = ["p{0}".format(i+1) for i in range(highest_length)]
    team_lineups[player_cols] = pd.DataFrame(team_lineups.lineup.tolist(), index= team_lineups.index)
    team_lineups.drop('lineup', axis=1, inplace=True)
    team_lineups.drop('#', axis=1, inplace=True)
    team_lineups.drop('index', axis=1, inplace=True)
    team_lineups.drop_duplicates(inplace=True)
    team_lineups = team_lineups.reset_index()
    
    filtered_lineups = pd.DataFrame(columns=['C', 'PF', 'SG', 'PG', 'SF', 'Offense Strength', 'Defense Strength', 'Play Type'])

    for i in range(len(team_lineups.index)):
        lineup_pos = defaultdict(set)
        
        for player in player_cols:
            positions = get_positions(team_lineups.at[i,player])
            for position in positions:
                lineup_pos[position].add(team_lineups.at[i,player])
        for position in lineup_pos:
            lineup_pos[position] = list(lineup_pos[position])
        if len(lineup_pos) != 5:
            continue     
        all_combinations = {}
        count = 0
        for players in product(*lineup_pos.values()):
            all_combinations[count] = [[x, j] for x, j in zip(lineup_pos, players)]
            count += 1
        all_combinations_keys = list(all_combinations.keys())
        for j in range(len(all_combinations_keys)):
            players = [x[1] for x in all_combinations[all_combinations_keys[j]]]
            player_set = set(players)
            if len(player_set) < len(players):
                del all_combinations[all_combinations_keys[j]]
        for key in all_combinations:
            updated_lineup = {}
            players = all_combinations[key]
            for pos, player in players:
                updated_lineup[pos] = player
            new_lineup = [updated_lineup['C'], updated_lineup['PF'], updated_lineup['SG'], updated_lineup['PG'], updated_lineup['SF']]
            offense_strength = 0
            defense_strength = 0
            offense_count = 0
            defense_count = 0
            for player in new_lineup:
                offense = offensive_players[(offensive_players['name'] == player) & (offensive_players['team'] == 'DAL')]
                defense = defensive_players[(defensive_players['name'] == player) & (defensive_players['team'] == 'DAL')]
                if not offense.empty:
                    offense_strength += offense['score'].values[0]
                    offense_count += 1
                if not defense.empty:
                    defense_strength += defense['score'].values[0]
                    defense_count += 1
            if offense_strength == 0 or defense_strength == 0:
                new_lineup.append(abs(team_lineups.at[i,'offense_strength']))
                new_lineup.append(abs(team_lineups.at[i,'defense_strength']))
            else:
                offense_strength /= offense_count
                defense_strength /= defense_count
                new_lineup.append(abs(offense_strength))
                new_lineup.append(abs(defense_strength))
            if new_lineup[-1] > new_lineup[-2]:
                new_lineup.append("Defense")
            else:
                new_lineup.append("Offense")
            
            filtered_lineups.loc[len(filtered_lineups.index)] = new_lineup
    
    filtered_lineups.drop_duplicates(inplace=True)
    filtered_lineups.sort_values(['Offense Strength', 'Defense Strength'], ascending=[False, False], inplace=True)
    filtered_lineups.set_index('Play Type', inplace=True)
    st.dataframe(filtered_lineups.head(10))

    # Metric information
    play_col, offense_col, defense_col = st.columns(3)

    if len(filtered_lineups.index) > 0:
        play_col.metric(":green[**Average Play Type**]", list(filtered_lineups.index)[0])
    offense_col.metric(":green[**Average Offensive Strength**]", "{:.3f}".format(filtered_lineups.head(10)['Offense Strength'].mean()))
    defense_col.metric(":green[**Average Defensive Strength**]", "{:.3f}".format(filtered_lineups.head(10)['Defense Strength'].mean()))
