# DataMavericks

## What it does
DataMavericks, or DataMavs for short, is a one-stop shop for analyzing Dallas Mavericks player performance and optimizing matchups based on lineups and player performance. A powerhouse dashboard run by AI, DataMavs allows users to do a wide variety of functionalities, including:

* Viewing hypothetical lineups
* Compare players across different teams
* Analyze player shots on the Mavs.

## How to run
Simply run `streamlit run main.py` and the website should load.

Refer to *[Requirements](Requirements.md)* for more information about the necessary libraries/modules used in this project.

## How we built it

* For the frontend, we used **Streamlit** and **CSS**.
* For the backend, we used **Python** and **Jupyter Notebooks**.

## The Secret Sauce(s)
We analyze and display three particular statistics
* **Optimizing Lineup**
    1. For lineup optimization, the player data for the season is used. Initial preprocessing helps us aggregate player performance for Dallas Mavericks based on the opponent team. Since the whole goal of optimization is to create an offense and defense score based on the numerous features such as fgm, fga, plusMinus we use **Principal Component Analysis** to reduce the numerous features to simply two features - offense and defense. <br>
    2. Following our reduced features we can build lineups based on Starting Position and the constraint of 5 players on the field. We use **unsupervised learning** specifically **KMeans** clustering to generate clusters of players for every starting position to then create unique lineups for games against every team, along with the ability to optimize the lineup for Offense Score or Defense Score.
* **Optimizing Matchup**
    1. To create matchups for individual players we used **Feature Engineering** to divide the dataset into offensive vs defensive players by team and also create additional features for our model to use for offense or defense stats generation based on player performance. A thing to consider was to ensure that opponent team was considered when creating a score
    2. Following feature generation a **Random Forest Regressor** is used to train our dataset and then generate offense and defense scores for the players on the same plane. For predicting who wins the matchup a simple comparison is done based on the weighted averages of the score.
* **Spatial Shot Analysis**
    1. Given a player from the Mavericks, view heat maps of where the players take their shots (and how frequently). This uses **KDE** to determine density-based player areas; the denser the area, the hotter the heatmap. 
    2. Also view the percentage of offensive shots.
    3. The best offense is a good defense, so view their defenses as well!

## Challenges we ran into
Figuring out what we wanted to include and filtering the data was important. 

## Accomplishments that we're proud of
We can pit real-life players in hypothetical scenarios. We can also generate hypothetical scenarios ourselves.

## What we learned
We learnt a lot about the Mavs and the power of predictive artificial intelligence.

## What's next for DataMavericks
* Medical Information to track  hurt/resting players 
* Scouting for Trade and Free Agency Market
* Create custom players for a Fantasy Basketball league
* Calculator to assess shooting performance from PBP data
