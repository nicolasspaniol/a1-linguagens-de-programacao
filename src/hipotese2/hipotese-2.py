from datetime import date, datetime
import pandas as pd
import os
"""
Quais foram as compras de jogadores com melhores e 
piores custo-benefício registradas?
"""

PATH = '../data/cost_benefit.csv'

def create():
    #Criação do arquivo CSV, caso ainda não criado
    #if not os.path.exists(PATH):
        cost_benefit = pd.DataFrame({
            "player_id": [],
            "club_id": [],
            "cost_benefit": []
        })
        cost_benefit.to_csv(PATH, index=False)
        return

def add(player_id, club_id, cb):
    #Inserção de cada transferência ao CSV
    cost_benefit = pd.DataFrame({
            "player_id": [player_id],
            "club_id": [club_id],
            "cost_benefit": [cb]             
    })
    cost_benefit.to_csv(PATH, mode='a', header=False, index=False)
    return

def open_csv(arquivo):
    with open('data/'+arquivo+'.csv', 'r', encoding='latin1') as file:
        return pd.read_csv(file)

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

#Em transfers, ordenar pelo valor
#Proxy para determinar se o jogar é bom: appearances, game_events
