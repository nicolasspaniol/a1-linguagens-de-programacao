""" Módulo para calcular medidas resumo e de associações dos dados """

import pandas as pd
import numpy as np
import math


def chi2(df: pd.DataFrame):
    """ Calcula a medida Qui^2 dos dados contidos no DataFrame. O Qui^2
        corresponde à soma da seguinte equação aplicada a cada dado no conjunto:
        `(o-e)^2 / e`, onde `o` é o valor observado e `e`, o esperado para
        a linha e a coluna consideradas.
        
        :param df: um DataFrame onde todos os dados representam frequências
        absolutas das linhas com as colunas
        :return: o Qui^2 do DataFrame
    """

    if df.shape[0] < 2 or df.shape[1] < 2:
        raise ValueError("O DataFrame deve ter pelo menos duas linhas e duas colunas")

    if not df.dtypes.apply(lambda dtype: np.issubdtype(dtype, np.number)).all():
        raise ValueError("Todos os dados devem ser numéricos (numpy.number)")
    
    sum_y = df.sum(axis=1)
    sum_x = df.sum(axis=0)
    total = sum_x.sum()
    exp = (np.array(sum_y).reshape(-1, 1) @ np.array(sum_x).reshape(1, -1)) / total
    return (np.square(df - exp) / exp).sum().sum()


def cramer_v(df: pd.DataFrame):
    """ Calcula o V de Cramer dos dados contidos no DataFrame,
        que indica o quão associadas estão as variáveis que representam as
        colunas e as linhas da tabela, retornando um valor entre 0 (nenhuma
        associação) e 1 (associação máxima).
        
        :param df: um DataFrame onde todos os dados representam frequências
        absolutas das linhas com as colunas
        :return: o V de Cramer das variáveis
    """
    k = min(df.shape) - 1
    df_chi2 = chi2(df)
    total = df.sum().sum()
    return math.sqrt(df_chi2 / total / k)


def contingency_coeff(df: pd.DataFrame):
    """ Calcula o coeficiente de contingência dos dados contidos no DataFrame,
        que indica o quão associadas estão as variáveis que representam as
        colunas e as linhas da tabela.

        :param df: um DataFrame onde todos os dados representam frequências
        absolutas das linhas com as colunas
        :return: o coeficiente de contingência das variáveis
    """
    df_chi2 = chi2(df)
    total = df.sum().sum()
    return math.sqrt(df_chi2 / (df_chi2 + total))
