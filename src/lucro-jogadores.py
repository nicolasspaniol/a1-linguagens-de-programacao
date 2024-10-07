import pandas as pd
from datetime import date, datetime
import locale
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


sns.set_theme(style="ticks", palette="pastel")
locale.setlocale(locale.LC_ALL, '')

players = pd.read_csv('data/players.csv')
transfers = pd.read_csv('data/transfers.csv')

# filtra o dataset, removendo transferências sem valor definido
transfers = transfers.loc[transfers['transfer_fee'] > 0].sort_values(['player_id', 'transfer_date'])


def parse_date(date_str: str) -> date:
    if len(date_str) > 10:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()
       
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def find_age(current_date: date, id: int):
    player = players.loc[players['player_id'] == id].iloc[0]
    if type(player['date_of_birth']) != str:
        return None

    birth = datetime.strptime(player['date_of_birth'], '%Y-%m-%d %H:%M:%S').date()
    return (current_date - birth).days / 365


# Para a hipótese atual, considerei como buyback a sequência dos eventos de
# venda e compra, nessa ordem, de um mesmo jogador por parte de um mesmo time
buybacks_list = []
current_player_id = 0
possible_buybacks = []
for _, row in transfers.iterrows():
    id = row['player_id']

    # se o ID do jogador mudou, desconsidera os buybacks pendentes
    if (current_player_id != id):
        possible_buybacks = []
    current_player_id = id

    for bb in possible_buybacks:
        if bb['club_id'] != row['to_club_id']: continue

        dt = parse_date(row['transfer_date'])
        bb['fee_bought'] = row['transfer_fee']
        bb['age_bought'] = find_age(dt, id)
        buybacks_list.append(bb)

    dt = parse_date(row['transfer_date'])
    age_sold = find_age(dt, id)
    # supomos que o jogador será comprado pelo time posteriormente e já
    # preenchemos as informações do buyback com o que temos
    bb = {
        'player_id': id,
        'club_id': row['from_club_id'],
        'fee_sold': row['transfer_fee'],
        'age_sold': age_sold
    }
    possible_buybacks.append(bb)


buybacks = pd.DataFrame(buybacks_list)
buybacks['balance'] = buybacks['fee_sold'] - buybacks['fee_bought']
buybacks['interval'] = buybacks['age_bought'] - buybacks['age_sold']

print(buybacks)
print(f'n: {len(buybacks)}')

print(f'saldo (mediana): {locale.currency(buybacks['balance'].median(), grouping=True)}')
print(f'saldo (desvio padrão): {locale.currency(buybacks['balance'].std(), grouping=True)}')
print(f'intervalo (média): {round(buybacks['interval'].mean(), 1)}')
print(f'idade de venda (média): {round(buybacks['age_sold'].mean(), 1)}')
print(f'idade de compra (média): {round(buybacks['age_bought'].mean(), 1)}')

# sns.boxplot(x=buybacks['balance'])
sns.boxplot(x=buybacks['interval'])
plt.show()
