from datetime import date, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

"""
Quais foram as compras de jogadores com melhores e 
piores custo-benefício registradas?
"""

PATH = '../data/cost_benefit2.csv'

def create():
    #Criação do arquivo CSV, caso ainda não criado
    #if not os.path.exists(PATH):
        cost_benefit = pd.DataFrame({
            "player_id": [],
            "from_club_id": [],
            "to_club_id": [],
            "date": [],
            "cost_benefit": []
        })
        cost_benefit.to_csv(PATH, index=False)
        return

def add(player_id, from_club_id, to_club_id, date, cb):
    #Inserção de cada transferência ao CSV
    cost_benefit = pd.DataFrame({
            "player_id": [player_id],
            "from_club_id": [from_club_id],
            "to_club_id": [to_club_id],
            "date": [date],
            "cost_benefit": [cb]             
    })
    cost_benefit.to_csv(PATH, mode='a', header=False, index=False)
    return

def open_csv(arquivo):
    with open('data/'+arquivo+'.csv', 'r', encoding='latin1') as file:
        return pd.read_csv(file)

def get_parameters(start_price, final_price, start_date, final_date, appearances_player):
    data_parameters = {
        "games_played": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        "goals": 0,
        "assists": 0,
        "start_price": start_price,
        "final_price": final_price}
    
    for _, each_row_appearances_player in appearances_player.iterrows():
        game_date = parse_date(each_row_appearances_player["date"])
        if start_date <= game_date and game_date <= final_date:
            data_parameters["games_played"] += 1
            data_parameters["yellow_cards"] += each_row_appearances_player["yellow_cards"]
            data_parameters["red_cards"] += each_row_appearances_player["red_cards"]
            data_parameters["goals"] += each_row_appearances_player["goals"]
            data_parameters["assists"] += each_row_appearances_player["assists"]
    return data_parameters

def proxy(games_played, yellow_cards, red_cards, goals, assists, start_price, final_price):
    delta_price = final_price - start_price
    modificador = 10 ** (len(str(delta_price))-1)

    #Fórmula para calcular desempenho do jogador, segundo sites esportivos (contem modificacao)
    reduce = ( (-1)*yellow_cards + (-3)*red_cards + (8)*goals + (5)*assists ) * modificador / games_played
    return round((reduce + delta_price) / start_price, 4)
    
def parse_date(date_str: str) -> date:
    if len(date_str) > 10:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()
    return datetime.strptime(date_str, '%Y-%m-%d').date()

#Tabelas a serem utilizadas
appearances = open_csv("appearances")
game_events = open_csv("game_events")
player_valuations = open_csv("player_valuations")
players = open_csv("players")
transfers = open_csv("transfers")

appearances.dropna(axis=0, inplace=True) 
game_events.dropna(axis=0, inplace=True)
player_valuations.dropna(axis=0, inplace=True)
players.dropna(axis=0, subset=["market_value_in_eur"], inplace=True)
transfers.dropna(axis=0, subset=["market_value_in_eur"], inplace=True)

create()
#Para cada jogador catalogado em "players"
for player_id in players['player_id']:
    transfers_player = transfers.loc[transfers['player_id'] == player_id]
    #Se esse jogador tiver transferências em "transfers"
    if not transfers_player.empty:
        transfers_player.sort_values(by='transfer_date', ascending=True, inplace=True)
        transfers_player.reset_index(drop=True, inplace=True)
        #Para cada transferência referente a esse jogador
        for index, each_row_transfers_player in transfers_player.iterrows():
            start_date = parse_date(each_row_transfers_player['transfer_date'])
            from_club_id = each_row_transfers_player['from_club_id']
            to_club_id = each_row_transfers_player['to_club_id']
            start_price = each_row_transfers_player['market_value_in_eur']
            if index < len(transfers_player) - 1:
                final_date = parse_date(transfers_player.loc[index+1,'transfer_date'])
                final_price = transfers_player.loc[index+1,'market_value_in_eur']
            else:
                final_date = datetime.now().date()
                final_price = players.loc[players['player_id'] == player_id, 'market_value_in_eur'].values[0]
            
            #Para cada jogo entre as datas da transfência atual e a próxima
            appearances_player = appearances.loc[appearances['player_id'] == player_id]
            data_parameters = get_parameters(start_price, final_price, start_date, final_date, appearances_player)
            if data_parameters["games_played"] != 0:
                add(player_id, from_club_id, to_club_id, start_date, proxy(**data_parameters))

cost_benefit = open_csv("cost_benefit")
cost_benefit.sort_values(by='cost_benefit', ascending=True, inplace=True)
cost_benefit.describe()

sns.boxplot(data=cost_benefit, y="cost_benefit")
plt.ylim(-200, 200)
plt.show()