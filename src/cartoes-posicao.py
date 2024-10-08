import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme(style="ticks", palette="pastel")

game_events = pd.read_csv('data/game_events.csv')
players = pd.read_csv('data/players.csv')

game_events = game_events.loc[game_events["type"] == "Cards"]

game_events["card_type"] = game_events["description"].map(lambda e: "yellow" if "yellow" in e.lower() else "red")
card_positions = pd.merge(game_events, players, on="player_id", how="left")

print(card_positions.groupby(["card_type", "position"].size().reset_index(name="count")))

#sns.barplot(x=card_positions["position"], y=card_positions["card_type"])
#plt.show()