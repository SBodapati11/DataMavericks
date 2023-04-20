import os

import streamlit as st
from SeasonDataFiltering import SeasonDataFiltering
from Matchups import Matchups
from Lineups import Lineups
from Homepage import Homepage

# Players
players_mavs = ["Luka Doncic", "Kyrie Irving", "Justin Holiday", "Theo Pinson", "Jaden Hardy", "Dwight Powell",
                 "Josh Green", "Tim Hardaway Jr.", "Markieff Morris", "Frank Ntilikina", "Reggie Bullock",
                 "Christian Wood", "Maxi Kleber", "Davis Bertans", "Javale McGee", "AJ Lawson",
                "Dorian Lawrence Finney-Smith", "Spencer Dinwiddie"]
# image folder
image_folder = "images"

# Define the Streamlit app layout
st.set_page_config(page_title="Data Mavericks", layout="wide")

image_name = "App/Logo.png"
image_path = os.path.join(image_folder, image_name)
st.sidebar.image(image_path, width=200)  # Add an image to the sidebar
st.sidebar.title("DataMavericks")
tabs = ["🏠 Homepage", "🏀 Lineups", "⛹️ Matchups", "🗑️ Player Shot Analysis"]
selected_tab = st.sidebar.radio("Navigation", tabs, index=0)

# Run the appropriate function based on the selected tab
if selected_tab == "🏠 Homepage":
    Homepage()
elif selected_tab == "🏀 Lineups":
    Lineups()
elif selected_tab == "⛹️ Matchups":
    Matchups()
elif selected_tab == "🗑️ Player Shot Analysis":
    SeasonDataFiltering()
