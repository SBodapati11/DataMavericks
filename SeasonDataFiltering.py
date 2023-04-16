# Required imports
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import shotchartdetail
import json
from pathlib import Path
from scipy.stats import gaussian_kde

mavs_pbp_season = pd.read_parquet(str(Path.cwd()) + "/data/mavs_pbp_season.parquet")
all_players_data = pd.read_parquet(str(Path.cwd()) + "/data/player_data.parquet")

mavs_players_names = all_players_data[all_players_data['team'] == 'DAL']

# Find all the shots_taken for a specific player
def filter_by_player_shots_taken(player):
  playerId = int(player.at[0,'nbaId'])
  teamId = int(player.at[0,'nbaTeamId'])
  
  # Get the shot chart data for the player
  shot_chart_json = shotchartdetail.ShotChartDetail(team_id = teamId,
                                                    player_id = playerId,
                                                    context_measure_simple = 'PTS',
                                                    season_nullable = '2022-23',
                                                    season_type_all_star = 'Regular Season')
  
  shot_chart_data = json.loads(shot_chart_json.get_json())
  
  column_names = shot_chart_data['resultSets'][0]['headers']
  data = shot_chart_data['resultSets'][0]['rowSet']
  shot_locations_data = pd.DataFrame(data=data,columns=column_names)

  return shot_locations_data

def SeasonDataFiltering():
    st.header("Player Shot Analysis")

    # Select player to look at stats for
    with st.expander(label="**Filter the season data by a specific player**"):
        with st.form("PlayerShotsForm", clear_on_submit=True):
            player_name = st.selectbox(label="Select player", options=mavs_players_names['name'].unique(),
                                    help="Select the player you want to filter data for")
            player_shots_submitted = st.form_submit_button(label="Filter Data")

            if player_shots_submitted:
                player = mavs_players_names[mavs_players_names['name'] == str(player_name)].reset_index()
                player_pbp = mavs_pbp_season[(mavs_pbp_season['playerId1'] == player.at[0,'nbaId']) | (mavs_pbp_season['playerId2'] == player.at[0,'nbaId']) | (mavs_pbp_season['playerId3'] == player.at[0,'nbaId'])].reset_index()
                
                shots_df = filter_by_player_shots_taken(player)
                
                # Draw the basketball court with the data
                court_figure = plt.figure(figsize=(4, 3.76))
                court = court_figure.add_axes([0, 0, 1, 1])
                court.set_xticks([])
                court.set_yticks([])

                updated_y_values = [x + 60 for x in list(shots_df['LOC_Y'])]
                kde = gaussian_kde(np.vstack([shots_df['LOC_X'], updated_y_values]))
                x_values, y_values = np.mgrid[shots_df['LOC_X'].min():shots_df['LOC_X'].max():shots_df['LOC_X'].size**0.5*1j,
                                            min(updated_y_values):max(updated_y_values):len(updated_y_values)**0.5*1j]
                z_values = kde(np.vstack([x_values.flatten(), y_values.flatten()]))
                court.contourf(x_values, y_values, z_values.reshape(x_values.shape), alpha=0.5)
                empty_court = plt.imread(str(Path.cwd()) + "/analytics_images/empty_court.png")
                court.imshow(empty_court, extent=[shots_df['LOC_X'].min(), shots_df['LOC_X'].max(), 
                                                min(updated_y_values), max(updated_y_values)], aspect='auto')
                plt.savefig(str(Path.cwd()) + "/analytics_images/{0}.png".format(player_name))
                image = Image.open(str(Path.cwd()) + "/analytics_images/{0}.png".format(player_name))
                st.write('{0} 2022-2023 Regular Season Shotmaking'.format(player_name))
                st.image(image)

                st.write("Offensive Plays By {0}".format(player_name))
                off_pie_fig, off_pie = plt.subplots()
                sizes = player_pbp['offensive_play'].value_counts(normalize=True)
                labels = list(player_pbp['offensive_play'].unique())
                if None in labels:
                    labels.remove(None)
                labels = ['{0} - {1} %'.format(i,np.round(j/sum(sizes)*100,2)) for i,j in zip(labels, sizes)]
                off_pie.pie(sizes, shadow=True, startangle=90)
                off_pie.axis('equal')
                off_pie.legend(labels=labels, bbox_to_anchor=(1,1), fontsize=8)
                plt.tight_layout()
                plt.savefig(str(Path.cwd()) + "/analytics_images/{0}_off_plays.png".format(player_name))
                image = Image.open(str(Path.cwd()) + "/analytics_images/{0}_off_plays.png".format(player_name))
                st.image(image)

                st.write("Defensive Plays By {0}".format(player_name))
                def_pie_fig, def_pie = plt.subplots()
                sizes = player_pbp['defensive_play'].value_counts(normalize=True)
                labels = list(player_pbp['defensive_play'].unique())
                if None in labels:
                    labels.remove(None)
                labels = ['{0} - {1} %'.format(i,np.round(j/sum(sizes)*100,2)) for i,j in zip(labels, sizes)]
                def_pie.pie(sizes, shadow=True, startangle=90)
                def_pie.axis('equal')
                def_pie.legend(labels=labels, bbox_to_anchor=(1,1), fontsize=8)
                plt.tight_layout()
                plt.savefig(str(Path.cwd()) + "/analytics_images/{0}_def_plays.png".format(player_name))
                image = Image.open(str(Path.cwd()) + "/analytics_images/{0}_def_plays.png".format(player_name))
                st.image(image)
                
    