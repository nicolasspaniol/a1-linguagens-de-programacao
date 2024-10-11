import pandas as pd
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import textwrap


sns.set_theme(style="ticks", palette="pastel")

game_events = pd.read_csv("data/game_events.csv")
game_lineups = pd.read_csv("data/game_lineups.csv")

# Filtra apenas os eventos de cartões
game_events = game_events.loc[game_events["type"] == "Cards"]

# Cria uma coluna para o tipo de cartão: amarelo ou vermelho
game_events["card_type"] = game_events["description"] \
    .map(lambda e: "yellow" if "yellow" in e.lower() else "red")

# Junta a tabela com os cartões com a tabela de escalações das partidas
merged = pd.merge(
    game_events,
    game_lineups,
    how="inner",
    on=["game_id", "player_id"]
).groupby(["card_type", "position"]).size().reset_index(name="count")

calc_rel_count = lambda r: ((merged["position"] == r["position"]) * merged["count"]).sum()
calc_total_count = lambda r: r["count"] / r["total_count"]
merged["total_count"] = merged.apply(calc_total_count, axis=1)
merged["rel_count"] = merged.apply(calc_rel_count, axis=1)

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
plt.show()

# Gráfico de barras empilhadas - proporção de cartões vermelhos/amarelhos por
# posição em campo
ax = so.Plot(merged, x="position", y="rel_count", color="card_type") \
    .add(so.Bar(), so.Stack()) \
    .scale(color={"yellow":"orange","red":"red"})
ax.show()
