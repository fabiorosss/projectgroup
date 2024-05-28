import pandas as pd


df = pd.read_csv('airlines.csv')
print(df.columns)

df.drop(['Alias', 'IATA', 'ICAO', 'Callsign', 'Active'], axis=1, inplace=True)
print(df)

df.drop_duplicates(subset=['Name', 'Country'], keep="first", inplace=True)
df.drop(columns=['C','Airline ID'], axis=1, inplace=True)
print(df)
print(df.columns)
df.drop(index=0, inplace=True)
print(df)
df.to_csv('airlines_final.csv')