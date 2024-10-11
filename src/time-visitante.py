import pandas as pd
import numpy as np
import seaborn.objects as so


def calc_resultado(r):
    # Para evitar mais consultas que o necessário
    home_goals = r["home_club_goals"]
    away_goals = r["away_club_goals"]

    if home_goals > away_goals:
        return "derrota"
    if home_goals == away_goals:
        return "empate"
    if home_goals < away_goals:
        return "vitória"


club_games = pd.read_csv("data/club_games.csv")
games = pd.read_csv("data/games.csv")

games_abroad = games.loc[games.competition_type == "international_cup"]
games_home_country = games.loc[games.competition_type != "international_cup"]

games["resultado"] = games.apply(calc_resultado, axis=1)

games["is_international"] = games["competition_type"] == "international_cup"

games_frequency = games.groupby(["resultado", "is_international"]).size().reset_index(name="count")

total_international = games_frequency.loc[games_frequency["is_international"]]["count"].sum()
total_home = games_frequency.loc[~games_frequency["is_international"]]["count"].sum()
games_frequency["count"] = np.where(games_frequency["is_international"] == True, games_frequency["count"] / total_international, games_frequency["count"] / total_home)

ax = so.Plot(games_frequency, x="is_international", y="count", color="resultado") \
    .add(so.Bar(), so.Stack())
ax.show()
