import csv
import pandas as pd

df = pd.read_csv('airlines.csv')
print(df.columns)

df.drop(['Alias', 'IATA', 'ICAO', 'Callsign', 'Active'], axis=1, inplace=True)
print(df)

df.to_csv('airlines2.csv')

#