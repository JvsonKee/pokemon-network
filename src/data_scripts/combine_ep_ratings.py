import pandas as pd

ratings_df = pd.read_csv("../../datasets/clean/ratings.csv")
episodes_df = pd.read_csv("../../datasets/clean/episodes.csv")

merged_df = episodes_df.merge(ratings_df, on=["season", "episode"], how="left")

merged_df.to_csv("../../datasets/clean/episode_nodes.csv", index=False)
