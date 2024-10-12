import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedFormatter, FixedLocator, PercentFormatter
import numpy as np
from datetime import date, datetime

sns.set_theme(style="ticks", palette="pastel")

players = pd.read_csv('data/football/players.csv')
players["date_of_birth"] = pd.to_datetime(players["date_of_birth"])

# Cria uma nova coluna na tabela com o mês do aniversário de cada jogador
players["month_of_birth"] = players["date_of_birth"].map(lambda d: d.month)

# Cria uma tabela com a quantidade de aniversariantes por mês
month_frequency = players.groupby(["month_of_birth"]).size().reset_index(name="count")

# Adiciona uma coluna com a proporção de aniversariantes por mês
quantity_players = month_frequency["count"].sum()
month_frequency["frequency"] = month_frequency["count"] / quantity_players * 100

# Calcula o desvio padrão da distribuição da quantidade de jugadores por mês
dp = month_frequency["count"].std()
print(f"Desvio padrão de aniversariantes por mês: {dp}")

meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

ax = sns.barplot(month_frequency, x="month_of_birth", y="frequency")
ax.xaxis.set_label_text("Mês de nascimento")
ax.yaxis.set_label_text("Percentual de jogadores")
ax.xaxis.set_major_locator(FixedLocator(range(len(meses))))
ax.xaxis.set_major_formatter(FixedFormatter(meses))
ax.yaxis.set_major_formatter(PercentFormatter())
plt.show()
