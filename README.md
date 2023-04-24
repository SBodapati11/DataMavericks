## What it does
DataMavericks, or DataMavs for short, is a one-stop shop for analyzing Dallas Mavericks individual player performance and optimizing matchups and lineups based on season statistics. A powerhouse dashboard run by AI, DataMavs allows users to do a wide variety of functionalities, including:

* Viewing potential lineups
* Comparing players across different teams
* Analyzing Mavs player shotmaking trends

## How to run
Simply run `streamlit run main.py` and the website should load.

## How we built it

* For the frontend, we used **Streamlit** and **CSS**.
* For the backend, we used **Python** and **Jupyter Notebooks**.

## The Secret Sauce(s)
We analyze and display three particular statistics
* **Optimizing Lineup**
    1. For lineup optimization, the player data for the season is used. Initial preprocessing helps us aggregate player performance for Dallas Mavericks based on the opponent team. Since the whole goal of optimization is to create an offense and defense score based on the numerous features such as fgm, fga, plusMinus we use **Principal Component Analysis** to reduce the numerous features to simply two features - offense and defense. <br>
    2. Following our reduced features we can build lineups based on Starting Position and the constraint of 5 players on the court. We use **unsupervised learning**, specifically **KMeans** clustering, to generate clusters of players for every starting position to then create unique lineups for games against every team, along with the ability to optimize the lineup for Offense Score or Defense Score.
* **Optimizing Matchup**
    1. To create matchups for individual players we used **Feature Engineering** to divide the dataset into offensive vs defensive players by team and also create additional features for our model to use for offense or defense stats generation based on player performance. A thing to consider was to ensure that opponent team was considered when creating a score.
    2. Following feature generation a **Random Forest Regressor** is used to train our dataset and then generate offense and defense scores for the players on the same plane. Predicting who wins the matchup is done through a simple comparison is done based on the weighted averages of the score.
* **Spatial Shot Analysis**
    1. Given a player from the Mavericks, view heat maps of where the players take their shots (and how frequently). This uses **Gaussian Kernel Density Estimation** to determine the distribution and frequency of player shots on the  court. The distribution is displayed using a heat-map overlaid on the court, with a lighter color indicating higher frequency.
    2. View the percentage of each type of offensive play made by the given player.
    3. The best offense is a good defense, so view their defensive play distribution as well!

## Challenges we ran into
The primary challenge was filtering out the vast amount of data available to us and organizing the data/analysis to tell a story. We focused on making the dashboard as easy to use as possible for coaches and players alike while telling a story using our 3-functionality approach.

## Accomplishments that we're proud of
From just one season's worth of play-by-play and player data, we were able to extract so much valuable information and correctly utilize it to create our dashboard.

## What we learned
We learnt a lot about the play-making tendencies of the Dallas Mavericks and witnessed the power of predicting machine learning/analytics.

## What's next for DataMavericks
* Medical Information to track hurt/resting players 
* Scouting for Trade and Free Agency Market
* Create custom players for a Fantasy Basketball league
* Calculator to assess shooting performance from PBP data
