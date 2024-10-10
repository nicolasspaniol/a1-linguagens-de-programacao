import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime

sns.set_theme(style="ticks", palette="pastel")

players = pd.read_csv('data/players.csv')


def parse_date(date_str: str) -> date:
    if len(date_str) > 10:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').date()
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def extract_month_of_birth(row):
    """ Extrai o mês da data de nascimento do jogador,
        aplicando a função parse_date() e retirando o mês da data obtida

        :param row: linha da tabela
        :return: mês do nascimento de 1.0 a 12.0
    """
    birth_date = row["date_of_birth"]
    if type(birth_date) == str:
        return parse_date(birth_date).month
    return None


# Cria uma nova coluna na tabela com o mês do aniversário de cada jogador
players["month_of_birth"] = players.apply(extract_month_of_birth,axis=1)

# Cria uma tabela com a frequência de aniversariantes por mês
month_frequency = players.groupby(["month_of_birth"]).size().reset_index(name="count")


def chi2(series: pd.Series):
    """ Calcula o Qui^2 de uma série de valores, tomando como valor esperado a média.

        :param series: lista de números
        :return: o Qui^2 calculado
    """
    expected = series.mean()
    return (np.square(series - expected) / expected).sum()
    

sns.barplot(month_frequency, x="month_of_birth", y="count")
plt.show()

# Calcula o Qui^2 da distribuição da quantidade de jugadores por mês
chi2_count = chi2(month_frequency["count"])
n = month_frequency["count"].sum()
C = (chi2_count/(chi2_count + n)) ** .5
print(f"Coeficiente de contingência: {C}")