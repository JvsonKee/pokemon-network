import pandas as pd

df = pd.read_csv(
    '../../datasets/raw/pokemon.csv', 
    usecols=['id', 'name', 'generation']
)

# remove last 119 pokemon paldea region
df = df.iloc[:-120]

# create node_type column
df['node_type'] = 'pokemon'

# capatalize the first letter of the pokemon name
df['name'] = df['name'].str.capitalize()

# renaming columns for gephi
df = df.rename(columns={ 'id': 'Id', 'name': 'Label' })

# export to csv file
df.to_csv("../../datasets/clean/pokemon_nodes.csv", index=False)
