import pandas as pd

df = pd.read_csv('airports-code.csv', delimiter=";")
print(df.columns)

df.drop(['City Name geo_name_id', 'Country Name geo_name_id', 'World Area Code'], axis=1, inplace=True)
print(df)
df.to_csv('airports-code2.csv')

print(df)
print(df.duplicated(['Airport Code']).sum())
input()
df.drop_duplicates(subset=['Airport Name', 'City Name'], keep='first', inplace=True)
print(df)