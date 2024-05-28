import pandas as pd

df = pd.read_csv('routes2.csv')
print(df)
df.drop_duplicates()
print(df)
# print(df)

# df.to_csv('airlines_final.csv')
