import pandas as pd
import boto3
import io
import re
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Circle, Rectangle, Arc

# Get the play-by-play data

# Set Buffer
buffer_pbp = io.BytesIO()
buffer_players = io.BytesIO()

# Create connection to S3
s3 = boto3.resource('s3', aws_access_key_id = 'AKIAWNNDBSXELJDB2NPI', aws_secret_access_key = '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')

# Read PBP Data from S3
pbp_object = s3.Object('utd-hackathon', 'event_pbp.parquet')
pbp_object.download_fileobj(buffer_pbp)

# Read the PBP data into a pandas dataframe and save it
df_pbp = pd.read_parquet(buffer_pbp)

# Read Players Data from S3
players_object = s3.Object('utd-hackathon', 'game_players.parquet')
players_object.download_fileobj(buffer_players)

# Read the PBP data into a pandas dataframe and save it
df_players = pd.read_parquet(buffer_players)
df_players.to_parquet(str(Path.cwd()) + '/data/player_data.parquet')

# find keywords to extract from the mesage descriptions
# replace punctuation, lowercase, remove numbers expect 3 and others

# check if shots are missed ('Missed') or not('Made')
# check for assists and fouls
offensive_plays = ["turnaround fadeaway shot","free throw","3pt shot","driving finger roll layup shot",
                   "turnover lost ball","violation kicked ball","jump ball","turnover bad pass","floating jump shot",
                   "fadeaway jump shot","driving floating jump shot","driving layup shot","running layup shot",
                   "pullup jump shot","driving dunk shot","jump shot","cutting layup shot",
                   "tip layup shot","driving floating bank jump shot","running jump shot","cutting dunk shot",
                   "turnover traveling","turnaround hook shot","tip dunk shot","turnover offensive foul","step back jump shot",
                   "assist","dunk shot","hook shot","running finger roll layup","alley oop layup shot",
                   "turnaround jump shot","running pullup jump shot","turnover out of bounds"]

#offensive_plays_basic = ["fadeaway","jump","layup", "turnover","hook", "pullup", "step","3pt","dunk", "free"]
defensive_plays = ["steal","block", "rebound"]

# Get the data for the Mavericks Regular Season
seasons=["Regular"]
team_names = ['DAL']
mavs_pbp = df_pbp.loc[df_pbp['team'].isin(team_names)] 
mavs_pbp_season = mavs_pbp.loc[mavs_pbp['seasonType'].isin(seasons)]
mavs_pbp_season = mavs_pbp_season.reset_index(drop=True)

# Add columns for denote whether a play is offensive, defensive, off_missed, and the quarter
mavs_pbp_season['offensive_play'] = pd.Series(dtype=str)
mavs_pbp_season['defensive_play'] = pd.Series(dtype=str)
mavs_pbp_season['off_missed'] = pd.Series(dtype=str)
#mavs_pbp_season['quarter'] = pd.Series()

# Iterate to classify plays as an offensive or defensive play
c=0
for idx,row in mavs_pbp_season.iterrows():
    msg_str = row['description']
    msg_str = re.sub(r'[^\w\s]', '', msg_str)
    msg_str = msg_str.lower()
    msg_list = msg_str.split(" ")
    msg_list = [i for i in msg_list if i!='']
    msg_str = ' '.join(msg_list)
    c+=1
    for op in offensive_plays:
      if op in msg_str:
        #print(op)
        mavs_pbp_season.at[idx, 'offensive_play'] = op
        break
    for dp in defensive_plays:
      if dp in msg_str:
        mavs_pbp_season.at[idx, 'defensive_play'] = dp
        break
    if 'foul' in msg_str:
      mavs_pbp_season.at[idx, 'offensive_play'] = 'foul'

# iterate to find the missed shots
for idx,row in mavs_pbp_season.iterrows():
    msg_str = row['description']
    msg_str = re.sub(r'[^\w\s]', '', msg_str)
    msg_str = msg_str.lower()
    msg_list = msg_str.split(" ")
    msg_list = [i for i in msg_list if i!='']
    #print(msg_list)
    msg_str = ' '.join(msg_list)
    if 'missed' in msg_str:
      mavs_pbp_season.at[idx, 'off_missed'] = 1
    elif 'made' in msg_str:
      mavs_pbp_season.at[idx, 'off_missed'] = 0
    else:
      mavs_pbp_season.at[idx, 'off_missed'] = -1

mavs_pbp_season.to_parquet(str(Path.cwd())+ '/data/mavs_pbp_season.parquet')

# Function to draw a half-court basketball court (mostly) to scale
def draw_basketball_court(court):

  # Create 3-point arc
  three_point_arc = Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor='black', lw=2)

  # Create 3-point lines
  court.plot([-220, -220], [0, 140], linewidth=2, color='black')
  court.plot([220, 220], [0, 140], linewidth=2, color='black')

  # Create the rim
  rim = Circle((0, 60), 15, facecolor='none', edgecolor='black', lw=2)

  # Create the paint areas
  outer_rectangle = Rectangle((-80, 0), 160, 190, fill=False, lw=2, edgecolor='black')
  inner_rectangle = Rectangle((-60, 0), 120, 190, fill=False, lw=2, edgecolor='black')

  # Create free throw arc
  free_throw_arc = Arc((0, 190), 120, 120, theta1=0, theta2=180, facecolor='none', edgecolor='black', lw=2)

  # Create dotted free throw arc
  dotted_free_throw_arc = Arc((0, 190), 120, 120, theta1=-180, theta2=0, facecolor='none', edgecolor='black', lw=2, ls='-')
      
  # Create the backboard
  court.plot([-30, 30], [40, 40], linewidth=2, color='black')

  # Add all the components
  court.add_artist(three_point_arc)
  court.add_artist(free_throw_arc)
  court.add_artist(dotted_free_throw_arc)
  court.add_artist(rim)
  court.add_artist(outer_rectangle)
  court.add_artist(inner_rectangle)

  # Remove axes ticks and set the dimensions for the 
  court.set_xticks([])
  court.set_yticks([])
  court.set_xlim(-250, 250)
  court.set_ylim(0, 470)

  court.set_facecolor('#dfbb85')

  return court

# Draw the basketball court with the data
court_figure = plt.figure(figsize=(4, 3.76))
court = court_figure.add_axes([0, 0, 1, 1])
court = draw_basketball_court(court)

plt.savefig(str(Path.cwd()) + "/analytics_images/empty_court.png")