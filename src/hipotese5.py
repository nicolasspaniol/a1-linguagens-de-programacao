"""
Jogadores com preço fora do comum tem o desempenho proporcional?
"""

from datetime import date, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import inflation

#Função correção da data_diff
def correct_data_diff(row : pd.core.series.Series) -> int:
    """ 
    Corrige a diferença de datas entre registros de um jogador, ajustando para um limite de 365 dias se necessário.
    Se o jogador mudou de clube (ou não é o mesmo jogador), a diferença entre as datas será calculada até o máximo de 365 dias.
    Caso contrário, mantém a diferença original de datas.

        :param row: Série contendo informações de data e se é o mesmo jogador.
        :return: Diferença de dias entre as datas, ajustada ou original.
    """
    if not row["same_player"]:
        return min((datetime.strptime("30/09/2024", "%d/%m/%Y").date() - row["date"].date()).days, 365)
    return row["date_diff"].days

#Função que calcula media ponderada do valor do jogador
def calc_mean_price(group : pd.core.frame.DataFrame) -> float:
    """ 
    Calcula a média ponderada do valor de mercado de um jogador com base na duração de tempo em que ele manteve esse valor.
    O cálculo utiliza a diferença de dias (date_diff) como peso para calcular a média ponderada do valor de mercado.

        :param group: DataFrame contendo o valor de mercado e a diferença de datas para cada registro do jogador.
        :return: Média ponderada do valor de mercado, arredondada para duas casas decimais.
    """
    return round(sum(group["market_value_in_eur"] * group["date_diff"]) / sum(group["date_diff"]), 2)

#Função que calcula performance do jogador
def calc_performance(group : pd.core.frame.DataFrame) -> float:
    """ 
    Calcula o desempenho de um jogador com base em suas estatísticas de jogo, como gols, assistências e cartões.
    O desempenho é calculado com pesos específicos para cada estatística, resultando em um valor proporcional
    ao número de jogos (group.shape[0]).

        :param group: DataFrame com as estatísticas de desempenho (gols, assistências, cartões) do jogador.
        :return: Valor numérico do desempenho, arredondado para quatro casas decimais.
    """
    return round(sum((-1)*group["yellow_cards"] + (-3)*group["red_cards"] + (8)*group["goals"] + (5)*group["assists"]) * 100 / group.shape[0], 4)

#Função que calcula o limite superior
def calc_upper_limit(col : pd.core.series.Series) -> float:
    """ 
    Calcula o limite superior para identificar outliers com base no intervalo interquartil.
    O cálculo utiliza o primeiro (Q1) e o terceiro quartil (Q3) para determinar a distância interquartil (IQR).
    O limite superior é calculado como Q3 + 1,5 * IQR, destacando os valores que estão acima desse limite.

        :param col: Série de valores numéricos (como preços) sobre os quais será calculado o limite.
        :return: Valor do limite superior, acima do qual os valores são considerados outliers.
    """
    q1 = col.quantile(0.25)
    q3 = col.quantile(0.75)
    return q3 + 1.5 * (q3 - q1)

#Abrindo as tabelas que serão utilizadas
appearances = pd.read_csv('../data/appearances.csv')
player_valuations = pd.read_csv('../data/player_valuations.csv')

#Limpando dados NaN das colunas que serão utilizadas
appearances.dropna(axis=0, subset=["yellow_cards", "red_cards", "goals", "assists"], inplace=True) 
player_valuations.dropna(axis=0, subset=["market_value_in_eur", "date"], inplace=True)

print(player_valuations)

#Criando mean_price
#Ordenar os dados, converter data, corrigir valores, criar colunas same_player e date_diff, calcular a média ponderada
player_valuations.sort_values(['player_id', 'date'], ascending=True, inplace=True)
player_valuations["date"] = pd.to_datetime(player_valuations["date"], yearfirst=True)
player_valuations['market_value_in_eur'] = player_valuations.apply(lambda row: inflation.inflation_adj(row['market_value_in_eur'], row['date']), axis=1)

print(player_valuations)

player_valuations["same_player"] = -player_valuations["player_id"].diff(-1) == 0
player_valuations["date_diff"] = -player_valuations["date"].diff(-1)
player_valuations["date_diff"] = player_valuations.apply(correct_data_diff, axis=1)
mean_price = player_valuations.groupby("player_id").apply(calc_mean_price).reset_index(name="mean_price")

print(mean_price)

#Criando performance
#Ordenar os dados, calcular performance do jogador
appearances.sort_values('player_id', ascending=True, inplace=True)
performance = appearances.groupby(["player_id", "player_name"]).apply(calc_performance).reset_index(name="performance")

print(performance)

#Unindo os dados
merged = pd.merge(performance, mean_price, how="left", on="player_id").dropna(axis=0).sort_values("mean_price", ascending=True)

#Calculando limite superior
merged["log_mean_price"] = np.log(merged["mean_price"])
upper_limit = calc_upper_limit(merged["mean_price"])
performance_upper = merged[merged["mean_price"] >= upper_limit]

print("oi5")
print(performance_upper)

#Plotando os gráficos
print(performance_upper.describe())
print(np.corrcoef(performance_upper["performance"], performance_upper["mean_price"])[0,1])
sns.scatterplot(data=performance_upper, x="log_mean_price", y="performance", color="red")
plt.show()