import pandas as pd
from datetime import date, datetime

players = pd.read_csv("data/players.csv")
transfers = pd.read_csv("data/transfers.csv")


def parse_date(date_str: str) -> date:
    if len(date_str) > 10:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()
       
    return datetime.strptime(date_str, '%Y-%m-%d').date()


# Para a hipótese atual, considerei como buyback a sequência dos eventos de
# venda e compra, nessa ordem, de um mesmo jogador por parte de um mesmo time
class Buyback:
    def __init__(self, player_id, club_id, fee_sale, fee_purchase, age_sale, age_purchase):
        self.player_id = player_id
        self.club_id = club_id
        self.fee_sale = fee_sale
        self.fee_purchase = fee_purchase
        self.age_sale = age_sale
        self.age_purchase = age_purchase


# filtrei o dataset
transfers = transfers.loc[transfers['transfer_fee'] > 0].sort_values(['player_id', 'transfer_date'])


def find_age(current_date: date, id: int):
    player = players.loc[players['player_id'] == id].iloc[0]
    if type(player['date_of_birth']) != str:
        return None

    birth = datetime.strptime(player['date_of_birth'], '%Y-%m-%d %H:%M:%S').date()
    return (current_date - birth).days / 365


buybacks = []
current_player_id = 0
possible_buybacks = []
for _, row in transfers.iterrows():
    id = row['player_id']

    # se o ID do jogador mudou, desconsidera os buybacks pendentes
    if (current_player_id != id):
        possible_buybacks = []
    current_player_id = id

    for bb in possible_buybacks:
        if bb.club_id != row['to_club_id']: continue

        dt = parse_date(row['transfer_date'])
        bb.fee_purchase = row['transfer_fee']
        bb.age_purchase = find_age(dt, id)
        buybacks.append(bb)

    dt = parse_date(row['transfer_date'])
    age_sold = find_age(dt, id)
    # supomos que o jogador será comprado pelo time posteriormente e já
    # preenchemos as informações do buyback com o que temos
    bb = Buyback(id, row['from_club_id'], row['transfer_fee'], None, age_sold, None)
    possible_buybacks.append(bb)


print(f"lucro médio = {sum(map(lambda e: e.fee_sale - e.fee_purchase, buybacks)) / len(buybacks)}")
print(f"intervalo médio = {sum(map(lambda e: e.age_purchase - e.age_sale, buybacks)) / len(buybacks)}")
print(f"idade média de venda = {sum(map(lambda e: e.age_sale, buybacks)) / len(buybacks)}")
print(f"idade média de compra = {sum(map(lambda e: e.age_purchase, buybacks)) / len(buybacks)}")
