import pandas as pd
import numpy as np
import seaborn as sns

county = {}

club_games = pd.read_csv("dataset/club_games.csv")
clubs = pd.read_csv("dataset/clubs.csv")
competitions = pd.read_csv("dataset/competitions.csv")

games_away = club_games.loc[club_games.hosting == "Away"]

for row in clubs.iterrows():
    print(row)
    country = competitions.loc[row[1]].country_name
    # print(county)
    # countries[row.club_id] = 

# print(games_away.head())

# vitorias_fora
# derrotas_fora
# empates_fora
# vitorias_exterior
# derrotas_exterior
# empates_exterior
