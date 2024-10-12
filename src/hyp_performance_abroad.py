"""
Módulo responsável por responder a hipótese:
"Dentre os times visitantes de cada partida, jogar dentro ou fora do país influencia o resultado da partida? (vitória, empate ou derrota)"
"""

import pandas as pd
import numpy as np
import seaborn.objects as so
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from summary_statistics import cramer_v


def label_result(r):
    # Para evitar mais consultas que o necessário
    home_goals = r["home_club_goals"]
    away_goals = r["away_club_goals"]

    if home_goals > away_goals:
        return "Derrota"
    if home_goals == away_goals:
        return "Empate"
    if home_goals < away_goals:
        return "Vitória"


club_games = pd.read_csv("data/football/club_games.csv")
games = pd.read_csv("data/football/games.csv")

# Cria coluna com o resultado da partida: vitória, empate ou derrota
games["result"] = games.apply(label_result, axis=1)
games["is_international"] = games["competition_type"] == "international_cup"

# Agrupa e conta a frequência de partidas dentro/fora do país para cada resultado
games_freq = games.groupby(["result", "is_international"]).size().reset_index(name="count")

total_international = games_freq.loc[games_freq["is_international"]]["count"].sum()
total_home = games_freq.loc[~games_freq["is_international"]]["count"].sum()

# Divide em uma tabela de dupla entrada por 'is_international' e 'result'
pivot = games_freq.pivot_table(index="result", columns="is_international", values="count")

games_freq["freq"] = np.where(games_freq["is_international"] == True, games_freq["count"] /
                                    total_international, games_freq["count"] / total_home)

# Renomeia os valores da coluna 'is_international': True -> "Fora do país",
# False -> "Dentro do país"
label_fun = lambda e: "Fora do país" if e else "Dentro do país"
games_freq["is_international"] = games_freq["is_international"].map(label_fun)

# Calcula o V de Cramer, que indica a associação entre os eixos da tabela
print(f"V de Cramer das variáveis 'is_international' e 'result': {round(cramer_v(pivot), 2)}")

p: so.Plot = so.Plot(games_freq, x="is_international", y="freq", color="result") \
    .add(so.Bar(), so.Stack()) \
    .label(x="Localização", y="Percentual dos resultados", color="Resultado da partida")

p.show()
