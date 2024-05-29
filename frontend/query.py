import csv
from estrazione_country import *

import numpy as np
import pandas as pd
from unidecode import unidecode

from funzioni import *

create_database_query = 'CREATE DATABASE jetair'
drop_database_query = 'DROP DATABASE IF EXISTS jetair'

connessione = create_server_connection('localhost', 'root', 'Gondoliere01_')

drop_database(connessione, drop_database_query)

create_database(connessione, create_database_query)

connessione_db = create_db_connection('localhost', 'root', 'Gondoliere01_', 'jetair')

create_flight_data = '''
CREATE TABLE flight_data(
    id INT PRIMARY KEY,
    codice_aereoporto_di_partenza INT,
    paese_di_partenza INT,
    codice_aereoporto_di_arrivo INT,
    paese_di_arrivo INT,
    modello_aereo VARCHAR(150),
    numero_di_compagnie VARCHAR(10),
    nome_compagnia VARCHAR(120),
    codice_volo CHAR(6),
    ora_partenza VARCHAR (255),
    ora_arrivo VARCHAR (255),
    num_scali INT,
    prezzo DECIMAL(7,2),
    emissioni_di_co2 DECIMAL(10,2),
    media_co2_percorso DECIMAL(10,2),
    percentuale_co2 INT,
    durata VARCHAR (255),
    mese INT,
    Mese_str VARCHAR(15),
    FOREIGN KEY (codice_aereoporto_di_partenza) REFERENCES airports(id) ON DELETE RESTRICT,
    FOREIGN KEY (codice_aereoporto_di_arrivo) REFERENCES airports(id) ON DELETE RESTRICT,
    FOREIGN KEY (paese_di_partenza) REFERENCES country(id) ON DELETE RESTRICT,
    FOREIGN KEY (paese_di_arrivo) REFERENCES country(id) ON DELETE RESTRICT
    );
    '''

create_airlines = '''
CREATE TABLE airlines(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    country INT,
    FOREIGN KEY (country) REFERENCES country(id)
    );
    '''

create_airports = '''
CREATE TABLE airports(
    id INT PRIMARY KEY AUTO_INCREMENT,
    airport_code VARCHAR(10) UNIQUE,
    airport_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name INT,
    country_code CHAR(3),
    latitude INT,
    longitude INT,
    FOREIGN KEY (country_name) REFERENCES country(id)
    );
    '''

create_fk_flight_data_airlines = '''
CREATE TABLE flight_data_airlines(
    id INT,
    airlines_flight_data INT,
    airlines_airlines INT,
    PRIMARY KEY (id, airlines_flight_data, airlines_airlines),
    FOREIGN KEY (airlines_flight_data) REFERENCES flight_data(id) ON DELETE RESTRICT,
    FOREIGN KEY (airlines_airlines) REFERENCES airlines(id) ON DELETE RESTRICT
    );
    '''

create_fk_rotte1 = '''
CREATE TABLE rotte1(
    airline_id INT,
    departure_airport VARCHAR(10),
    departure_airport_id INT,
    arrival_airport VARCHAR(10),
    arrival_airport_id INT,
    PRIMARY KEY (airline_id, departure_airport, arrival_airport),
    FOREIGN KEY (departure_airport) REFERENCES airports(airport_code),
    FOREIGN KEY (arrival_airport) REFERENCES airports(airport_code),
    FOREIGN KEY (airline_id) REFERENCES airlines(id)
);
'''

create_country = '''
CREATE TABLE country(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE
    );
    '''

create_table_utenti = '''
CREATE TABLE utenti(
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(120),
    password VARCHAR(30),
    nome VARCHAR(50),
    cognome VARCHAR(50),
    indirizzo VARCHAR(150),
    città VARCHAR(150)
    );
    '''


delete_from_utenti = '''
    ALTER TABLE utenti(
    
    '''

create_trigger_ins_att = '''
CREATE TRIGGER tr_utenti AFTER INSERT ON utenti
FOR EACH ROW
BEGIN
  INSERT INTO platform (operazione, id, data)
  VALUES ('INSERT', NEW.id, CURRENT_TIMESTAMP);
END;
'''

create_trigger_del_att = '''
CREATE TRIGGER tr_utenti_delete AFTER DELETE ON utenti
FOR EACH ROW
BEGIN
  INSERT INTO platform (operazione, id, data)
  VALUES ('DELETE', OLD.id, CURRENT_TIMESTAMP);
END;
'''

execute_query(connessione_db, create_country)
execute_query(connessione_db, create_airlines)
execute_query(connessione_db, create_airports)
execute_query(connessione_db, create_flight_data)
execute_query(connessione_db, create_fk_flight_data_airlines)
execute_query(connessione_db, create_fk_rotte1)
execute_query(connessione_db, create_table_utenti)

q1 = f'INSERT INTO airports (airport_code, airport_name, city_name, country_name, country_code, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)'
q2 = f'INSERT INTO airlines(name, country) VALUES (%s, %s)'
q3 = (
    f'INSERT INTO flight_data(id, codice_aereoporto_di_partenza,paese_di_partenza,codice_aereoporto_di_arrivo,paese_di_arrivo,modello_aereo,'
    f'numero_di_compagnie,nome_compagnia,codice_volo,ora_partenza,ora_arrivo,num_scali,prezzo,emissioni_di_co2,media_co2_percorso,percentuale_co2,durata,mese,Mese_str)'
    f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
q4 = f'INSERT INTO flight_data_airlines(id, airlines_flight_data, airlines_airlines) VALUES (%s, %s, %s)'
q5 = f'INSERT INTO rotte1(airline_id, departure_airport, departure_airport_id, arrival_airport, arrival_airport_id) VALUES (%s, %s, %s, %s, %s)'
q6 = f'INSERT INTO country(name) VALUES (%s)'
q7 = f'INSERT INTO utenti(email, password, nome, cognome, indirizzo, citta) VALUES (%s, %s, %s, %s, %s, %s)'

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


