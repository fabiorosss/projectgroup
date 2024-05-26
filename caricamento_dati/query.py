from funzioni import *

create_database_query = 'CREATE DATABASE JETAIR'
drop_database_query = 'DROP DATABASE IF EXISTS JETAIR'

connessione = create_server_connection('localhost', 'root', 'Gondoliere01_')

drop_database(connessione, drop_database_query)

create_database(connessione, create_database_query)

connessione_db = create_db_connection('localhost', 'root', 'Gondoliere01_', 'JETAIR')

create_flight_data = '''
CREATE TABLE flight_data(
    id INT PRIMARY KEY AUTO_INCREMENT,
    codice_aereoporto_di_partenza CHAR(3) NOT NULL,
    paese_di_partenza VARCHAR(50),
    codice_aereoporto_di_arrivo CHAR(3) NOT NULL,
    paese_di_arrivo VARCHAR(50),
    modello_aereo VARCHAR(150),
    numero_di_compagnie VARCHAR(10),
    nome_compagnia VARCHAR(70),
    codice_volo CHAR(6),
    ora_partenza DATE,
    ora_arrivo DATE,
    num_scali INT,
    prezzo INT,
    emissioni_di_co2 INT IF NOT NULL,
    media_co2_percorso INT IF NOT NULL,
    percentuale_co2 INT IF NOT NULL,
    durata DATE,
    mese VARCHAR(15)
    );
    '''

create_airlines = '''
CREATE TABLE airlines(
    id INT PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(100)
    );
    '''

create_airports = '''
CREATE TABLE airports(
    id INT PRIMARY KEY
    Airport Code VARCHAR(100),
    Airport Name VARCHAR(100),
    City Name VARCHAR(100),
    Country Name VARCHAR(100),
    Country Code CHAR(3),
    Latitude VARCHAR(30),
    Longitude VARCHAR(30),
    coordinates VARCHAR(30)
    );
    '''

create_

