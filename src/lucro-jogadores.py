import pandas as pd
from datetime import date, datetime
import locale
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def parse_date(date_str: str) -> date:
    """ Converte uma string representando uma data para um objeto
        `datetime.date`. As datas devem estar formatadas como
        `YYYY-mm-dd HH:MM:SS` ou `YYYY-mm-dd`.

        :param date_str: a string com a data em um dos formatos esperados
        :return: a data como um objeto `datetime.date`
    """
    if len(date_str) > 10:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
       
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def find_age(current_date: date, id: int) -> float:
    """ Encontra a idade de um jogador de ID `id` no momento `current_date`, a
        partir das informações do jogador contidas no arquivo `players.csv`.

        :param current_date: data com base na qual a idade será calculada
        :param id: ID do jogador
        :return: a idade do jogador no momento informado, em anos
    """
    p = players.loc[players["player_id"] == id].iloc[0]
    if type(p["date_of_birth"]) != str:
        return None

    birth = datetime.strptime(p["date_of_birth"], "%Y-%m-%d %H:%M:%S").date()
    return (current_date - birth).days / 365


# Configurações
sns.set_theme(style="ticks", palette="pastel")
locale.setlocale(locale.LC_ALL, "")

players = pd.read_csv("data/players.csv")
transfers = pd.read_csv("data/transfers.csv")

# Filtra o dataset, removendo transferências sem valor reportado, e ordena
transfers = transfers.loc[transfers["transfer_fee"] > 0]
transfers = transfers.sort_values(["player_id", "transfer_date"])

# Para a hipótese atual, consideramos como buyback a sequência dos eventos de
# venda e compra, nessa ordem, de um mesmo jogador por parte de um mesmo time
buybacks_list = []
current_player_id = -1
possible_buybacks = []
for _, row in transfers.iterrows():
    id = row["player_id"]

    # Se o ID do jogador mudou, desconsidera os buybacks pendentes
    if (current_player_id != id):
        possible_buybacks = []
    current_player_id = id

    # Aqui verificamos se o jogador foi anteriormente vendido pelo time que
    # está comprando-o na transferência atual
    for bb in possible_buybacks:
        if bb["club_id"] != row["to_club_id"]: continue

        # Adiciona o buyback para ser analisado posteriormente
        dt = parse_date(row["transfer_date"])
        bb["fee_bought"] = row["transfer_fee"]
        bb["age_bought"] = find_age(dt, id)
        buybacks_list.append(bb)

    dt = parse_date(row["transfer_date"])
    age_sold = find_age(dt, id)

    # Supomos que o jogador será comprado pelo time posteriormente e já
    # preenchemos as informações do buyback com o que temos
    bb = {
        "player_id": id,
        "club_id": row["from_club_id"],
        "fee_sold": row["transfer_fee"],
        "age_sold": age_sold
    }
    possible_buybacks.append(bb)

buybacks = pd.DataFrame(buybacks_list)
buybacks["balance"] = buybacks["fee_sold"] - buybacks["fee_bought"]
buybacks['sqrt_balance'] = np.sign(buybacks['balance']) * np.sqrt(np.abs(buybacks['balance']))
buybacks["interval"] = buybacks["age_bought"] - buybacks["age_sold"]

# ------------------------------------------------------------------------------

print(f"n: {len(buybacks)}")
print(f"saldo (mediana): {locale.currency(buybacks["balance"].median(), grouping=True)}")
print(f"saldo (desvio padrão): {locale.currency(buybacks["balance"].std(), grouping=True)}")
print(f"intervalo (média): {round(buybacks["interval"].mean(), 1)}")
print(f"idade de venda (média): {round(buybacks["age_sold"].mean(), 1)}")
print(f"idade de compra (média): {round(buybacks["age_bought"].mean(), 1)}")

sns.boxplot(y=buybacks["sqrt_balance"])
plt.show()

sns.boxplot(y=buybacks["balance"])
plt.show()

sns.boxplot(y=buybacks["interval"])
plt.show()
