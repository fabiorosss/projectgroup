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

create_trigger = '''
CREATE TABLE platform(
    operazione VARCHAR(10),
    data TIMESTAMP,
    id_riga INT
);
'''

country_city_airport = '''
SELECT a.city_name, a.airport_name, a.latitude, a.longitude
FROM airports AS a
INNER JOIN country AS c
ON a.country_name = c.id
WHERE c.name = %s
'''

city_airport = '''
SELECT name
FROM country
'''

