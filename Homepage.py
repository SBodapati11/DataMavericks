import streamlit as st


def Homepage():
    st.title("🏠 Welcome to DataMavericks!")
    st.header("A one-stop-shop AI powerhouse dashboard for the Mavs!")

    st.markdown("As longtime fans of the Mavs, we seek to put them through hypothetical scenarios to help them in \
                these three through the use of AI. Introducing DataMavericks, an AI-powered dashboard that can\
                generate optimal lineups, match player against player, and track player behavior for improvement \
                using play-by-play data. Here's a look at what we have to offer.")

    st.write("---------------------------------------------------------------------------------------")
    
    st.subheader("_Team vs Team_")
    st.write("Explore curated lineups against every team optimized and generated by our model.")

    st.subheader("_Player vs Player_")
    st.write("Compare potential matchups between Mavs players and opponent players.")

    st.subheader("_Player vs Self_")
    st.write("Review player performance for the 2022-2023 Season.")

    st.write("---------------------------------------------------------------------------------------")

    st.markdown("But don't let us tell you about it. **Try it out for yourself.**")

    st.markdown("⬅️ Use the sidebar to begin!")
