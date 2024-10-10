import pandas as pd
import numpy as np
import seaborn.objects as so


club_games = pd.read_csv("dataset/club_games.csv")
games = pd.read_csv("dataset/games.csv")

games_abroad = games.loc[games.competition_type == "international_cup"]
games_home_country = games.loc[games.competition_type != "international_cup"]

def calc_resultado(r):
    if r['home_club_goals'] > r['away_club_goals']:
        return 'derrota'
    if r['home_club_goals'] == r['away_club_goals']:
        return 'empate'
    if r['home_club_goals'] < r['away_club_goals']:
        return 'vitória'
    

games["resultado"] = games.apply(calc_resultado, axis=1)

games["is_international"] = games["competition_type"] == "international_cup"

fubá = games.groupby(["resultado", "is_international"]).size().reset_index(name="count")

print(fubá)

total_international = fubá.loc[fubá["is_international"]]["count"].sum()
total_home = fubá.loc[~fubá["is_international"]]["count"].sum()
fubá['count'] = np.where(fubá['is_international'] == True, fubá['count'] / total_international, fubá['count'] / total_home)

ax = so.Plot(fubá, x="is_international", y="count", color="resultado") \
    .add(so.Bar(), so.Stack())
ax.show()
