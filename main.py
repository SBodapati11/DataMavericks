import os

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
from pathlib import Path


# Players
players_mavs = ["Luka Doncic", "Kyrie Irving", "Justin Holiday", "Theo Pinson", "Jaden Hardy", "Dwight Powell",
                 "Josh Green", "Tim Hardaway Jr.", "Markieff Morris", "Frank Ntilikina", "Reggie Bullock",
                 "Christian Wood", "Maxi Kleber", "Davis Bertans", "Javale McGee", "AJ Lawson"]
# image folder
image_folder = "images"

# Define function for the first tab
def Lineups():
    st.header("Lineups")

    teams = ["Dallas Mavericks", "Los Angeles Lakers", "Golden State Warriors", "Brooklyn Nets"]
    selected_team = st.selectbox("Select a team", teams, index=0)

    if selected_team == "Dallas Mavericks":
        st.markdown("Current Team: **Dallas Mavericks** (click to change)")
    elif selected_team == "Los Angeles Lakers":
        st.markdown("Current Team: **Los Angeles Lakers** (click to change)")
    elif selected_team == "Golden State Warriors":
        st.markdown("Current Team: **Golden State Warriors** (click to change)")
    else:
        st.markdown("Current Team: **Brooklyn Nets** (click to change)")

    # Define the table headers
    headers = ["Player Name", "Position", "Height(ft\"in)", "Weight(lbs)", "Info"]

    # TEAM TABLE - Dallas Mavericks
    if selected_team == "Dallas Mavericks":
        # Define the data for the first row
        data = {
            "Player Name": "Luka Doncic",
            "Position": "PG",
            "Height(ft\"in)": "6'7\"",
            "Weight(lbs)": 230,
            "Info": "Lorem ipsum dolor sit amet"
        }
    # TODO - Fill in more possible teams and their players
    else:
        data = {
            "Player Name": "Check Back Later!",
            "Position": "Nonexistent",
            "Height(ft\"in)": "5'12\"",
            "Weight(lbs)": 100,
            "Info": "Under Construction"
        }
    # Create a list of data that contains the first row and the remaining rows with ellipses
    data_list = [data] + [{"...": "..." for _ in range(len(headers))} for _ in range(9)]

    # Create a Pandas DataFrame object from the list of data and the headers
    df = pd.DataFrame(data_list, columns=headers)

    # Display the table in Streamlit
    st.table(df)


# Define function for the second tab
def Matchups():
    st.header("Matchups")

    Players_2 = ["Bryant Test", "Papa's pizzeria", "Gray Domino", "Black Velvet", "Chcolate Coating"]
    st.write(f"<span style='color: blue'><b>Select Player 1</b></span>", unsafe_allow_html=True)
    selected_player_1 = st.selectbox(" ", players_mavs)
    st.write(f"<span style='color: red'><b>Select Player 2</b></span>", unsafe_allow_html=True)
    selected_player_2 = st.selectbox(" ", Players_2)
    # TODO - Pull up selected_player_1's stats and selected_player_2's stats and run algorithmic magic on them woo
    # pit players against each other and run probability of p1 beating p2
    estimated_chance = 49

    # after doing that, put them next to each other using an automatically pulled image
    image_name = "{0}.png".format(selected_player_1.split()[0].lower())
    image_path = os.path.join(image_folder, image_name)
    fighter1_image = Image.open(image_path)

    # TODO - Make the second fighter automatic
    image_2_name = "testbryant.png"
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


# Define function for the third tab
def Shooting_Calculator():
    st.header("Shooting Calculator")

    st.write(f"<span style='color: blue'><b>Select Player</b></span>", unsafe_allow_html=True)
    selected_player_1 = st.selectbox(" ", players_mavs, index=0)

    basketball_shots = ['Jump Shot', 'Layup', 'Dunk', 'Hook Shot', 'Tip Shot', 'Alley-oop', 'Free Throw',
                        'Three-Pointer']
    st.write(f"<span style='color: red'><b>Select a Shot</b></span>", unsafe_allow_html=True)
    selected_shot = st.selectbox(" ", basketball_shots, index=0)

    # TODO: Actually calculate the chance he has using a time series
    estimated_chance = 99.875

    # TODO: Make this graph take in actual data
    # Generate sample data
    time = pd.date_range("2022-01-01", periods=100, freq="1min")
    y = np.random.randn(100)
    y = np.abs(y)  # Make all values positive

    # Create two columns
    col1, col2 = st.columns([1, 2])

    # TODO: match selected_player_1 to its image mapping
    with col1:
        # after doing that, put them next to each other using an automatically pulled image
        image_name = "{0}.png".format(selected_player_1.split()[0].lower())
        image_path = os.path.join(image_folder, image_name)
        selection = Image.open(image_path)
        st.image(selection, use_column_width=True)

    # Add line chart to the second column
    with col2:
        # Create dataframe with sample data
        df = pd.DataFrame({"time": time, "y": y})

        # Create line chart
        line_chart = (
            alt.Chart(df)
            .mark_line(color="darkblue")
            .encode(
                x="time:T",
                y="y:Q",
            )
        )

        # Create filled area below the line chart
        area_chart = (
            alt.Chart(df)
            .mark_area(color="lightblue", opacity=0.3)
            .encode(
                x="time:T",
                y=alt.Y("y:Q", stack=None),
                tooltip=["y:Q"],
            )
        )

        # Combine the line chart and area chart
        chart = line_chart + area_chart

        # Set chart size and title
        chart.properties(width=700, height=400, title="Sample Line Chart with Filled Area")

        # Display the chart
        st.altair_chart(chart, use_container_width=True)

    # Add more code here for custom functionality
    # Write Prediction
    st.subheader("Prediction")
    st.write(
        f"<span style='color: blue'>{selected_player_1}</span> has a <b>{str(estimated_chance)}</b> chance of making a <b>{selected_shot}</b>.",
        unsafe_allow_html=True)


def Log_Off():
    st.header("Log Off")


# Define the Streamlit app layout
st.set_page_config(page_title="Data Mavericks", layout="wide")

image_name = "mavs.png"
image_path = os.path.join(image_folder, image_name)
st.sidebar.image(image_path, width=200)  # Add an image to the sidebar
st.sidebar.title("DataMavericks")
tabs = ["Lineups", "Matchups", "Shooting Calculator", "Log Off"]
selected_tab = st.sidebar.radio("Navigation", tabs, index=0)

# Run the appropriate function based on the selected tab
if selected_tab == "Lineups":
    Lineups()
elif selected_tab == "Matchups":
    Matchups()
elif selected_tab == "Shooting Calculator":
    Shooting_Calculator()
else:
    Log_Off()
