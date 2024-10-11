"""
Módulo de Análise de Custo-Benefício de Compras de Jogadores.
Este módulo processa e analisa dados de transferências de jogadores vindos de datasets 
retirados do site de futebol "https://www.transfermarkt.com.br/" , performances e valores 
de mercado para calcular o custo-benefício de contratações em termos de desempenho em 
campo e variação no valor de mercado.

Funções criadas:
1º - Abertura dos arquivos CSV
2º - Cálculo do custo-benefício dos jogadores
3º - Correção de datas e valores de mercado ajustados pela inflação
4º - Geração de gráficos para visualização dos resultados obtidos
"""

from datetime import date, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import inflation

"""
Hipótese 2: Quais foram as compras de jogadores com melhores e piores custo-benefício registradas?
"""

#Função para abrir arquivos csv
def open_csv(arquivo : str) -> pd.core.frame.DataFrame:
    """
    Abre um arquivo CSV na pasta '../data/' e carrega os dados em um DataFrame.

        :param arquivo: Nome do arquivo CSV (sem a extensão '.csv').
        :return: DataFrame contendo os dados do arquivo.
    """
    with open('../data/'+arquivo+'.csv', 'r', encoding='latin1') as file:
        return pd.read_csv(file)

#Função para calcular custo-beneficio
def calc_cost_benefit(group : pd.core.frame.DataFrame) -> float:
    """
    Calcula o custo-benefício de um jogador baseado em desempenho e valor de mercado.
    Considera estatísticas como gols, assistências, cartões, e a variação no valor de mercado ao longo do tempo.
    A fórmula utiliza pesos específicos para cada estatística, resultando em um valor numérico que reflete 
    se o jogador trouxe um bom retorno em relação ao investimento.

        :param group: DataFrame contendo as estatísticas e o valor de mercado do jogador.
        :return: Valor numérico que indica o custo-benefício do jogador.
    """
    delta_price = (group["market_value_in_eur_shift"].iloc[0] - group["market_value_in_eur"].iloc[0])
    modificador = 10 ** (len(str(delta_price))-1)
    #Fórmula para calcular desempenho do jogador, segundo sites esportivos (contem modificacao)
    reduce = sum((-1)*group["yellow_cards"] + (-3)*group["red_cards"] + (8)*group["goals"] + (5)*group["assists"]) * modificador / group.shape[0]
    return round((reduce + delta_price) / group["market_value_in_eur"].iloc[0], 4)
    
#Função correção da data_diff
def correct_data_shift(row : pd.core.series.Series) -> datetime.date:
    """
    Corrige a data da transferência do jogador, considerando se é o mesmo jogador.
    Se for o mesmo jogador, retorna a data da última transferência; caso contrário, retorna a data atual.

        :param row: Série contendo informações do jogador, incluindo se é o mesmo jogador e a data de transferência.
        :return: Data corrigida da transferência ou a data atual.
    """
    if not row["same_player"]:
        return datetime.now().date()
    return row["date_shift"].date()

#Função correção da market_value_in_eur_shift
def correct_market_value_in_eur_shift(row : pd.core.series.Series) -> float:
    """ 
    Corrige o valor de mercado de um jogador, levando em consideração a inflação e se é o mesmo jogador.
    Se for um jogador diferente, retorna o valor de mercado atual. Se for o mesmo jogador, retorna o valor de mercado 
    ajustado para o período anterior.

        :param row: Série com informações sobre o jogador, incluindo o valor de mercado e a indicação se é o mesmo jogador.
        :return: Valor de mercado corrigido com base na inflação ou o valor de mercado atual.
    """
    if not row["same_player"]:
        return row["current_market_value"]
    return row["market_value_in_eur_shift"]



#Abrindo as tabelas que serão utilizadas
appearances = open_csv("appearances")
players = open_csv("players")
transfers = open_csv("transfers")

#Limpando dados NaN das colunas que serão utilizadas
appearances.dropna(axis=0, subset=["yellow_cards", "red_cards", "goals", "assists"], inplace=True) 
transfers.dropna(axis=0, subset=["player_name", "transfer_date","market_value_in_eur", "from_club_id", "to_club_id"], inplace=True)
players.dropna(axis=0, subset=["name", "market_value_in_eur"], inplace=True)

#Criando coluna same_player
transfers.sort_values(['player_id', 'transfer_date'], ascending=True, inplace=True)
transfers["transfer_date"] = pd.to_datetime(transfers["transfer_date"], yearfirst=True)
transfers["same_player"] = -transfers["player_id"].diff(-1) == 0

#Criando coluna data_shift
transfers['date_shift'] = transfers['transfer_date'].shift(-1)
transfers["date_shift"] = transfers.apply(correct_data_shift, axis=1)

#Criando coluna market_value_in_eur_shift
transfers['market_value_in_eur'] = inflation.inflation_adj(transfers['market_value_in_eur'], transfers["transfer_date"])
transfers['market_value_in_eur_shift'] = transfers['market_value_in_eur'].shift(-1)
players.rename(columns={'market_value_in_eur': 'current_market_value'}, inplace=True)
transfers = pd.merge(players[["player_id", "current_market_value"]], transfers, on='player_id')
transfers["market_value_in_eur_shift"] = transfers.apply(correct_market_value_in_eur_shift, axis=1)

#Criando performance
appearances.sort_values(['player_id', 'date'], ascending=True, inplace=True)
appearances["date"] = pd.to_datetime(appearances["date"], yearfirst=True)

#Unindo as tabelas
merged = pd.merge(appearances, transfers, on='player_id')
merged = merged[(merged['date'] >= merged['transfer_date']) & (merged['date'] <= merged['date_shift'])]
merged.rename(columns={'player_name_x': 'player_name'}, inplace=True)

#Agrupar por transferência
cost_benefit = merged.groupby(['player_id', 'player_name', 'transfer_date', 'from_club_id', 'from_club_name', 'to_club_id', 'to_club_name']).apply(calc_cost_benefit).reset_index(name="cost_benefit")
cost_benefit.sort_values(by='cost_benefit', ascending=False, inplace=True)
cost_benefit

#Plotando o gráfico
print(cost_benefit[["cost_benefit"]].describe())
sns.boxplot(data=cost_benefit,  y="cost_benefit", color="red")
plt.show()

