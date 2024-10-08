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

def extract_month_of_birth(r):
    birth_date = r["date_of_birth"]
    if type(birth_date) == str:
        return parse_date(birth_date).month
    return None

players["month_of_birth"] = players.apply(extract_month_of_birth,axis=1)

month_frequency = players.groupby(["month_of_birth"]).size().reset_index(name="count")

sns.barplot(month_frequency, x="month_of_birth", y="count")
plt.show()