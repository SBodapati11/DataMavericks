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
import seaborn as sns
import plotly.express as px

# Get the play by play and players data
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
    player_name = st.selectbox(label="**Filter the season data by a specific player**", options=mavs_players_names['name'].unique(),
                            help="Select the player you want to filter data for")

    player = mavs_players_names[mavs_players_names['name'] == str(player_name)].reset_index()
    player_pbp = mavs_pbp_season[(mavs_pbp_season['playerId1'] == player.at[0,'nbaId']) | (mavs_pbp_season['playerId2'] == player.at[0,'nbaId']) | (mavs_pbp_season['playerId3'] == player.at[0,'nbaId'])].reset_index()
    
    shots_df = filter_by_player_shots_taken(player)
    
    # Draw the basketball court with the data
    court_figure = plt.figure(figsize=(4, 3.76))
    court = court_figure.add_axes([0, 0, 1, 1])
    court.set_xticks([])
    court.set_yticks([])

    # Create the player's shot map using gaussian kde
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
    st.subheader('{0} 2022-2023 Regular Season Shotmaking'.format(player_name))
    st.image(image)

    # Create the player offensive play tree map
    st.subheader("Offensive Plays By {0}".format(player_name))
    off_pie_fig, off_pie = plt.subplots()
    sizes = player_pbp['offensive_play'].value_counts(normalize=True)
    labels = list(player_pbp['offensive_play'].unique())
    if None in labels:
        labels.remove(None)
    labels = ['{0} - {1} %'.format(i,np.round(j/sum(sizes)*100,2)) for i,j in zip(labels, sizes)]
    #off_pie.pie(sizes, shadow=True, startangle=90)
    colors = ['#002B5E','#000000','#FFFFFF']
    fig = px.treemap(
        names=sizes.index,
        parents=['Offensive'] * len(sizes),
        values=sizes.values * 100,
        color=sizes.values,
        color_continuous_scale=colors,
        #hover_data={'%': np.round(sizes.values*100, 2)},
        labels={'names': 'Type', 'parents': 'Play'}
    )
    # Format the text to display on hover
    fig.update_traces(hovertemplate='%{label} - %{value:.2f} %<extra></extra>')

    # set the background color and grid color
    fig.update_layout(
        paper_bgcolor="#00538C",
        plot_bgcolor="#00538C",
        width=800,
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    fig.update_layout(coloraxis_colorbar=dict(tickfont_color='white'))
    off_pie.axis('equal')
    plt.tight_layout()

    #off_pie.legend(labels=labels, bbox_to_anchor=(1,1), fontsize=8)
    #plt.savefig(str(Path.cwd()) + "/analytics_images/{0}_off_plays.png".format(player_name))
    #image = Image.open(str(Path.cwd()) + "/analytics_images/{0}_off_plays.png".format(player_name))
    #st.image(image)

    fig.write_html(str(Path.cwd()) + "/analytics_images/{0}_off_plays.html".format(player_name))
    with open(str(Path.cwd()) + "/analytics_images/{0}_off_plays.html".format(player_name), 'r', encoding="UTF-8") as f:
        html_string = f.read()
    st.components.v1.html(html_string, width=800, height=600)


    # Create the player defensive play graph
    st.subheader("Defensive Plays By {0}".format(player_name))
    def_pie_fig, def_pie = plt.subplots()
    sizes = player_pbp['defensive_play'].value_counts(normalize=True)
    labels = list(player_pbp['defensive_play'].unique())
    if None in labels:
        labels.remove(None)
    labels = ['{0} - {1} %'.format(i,np.round(j/sum(sizes)*100,2)) for i,j in zip(labels, sizes)]
    #def_pie.pie(sizes, shadow=True, startangle=90)
    def_colors =['#002B5E','#000000','#FFFFFF']
    def_pie.pie(sizes, shadow=True, startangle=90,autopct=None, counterclock=False, textprops={'color': 'black', 'fontsize': 12, 'fontweight': 'bold'}, colors=def_colors)
    def_pie_fig.set_facecolor('none')

    def_pie.axis('equal')
    def_pie.legend(labels=labels, bbox_to_anchor=(1,1), fontsize=8)
    plt.tight_layout()
    plt.savefig(str(Path.cwd()) + "/analytics_images/{0}_def_plays.png".format(player_name))
    image = Image.open(str(Path.cwd()) + "/analytics_images/{0}_def_plays.png".format(player_name))
    st.image(image)
    

