import os

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
from pathlib import Path
import process_data
from SeasonDataFiltering import SeasonDataFiltering
from Matchups import Matchups
from Lineups import Lineups

# Players
players_mavs = ["Luka Doncic", "Kyrie Irving", "Justin Holiday", "Theo Pinson", "Jaden Hardy", "Dwight Powell",
                 "Josh Green", "Tim Hardaway Jr.", "Markieff Morris", "Frank Ntilikina", "Reggie Bullock",
                 "Christian Wood", "Maxi Kleber", "Davis Bertans", "Javale McGee", "AJ Lawson"]
# image folder
image_folder = "images"

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


# Define the Streamlit app layout
st.set_page_config(page_title="Data Mavericks", layout="wide")

image_name = "mavs.png"
image_path = os.path.join(image_folder, image_name)
st.sidebar.image(image_path, width=200)  # Add an image to the sidebar
st.sidebar.title("DataMavericks")
tabs = ["Lineups", "Matchups", "Season Data Filtering"]
selected_tab = st.sidebar.radio("Navigation", tabs, index=0)

# Run the appropriate function based on the selected tab
if selected_tab == "Lineups":
    Lineups()
elif selected_tab == "Matchups":
    Matchups()
elif selected_tab == "Season Data Filtering":
    SeasonDataFiltering()
