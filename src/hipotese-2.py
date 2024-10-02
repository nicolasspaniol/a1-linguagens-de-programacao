import pandas as pd

"""
Quais foram as compras de jogadores com melhores e 
piores custo-benefício registradas?
"""

def open_csv(arquivo):
    with open('data/'+arquivo+'.csv', 'r', encoding='latin1') as file:
        return pd.read_csv(file)
    
#Tabelas a serem utilizadas

appearances = open_csv("appearances")
game_events = open_csv("game_events")
player_valuations = open_csv("player_valuations")
players = open_csv("players")
transfers = open_csv("transfers")



#Em transfers, ordenar pelo valor
#Proxy para determinar se o jogar é bom: appearances, game_events
