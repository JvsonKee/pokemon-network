import pandas as pd
import itertools

df = pd.read_csv(
    '../../datasets/raw/single-types.csv'
)

# extract the types into a set
types = set(df.columns.tolist()[1:])

# create a set for all possible dual types
dual_types = set(
    [f"{min(type1, type2)}-{max(type1, type2)}" for type1, type2 in itertools.combinations(types, 2)]
)

for tp in dual_types:
    print(tp)