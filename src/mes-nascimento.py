import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime

sns.set_theme(style="ticks", palette="pastel")

players = pd.read_csv('data/players.csv')
players["date_of_birth"] = pd.to_datetime(players["date_of_birth"])


def extract_month_of_birth(row):
    """ Extrai o mês da data de nascimento do jogador,
        aplicando a função parse_date() e retirando o mês da data obtida

        :param row: linha da tabela
        :return: mês do nascimento de 1.0 a 12.0
    """
    birth_date = row["date_of_birth"]
    if type(birth_date) == str:
        return birth_date.month
    return None


# Cria uma nova coluna na tabela com o mês do aniversário de cada jogador
players["month_of_birth"] = players.apply(extract_month_of_birth,axis=1)

# Cria uma tabela com a quantidade de aniversariantes por mês
month_frequency = players.groupby(["month_of_birth"]).size().reset_index(name="count")

# Adiciona uma coluna com a proporção de aniversariantes por mês
quantity_players = month_frequency["count"].sum()
month_frequency["frequency"] = month_frequency["count"]/quantity_players

sns.barplot(month_frequency, x="month_of_birth", y="frequency")
plt.show()

# Calcula o desvio padrão da distribuição da quantidade de jugadores por mês
dp = month_frequency["count"].std()
print(f"Desvio padrão de aniversariantes por mês: {dp}")

