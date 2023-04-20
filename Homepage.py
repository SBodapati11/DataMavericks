import streamlit as st


def Homepage():
    st.title("🏠 Welcome to DataMavericks!")
    st.image("images/App/Logo.png", width=200)
    st.header("A one-stop-shop AI powerhouse dashboard for the Mavs!")

    st.subheader("__Team vs Team.__")
    st.subheader("__Player vs player.__")
    st.subheader("__Player vs self.__")

    st.markdown("As longtime fans of the Mavs, we seek to put them through hypothetical scenarios to help them in "
                "these three through the use of AI. Introducing DataMavericks, an AI-powered dashboard that can "
                "generate optimal lineups, match player against player, and track player behavior for improvement "
                "using play-by-play data.")

    st.markdown("But don't let us tell you about it. **Try it out for yourself.**")

    st.markdown("⬅️ Use the sidebar to begin!")
