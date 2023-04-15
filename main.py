import streamlit as st


# Define function for the first tab
def Lineups():
    st.header("Lineups")
    st.write("This is the content for Lineups.")
    # Add more code here for custom functionality


# Define function for the second tab
def Matchups():
    st.header("Matchups")
    st.write("This is the content for Matchups.")
    # Add more code here for custom functionality


# Define function for the third tab
def Shooting_Calculator():
    st.header("Shooting Calculator")
    st.write("This is the content for Shooting Calculator.")
    # Add more code here for custom functionality


def Log_Off():
    st.header("Log Off")


# Define the Streamlit app layout
st.set_page_config(page_title="Data Mavericks", layout="wide")
st.sidebar.title("DataMavericks")
tabs = ["Lineups", "Matchups", "Shooting Calculator"]
selected_tab = st.sidebar.radio("", tabs)

# Run the appropriate function based on the selected tab
if selected_tab == "Lineups":
    Lineups()
elif selected_tab == "Matchups":
    Matchups()
elif selected_tab == "Shooting Calculator":
    Shooting_Calculator()
else:
    Log_Off()