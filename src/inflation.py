""" Módulo responsável por corrigir valores em Euro para a inflação """

import pandas as pd
from datetime import datetime
import math


def inflation_adj(value: float, period: datetime):
    """ Ajusta o valor monetário passado para a inflação atual (setembro de
        2024).
        
        :param value: o valor a ser corrigido
        :param period: um objeto `datetime` com o período em que o valor foi
        considerado
        :return: valor corrigido
    """

    if value < 0:
        raise ValueError("O parâmetro 'value' não pode ser negativo")

    if math.isnan(value):
        raise ValueError("O parâmetro 'value' não pode ser NaN")

    if period < datetime(1997, 1, 1):
        raise ValueError("O parâmetro 'period' deve representar uma data posterior a 1996")

    if period > datetime(2024, 9, 30):
        raise ValueError("O parâmetro 'period' deve representar uma data anterior a outubro de 2024")

    period_str = period.strftime("%Y-%m")
    now = df.loc[df["period"] == "2024-09"].iloc[0]["cum_inflation"]
    then = df.loc[df["period"] == period_str].iloc[0]["cum_inflation"]
    return round(value * now / then, 2)


# Fonte: https://data.ecb.europa.eu/data/datasets/ICP/ICP.M.U2.N.000000.4.ANR
df = pd.read_csv("data/hcpi/hcpi.csv")
df["date"] = pd.to_datetime(df["date"], yearfirst=True)
df["period"] = df["date"].dt.to_period("M").astype(str)

cum_inflation = []
index = 100
for i, r in df.iterrows():
    index *= 1 + r["inflation"] / 1200
    cum_inflation.append(index)

df["cum_inflation"] = pd.Series(cum_inflation)
