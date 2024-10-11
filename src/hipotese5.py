from datetime import date, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import inflation

"""
Jogadores com preço fora do comum tem o desempenho proporcional?
"""

#Função para abrir arquivos csv
def open_csv(arquivo : str) -> pd.core.frame.DataFrame:
    with open('../data/'+arquivo+'.csv', 'r', encoding='latin1') as file:
        return pd.read_csv(file)

#Função correção da data_diff
def correct_data_diff(row : pd.core.series.Series) -> int:
    if not row["same_player"]:
        return min((datetime.now().date() - row["date"].date()).days, 365)
    return row["date_diff"].days

#Função media ponderada do valor do jogador
def calc_mean_price(group : pd.core.frame.DataFrame) -> float:
    return round(sum(group["market_value_in_eur"] * group["date_diff"]) / sum(group["date_diff"]), 2)

def calc_performance(group : pd.core.frame.DataFrame) -> float:
    return round(sum((-1)*group["yellow_cards"] + (-3)*group["red_cards"] + (8)*group["goals"] + (5)*group["assists"]) * 100 / group.shape[0], 4)

def calc_upper_limit(col : pd.core.series.Series) -> float:
    q1 = col.quantile(0.25)
    q3 = col.quantile(0.75)
    return q3 + 1.5 * (q3 - q1)

#Abrindo as tabelas que serão utilizadas
appearances = open_csv("appearances")
player_valuations = open_csv("player_valuations")
players = open_csv("playes")

#Limpando dados NaN das colunas que serão utilizadas
appearances.dropna(axis=0, subset=["yellow_cards", "red_cards", "goals", "assists"], inplace=True) 
player_valuations.dropna(axis=0, subset=["market_value_in_eur", "date"], inplace=True)
players.drop(axis=0, subset=["name"], inplace=True)

#Criando mean_price
#Ordenar os dados, converter data, corrigir valores, criar colunas same_player e date_diff, calcular a média ponderada
player_valuations.sort_values(['player_id', 'date'], ascending=True, inplace=True)
player_valuations["date"] = pd.to_datetime(player_valuations["date"], yearfirst=True)
player_valuations["market_value_in_eur"] = inflation.inflation_adj(player_valuations["market_value_in_eur"], player_valuations["date"])
player_valuations["same_player"] = -player_valuations["player_id"].diff(-1) == 0
player_valuations["date_diff"] = -player_valuations["date"].diff(-1)
player_valuations["date_diff"] = player_valuations.apply(correct_data_diff, axis=1)
mean_price = player_valuations.groupby("player_id").apply(calc_mean_price).reset_index(name="mean_price")

#Criando performance
#Ordenar os dados, calcular performance do jogador
appearances.sort_values('player_id', ascending=True, inplace=True)
performance = appearances.groupby("player_id").apply(calc_performance).reset_index(name="performance")

#Unindo os dados
merged = pd.merge(players["player_id", "name"], performance, mean_price, how="left", on="player_id").dropna(axis=0).sort_values("mean_price", ascending=True)

#Calculando limite superior
merged["log_mean_price"] = np.log(merged["mean_price"])
upper_limit = calc_upper_limit(merged["mean_price"])
performance_upper = merged[merged["mean_price"] >= upper_limit]

#Plotando os gráficos
print(performance_upper.describe())
print(np.corrcoef(performance_upper["performance"], performance_upper["mean_price"])[0,1])
sns.scatterplot(data=performance_upper, x="log_mean_price", y="performance", color="red")
plt.show()


