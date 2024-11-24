"""
Módulo de Análise de Desempenho e Preço de Jogadores.
Este módulo analisa a relação entre o valor de mercado fora do comum de jogadores e seu 
desempenho em campo, determinando se os jogadores com preços inflacionados têm um desempenho 
proporcional aos demais.

Funções criadas:
1º - Abertura dos arquivos CSV
2º - Cálculo da média ponderada do valor de cada jogador
3º - Cálculo do desempenho dos jogadores
4º - Identificação dos outliers (jogadores com preço acima do limite superior)
5º - Geração dos gráficos de correlação entre preço e desempenho
"""

from datetime import date, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import inflation

"""
Jogadores com preço fora do comum tem o desempenho proporcional?
"""

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
appearances = pd.read_csv('data/appearances.csv')
player_valuations = pd.read_csv('data/player_valuations.csv')

#Limpando dados NaN das colunas que serão utilizadas
appearances.dropna(axis=0, subset=["yellow_cards", "red_cards", "goals", "assists"], inplace=True) 
player_valuations.dropna(axis=0, subset=["market_value_in_eur", "date"], inplace=True)

#Criando mean_price
#Ordenar os dados, converter data, corrigir valores, criar colunas same_player e date_diff, calcular a média ponderada
player_valuations.sort_values(['player_id', 'date'], ascending=True, inplace=True)
player_valuations["date"] = pd.to_datetime(player_valuations["date"], yearfirst=True)
player_valuations['market_value_in_eur'] = player_valuations.apply(lambda row: inflation.inflation_adj(row['market_value_in_eur'], row['date']), axis=1)
player_valuations["same_player"] = -player_valuations["player_id"].diff(-1) == 0
player_valuations["date_diff"] = -player_valuations["date"].diff(-1)
player_valuations["date_diff"] = player_valuations.apply(correct_data_diff, axis=1)
mean_price = player_valuations.groupby("player_id").apply(calc_mean_price).reset_index(name="Preco_Medio")

#Criando performance
#Ordenar os dados, calcular performance do jogador
appearances.sort_values('player_id', ascending=True, inplace=True)
performance = appearances.groupby(["player_id", "player_name"]).apply(calc_performance).reset_index(name="Desempenho")

#Unindo os dados
merged = pd.merge(performance, mean_price, how="left", on="player_id").dropna(axis=0).sort_values("Preco_Medio", ascending=True)

#Calculando limite superior
merged["Log_Preco_Medio"] = np.log(merged["Preco_Medio"])
upper_limit = np.log(calc_upper_limit(merged["Preco_Medio"]))

df = pd.DataFrame({
        "Log_Preco_Medio_do_jogador": [],
        "Quartil_1": [],
        "Media_do_desempenho_dos_jogadores_nesse_intervalo": [],
        "Quartil_3": []
        
    })

for i in range(-6, 4):
    inf = upper_limit + i
    sup = upper_limit + i + 1
    intervalo = merged[(merged["Log_Preco_Medio"] >= inf) & (merged["Log_Preco_Medio"] < sup)]
    q1 = intervalo["Desempenho"].quantile(0.25)
    q2 = intervalo["Desempenho"].quantile(0.5)
    q3 = intervalo["Desempenho"].quantile(0.75)
    df.loc[i+6] = [(sup+inf)/2, q1, q2, q3]
    print(inf, sup, q1, q2, q3)

df.to_csv("performance.csv")

#Plotando os gráficos
# print(merged.describe())
# print("Correlação: ", np.corrcoef(merged["Desempenho"], merged["Preco_Medio"])[0,1])
# sns.lineplot(data=df, x="Intervalo", y="Média", color="blue")
# plt.show()
