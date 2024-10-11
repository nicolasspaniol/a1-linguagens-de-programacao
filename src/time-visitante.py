import pandas as pd
import numpy as np
import seaborn.objects as so
from summary_statistics import cramer_v


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

games["result"] = games.apply(calc_resultado, axis=1)

games["is_international"] = games["competition_type"] == "international_cup"

games_frequency = games.groupby(["result", "is_international"]).size().reset_index(name="count")

total_international = games_frequency.loc[games_frequency["is_international"]]["count"].sum()
total_home = games_frequency.loc[~games_frequency["is_international"]]["count"].sum()

pivot = games_frequency.pivot_table(index="result", columns="is_international", values="count")

games_frequency["count"] = np.where(games_frequency["is_international"] == True, games_frequency["count"] /
                                    total_international, games_frequency["count"] / total_home)

print(f"V de Cramer das variáveis 'is_international' e 'result': {round(cramer_v(pivot), 2)}")
ax = so.Plot(games_frequency, x="is_international", y="count", color="result") \
    .add(so.Bar(), so.Stack()) \
    .label(x="É internacional", y="Frequência relativa", color="Resultado da partida")
ax.show()
