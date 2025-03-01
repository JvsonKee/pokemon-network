import pandas as pd

df = pd.read_csv(
    '../../datasets/raw/pokemon.csv', 
    usecols=['id', 'name', 'rank', 'evolves_from', 'type1', 'type2']
)

# remove last 119 pokemon paldea region
df = df.iloc[:-120]

# create dictionary mapping the name of the pokemon to their corresponding id
name_to_id = df.set_index('name')['id'].to_dict()

# replace the names in the "evolves_from" column with the corresponding id 
df["evolves_from"] = df["evolves_from"].map(name_to_id)

# replace missing values with -1 (pokemon that do not evolve from something)
df["evolves_from"] = df["evolves_from"].fillna(-1)

# covert to integers
df["evolves_from"] = df["evolves_from"].astype(int)

df = df.rename(columns={ 'id': 'Id', 'name': 'Label' })

# export to csv file
df.to_csv("../../datasets/clean/pokemon_nodes.csv", index=False)
