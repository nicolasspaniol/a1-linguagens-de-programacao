import pandas as pd
import numpy as np
import seaborn as sns

countries = {}

club_games = pd.read_csv("dataset/club_games.csv")
clubs = pd.read_csv("dataset/clubs.csv")
competitions = pd.read_csv("dataset/competitions.csv")

games_away = club_games.loc[club_games.hosting == "Away"]

for row in clubs.itertuples():
    country = competitions.loc[competitions.competition_id == row.domestic_competition_id, "country_name"].values[0]
    countries[row.club_id] = country

print(countries)

# vitorias_fora
# derrotas_fora
# empates_fora
# vitorias_exterior
# derrotas_exterior
# empates_exterior
