from datetime import date, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

"""
Quais foram as compras de jogadores com melhores e 
piores custo-benefício registradas?
"""

#Função para abrir arquivos csv
def open_csv(arquivo):
    with open('../data/'+arquivo+'.csv', 'r', encoding='latin1') as file:
        return pd.read_csv(file)

#Função para calcular custo-beneficio
def calc_cost_benefit(group):
    delta_price = (group["market_value_in_eur_shift"].iloc[0] - group["market_value_in_eur"].iloc[0])
    modificador = 10 ** (len(str(delta_price))-1)
    #Fórmula para calcular desempenho do jogador, segundo sites esportivos (contem modificacao)
    if group.shape[0] != 0:
        reduce = sum((-1)*group["yellow_cards"] + (-3)*group["red_cards"] + (8)*group["goals"] + (5)*group["assists"]) * modificador / group.shape[0]
        if group["market_value_in_eur"].iloc[0] != 0:
            return round((reduce + delta_price) / group["market_value_in_eur"].iloc[0], 4)
    return None
    
#Função correção da data_diff
def correct_data_shift(row):
    if not row["same_player"]:
        return datetime.now().date()
    return row["date_shift"].date()

#Função correção da market_value_in_eur_shift
def correct_market_value_in_eur_shift(row):
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
merged[["player_id", "transfer_date", "date", "date_shift", "market_value_in_eur","market_value_in_eur_shift", "yellow_cards", "red_cards", "goals", "assists"]].head(50)


cost_benefit = merged.groupby(['player_id', 'transfer_date']).apply(calc_cost_benefit).reset_index(name="cost_benefit")

#Plotando o gráfico
print(cost_benefit[["cost_benefit"]].describe())
sns.boxplot(data=cost_benefit,  y="cost_benefit", color="red")
plt.show()

