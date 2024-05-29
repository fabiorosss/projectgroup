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
    email VARCHAR(120) UNIQUE,
    password VARCHAR(30),
    nome VARCHAR(50),
    cognome VARCHAR(50),
    indirizzo VARCHAR(150),
    città VARCHAR(150)
    );
    '''

create_table_trigger = '''
CREATE TABLE platform(
    operazione VARCHAR(10),
    data TIMESTAMP,
    id_riga INT
);
'''

create_trigger_inserimento_utenti = '''
DELIMI
CREATE TRIGGER tr_utenti_delete AFTER DELETE ON utenti
FOR EACH ROW
BEGIN
  INSERT INTO platform (operazione, id, data)
  VALUES ('INSERT', OLD.id, CURRENT_TIMESTAMP);
END$$

DELIMITER ;
'''

create_trigger_elim_utenti = '''
DELIMITER $$

CREATE TRIGGER tr_eliminazione_utenti AFTER DELETE ON utenti
FOR EACH ROW
BEGIN
  INSERT INTO platform (operazione, data, id_riga)
  VALUES ('DELETE', CURRENT_TIMESTAMP, OLD.id);
END$$

DELIMITER ;
'''

accedi_su_sito = '''
    SELECT *
    FROM utenti
    WHERE email = %s AND password = %s
'''

delete_from_utenti = '''
    ALTER TABLE utenti(
    DELETE * FROM utenti
    WHERE email = %s AND password = %s
    );
    '''

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

query_email = '''
SELECT email
FROM utenti
WHERE email = %s
'''
