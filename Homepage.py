import streamlit as st

def Homepage():

    st.title("Home")
    st.image("images/App/Logo.png", width=200)
    st.header("Welcome to DataMavericks!")
    st.subheader("A one-stop-shop AI powerhouse dashboard for the Mavs!")

    st.markdown("__Team vs Team.__")
    st.markdown("__Player vs player.__")
    st.markdown("__Player vs self.__")

    st.markdown("As longtime fans of the Mavs, we seek to put them through hypothetical scenarios to help them in "
                "these three through the use of AI. Introducing DataMavericks, an AI-powered dashboard that can "
                "generate optimal lineups, match player against player, and track player behavior for improvement "
                "using play-by-play data.")

    st.markdown("But don't let us tell you about it. **Try it out for yourself.**")
