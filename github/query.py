import csv
from estrazione_country import *

import numpy as np
import pandas as pd
from unidecode import unidecode
from q import *
from funzioni import *

create_database_query = 'CREATE DATABASE jetair'
drop_database_query = 'DROP DATABASE IF EXISTS jetair'

connessione = create_server_connection('localhost', 'root', 'Gondoliere01_')

drop_database(connessione, drop_database_query)

create_database(connessione, create_database_query)

connessione_db = create_db_connection('localhost', 'root', 'Gondoliere01_', 'jetair')

execute_query(connessione_db, create_country)
execute_query(connessione_db, create_airlines)
execute_query(connessione_db, create_airports)
execute_query(connessione_db, create_flight_data)
execute_query(connessione_db, create_fk_flight_data_airlines)
execute_query(connessione_db, create_fk_rotte1)
execute_query(connessione_db, create_table_utenti)



df_airports = pd.read_csv('../csv_puliti/airports-code2_final.csv')
df_airports.pop('Unnamed: 0')
df_airports.pop('coordinates')
df_airports['Country Name'] = df_airports['Country Name'].map(d)
df_airports = df_airports.replace({np.nan: None})

with open('../csv_puliti/flight_data_final.csv') as file:
    lettore = csv.reader(file)
    next(lettore)
    lista_flight_data = list(lettore)
with open('../csv_puliti/partenze_flight_airports.csv') as file:
    lettore = csv.reader(file)
    next(lettore)
    lista_partenze = list(lettore)
with open('../csv_puliti/arrivi_flight_airports.csv') as file:
    lettore = csv.reader(file)
    next(lettore)
    lista_arrivi = list(lettore)

i = 0
for elem in lista_flight_data:
    i += 1
    elem[0] = i
    elem[1] = lista_partenze[i - 1][1]
    elem[3] = lista_arrivi[i - 1][1]
    elem[11] = int(elem[11])
    elem[17] = int(elem[17])
    elem[12] = float(elem[12])
    try:
        elem[13] = float(elem[13])
    except ValueError:
        elem[13] = float(0)
    try:
        elem[14] = float(elem[14])
    except ValueError:
        elem[14] = float(elem[14] + '.00')
    try:
        elem[15] = int(elem[15])
    except ValueError:
        elem[15] = 0

for elem in lista_flight_data:
    if elem[2] in d.keys():
        elem[2] = d[elem[2]]
    if elem[4] in d.keys():
        elem[4] = d[elem[4]]

with open('flight_data_database_FK.csv', 'w', newline='') as f:
    fieldnames = ['id', 'codice_aereoporto_di_partenza', 'paese_di_partenza', 'codice_aereoporto_di_arrivo',
                  'paese_di_arrivo', 'modello_aereo', 'numero_di_compagnie', 'nome_compagnia', 'codice_volo',
                  'ora_partenza', 'ora_arrivo', 'num_scali', 'prezzo', 'emissioni_di_co2', 'media_co2_percorso',
                  'percentuale_co2', 'durata', 'mese', 'Mese_str']
    writer = csv.writer(f, delimiter=',')
    writer.writerow(fieldnames)
    for row in lista_flight_data:
        writer.writerow(row)

df_airlines = pd.read_csv('../csv_puliti/airlines_final.csv')
df_airlines.pop('Unnamed: 0')
df_airlines['Country'] = df_airlines['Country'].map(d)
df_airlines = df_airlines.replace({np.nan: None})

# df_flight_data = pd.read_csv('../csv_puliti/flight_data_final.csv')
# df_flight_data.pop('Unnamed: 0')
# df_flight_data = df_flight_data.replace({np.nan: None})
# df_flight_data['num_scali'] = df_flight_data['num_scali'].astype(str)
# df_flight_data['mese'] = df_flight_data['mese'].astype(str)
# df_flight_data = df_flight_data.astype(str)
# print(df_flight_data.dtypes)

with open('../csv_puliti/df_da_esportare_final.csv') as file:
    lettore = csv.reader(file)
    next(lettore)
    lista_flight_airlines = list(lettore)

for elem in lista_flight_airlines:
    elem[0] = int(elem[0])
    elem[1] = int(elem[1])
    elem[2] = int(elem[2])

# df_air_fli = pd.read_csv('../csv_puliti/df_da_esportare_final.csv')
# df_air_fli.pop('Unnamed: 0')
# df_air_fli.drop_duplicates(inplace=True)

df_rotte = pd.read_csv('../csv_puliti/routes_final.csv')
df_rotte.pop('Unnamed: 0')
df_rotte.pop('Airline')
df_rotte.replace(r'\N', np.nan, inplace=True)
df_rotte.dropna(inplace=True)

df_country = pd.read_csv('../csv_puliti/country.csv')
df_country.pop('Unnamed: 0')
df_country = df_country.replace({np.nan: None})

caricamento_dataframe(connessione_db, q6, df_country)
caricamento_dataframe(connessione_db, q1, df_airports)
caricamento_dataframe(connessione_db, q2, df_airlines)
caricamento_lista(connessione_db, q3, lista_flight_data)
caricamento_lista(connessione_db, q4, lista_flight_airlines)
caricamento_dataframe2(connessione_db, q5, df_rotte)
