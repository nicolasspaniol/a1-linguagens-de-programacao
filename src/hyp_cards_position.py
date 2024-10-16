"""
Módulo responsável por responder a hipótese:
"A posição dos jogadores em campo influencia na quantidade de cartões que estes recebem?"
"""

import pandas as pd
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt
import textwrap


sns.set_theme(style="ticks", palette="pastel")

game_events = pd.read_csv("data/football/game_events.csv")
game_lineups = pd.read_csv("data/football/game_lineups.csv")

# Filtra apenas os eventos de cartões
game_events = game_events.loc[game_events["type"] == "Cards"]

game_events["card_type"] = game_events["description"] \
    .map(lambda e: "yellow" if "yellow" in e.lower() else "red")

merged = pd.merge(
    game_events,
    game_lineups,
    how="inner",
    on=["game_id", "player_id"]
).groupby(["card_type", "position"]).size().reset_index(name="count")

# Calcula a quantidade total de jogadores por posição
calc_total = lambda r: ((merged["position"] == r["position"]) * merged["count"]).sum()
merged["total_count"] = merged.apply(calc_total, axis=1)
merged["rel_count"] = merged.apply(lambda r: r["count"] / r["total_count"], axis=1)

# Filtra posições com quantidade insuficiente de dados
merged = merged.loc[merged["total_count"] > 150]
print(f"n = {merged['count'].sum()}")

# Gráfico de barras - quantidade de cartões recebidos por posição em campo
ax = sns.barplot(
    merged.loc[merged["card_type"] == "yellow"],
    x="position",
    y="count",
)
# Quebra o texto no eixo X em múltiplas linhas
labels = [textwrap.fill(label.get_text(), 12) for label in ax.get_xticklabels()]
ax.set_xticklabels(labels)
ax.xaxis.set_label_text("Posição em campo")
ax.yaxis.set_label_text("Número de jogadores")
plt.show()

merged["card_type"] = merged["card_type"].map(lambda e: "Vermelho" if e == "red" else "Amarelo")

# Gráfico de barras empilhadas - proporção de cartões vermelhos/amarelos por
# posição em campo
ax = so.Plot(merged, x="position", y="rel_count", color="card_type") \
    .add(so.Bar(), so.Stack()) \
    .scale(color={ "Amarelo": "orange", "Vermelho": "red" }) \
    .label(x="Posição em campo", y="Percentual do tipo de cartão", color="Tipo de cartão")
ax.show()
