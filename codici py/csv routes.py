import pandas as pd

df = pd.read_csv('routes.csv')
print(df.columns)

df.drop(['Codeshare', 'Equipment', 'Stops'], axis=1, inplace=True)
print(df)
df.to_csv('routes2.csv')