from datetime import date, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

"""
Quais foram as compras de jogadores com melhores e 
piores custo-benefício registradas?
"""

def add_h2(path, player_id, from_club_id, to_club_id, date, cb):
    #Inserção de cada transferência ao CSV
    cost_benefit = pd.DataFrame({
            "player_id": [player_id],
            "from_club_id": [from_club_id],
            "to_club_id": [to_club_id],
            "date": [date],
            "cost_benefit": [cb]             
    })
    cost_benefit.to_csv(path, mode='a', header=False, index=False)
    return

def add_h5(path, player_id, mean_price, performance):
    #Inserção de cada transferência ao CSV
    cost_benefit = pd.DataFrame({
            "player_id": [player_id],
            "mean_price": [mean_price],
            "performance": [performance]             
    })
    cost_benefit.to_csv(path, mode='a', header=False, index=False)
    return

def open_csv(arquivo):
    with open('../data/'+arquivo+'.csv', 'r', encoding='latin1') as file:
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

def update_parameters(data_parameters_total, data_parameters):
    data_parameters_total["games_played"] += data_parameters["games_played"]
    data_parameters_total["yellow_cards"] += data_parameters["yellow_cards"]
    data_parameters_total["red_cards"] += data_parameters["red_cards"]
    data_parameters_total["goals"] += data_parameters["goals"]
    data_parameters_total["assists"] += data_parameters["assists"]
    return data_parameters_total

def proxy(games_played, yellow_cards, red_cards, goals, assists, start_price, final_price):
    delta_price = final_price - start_price
    modificador = 10 ** (len(str(delta_price))-1)

    #Fórmula para calcular desempenho do jogador, segundo sites esportivos (contem modificacao)
    reduce = ( (-1)*yellow_cards + (-3)*red_cards + (8)*goals + (5)*assists ) * modificador / games_played
    return round((reduce + delta_price) / start_price, 4)

def proxy2(games_played, yellow_cards, red_cards, goals, assists):
    reduce = ( (-1)*yellow_cards + (-3)*red_cards + (8)*goals + (5)*assists ) * 100 / games_played
    return reduce
    
def calc_mean_price(player_valuations):
    player_valuations.reset_index(drop=True, inplace=True)
    total_days = 0
    total_market_value = 0
    for index, each_row_player_valuations in player_valuations.iterrows():
        market_value = each_row_player_valuations['market_value_in_eur']
        start_date = parse_date(each_row_player_valuations['date'])
        if index < len(player_valuations) - 1:
            final_date = parse_date(player_valuations.loc[index+1,'date'])
        else:
            final_date = datetime.now().date()
        diferenca = final_date - start_date
        days = diferenca.days
        total_days += days
        total_market_value += market_value * days
    return total_market_value / total_days

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
cost_benefit = pd.DataFrame({
        "player_id": [],
        "from_club_id": [],
        "to_club_id": [],
        "date": [],
        "cost_benefit": []
    })
performance = pd.DataFrame({
        "player_id": [],
        "mean_price": [],
        "performance": []
    })

#Limpar as tabelas utilizadas
appearances.dropna(axis=0, inplace=True) 
game_events.dropna(axis=0, inplace=True)
player_valuations.dropna(axis=0, inplace=True)
players.dropna(axis=0, subset=["market_value_in_eur"], inplace=True)
transfers.dropna(axis=0, subset=["market_value_in_eur"], inplace=True)




player_valuations.sort_values(['player_id', 'date'], ascending=True, inplace=True)
player_valuations["date"].diff()


players["mean_price"] = calc_mean_price(player_valuations)

appearances.sort_values('player_id', ascending=True, inplace=True)
players["performance"] = proxy2(appearances)

#Para cada jogador catalogado em "players"
for player_id in players['player_id']:
    transfers_player = transfers.loc[transfers['player_id'] == player_id]
    #Se esse jogador tiver transferências em "transfers"
    if not transfers_player.empty:
        transfers_player.sort_values(by='transfer_date', ascending=True, inplace=True)
        transfers_player.reset_index(drop=True, inplace=True)
        data_parameters_total = {
            "games_played": 0,
            "yellow_cards": 0,
            "red_cards": 0,
            "goals": 0,
            "assists": 0}
        mean_price = calc_mean_price(player_valuations.loc[player_valuations['player_id'] == player_id])
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
            data_parameters_total = update_parameters(data_parameters_total, data_parameters)
            if data_parameters["games_played"] != 0:
                add_h2('../data/cost_benefit2.csv', player_id, from_club_id, to_club_id, start_date, proxy(**data_parameters))
        if data_parameters_total["games_played"] != 0:
            add_h5('../data/performance.csv', player_id, mean_price, proxy2(**data_parameters_total))




