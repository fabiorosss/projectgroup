import pandas as pd

df = pd.read_csv('csv_puliti/flight_data_database.csv')
df.drop_duplicates()
df2 = pd.read_csv('csv_puliti/airports_database.csv')
df2.drop_duplicates()

lista1 = df['codice_aereoporto_di_partenza'].to_list()
lista2 = df['codice_aereoporto_di_arrivo'].to_list()
lista3 = df2['airport_code'].to_list()
diz = {lista3[i]: i for i in range(len(lista3))}


lista_flight = [[lista1[i], lista2[i]] for i in range(len(lista1))]

df3 = pd.DataFrame(lista_flight, columns=['partenza', 'arrivo'])
print(df3)
df3['partenza'] = df3['partenza'].map(diz)
df3['arrivo'] = df3['arrivo'].map(diz)
print(df3)
df3['arrivo'].to_csv('arrivi_flight_airports.csv')
df3['partenza'].to_csv('partenze_flight_airports.csv')
