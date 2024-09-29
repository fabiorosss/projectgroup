from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from webdriver_manager.chrome import ChromeDriverManager

from q import *
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from q import *
from flask import Flask, request

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'


def get_driver():
    options = Options()
    # options.add_argument('--headless')  # Esegui il browser in modalità headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def funzione_mese(dati_utente):
    url_giorni = 'https://www.kiwi.com/it/search/tiles/italia/italia/2024-06-09/2024-07-12'
    url_mesi = 'https://www.kiwi.com/it/search/tiles/italia/italia/2024-06-01_2024-06-30/2024-07-01_2024-07-30'
    if dati_utente['giorno_partenza'] == '' and dati_utente['giorno_arrivo'] == '':
        if dati_utente['mese_partenza'] == '11' or dati_utente['mese_partenza'] == '04' or dati_utente[
            'mese_partenza'] == '06' or dati_utente['mese_partenza'] == '09' and dati_utente['mese_arrivo'] == '11' or \
                dati_utente['mese_arrivo'] == '04' or dati_utente['mese_arrivo'] == '06' or dati_utente['mese_arrivo'] == '09':
            url = f'https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza'].lower()}/{dati_utente['paese_arrivo'].lower()}/2024-{dati_utente['mese_partenza']}-01_2024-{dati_utente['mese_partenza']}-30/2024-{dati_utente['mese_arrivo']}-01_2024-{dati_utente['mese_arrivo']}-30'
        elif dati_utente['mese_partenza'] == '11' or dati_utente['mese_partenza'] == '04' or dati_utente[
            'mese_partenza'] == '06' or dati_utente['mese_partenza'] == '09':
            url = f'https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza'].lower()}/{dati_utente['paese_arrivo'].lower()}/2024-{dati_utente['mese_partenza']}-01_2024-{dati_utente['mese_partenza']}-30/2024-{dati_utente['mese_arrivo']}-01_2024-{dati_utente['mese_arrivo']}-31'  # nel caso si effettui la ricerca per mese
        elif dati_utente['mese_arrivo'] == '11' or dati_utente['mese_arrivo'] == '04' or dati_utente[
            'mese_arrivo'] == '06' or dati_utente['mese_arrivo'] == '09':
            url = f'https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza'].lower()}/{dati_utente['paese_arrivo'].lower()}/2024-{dati_utente['mese_partenza']}-01_2024-{dati_utente['mese_partenza']}-31/2024-{dati_utente['mese_arrivo']}-01_2024-{dati_utente['mese_arrivo']}-30'
        else:
            url = f'https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza'].lower()}/{dati_utente['paese_arrivo'].lower()}/2024-{dati_utente['mese_partenza']}-01_2024-{dati_utente['mese_partenza']}-31/2024-{dati_utente['mese_arrivo']}-01_2024-{dati_utente['mese_arrivo']}-31'
    else:
        url = f'https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza'].lower()}/{dati_utente['paese_arrivo'].lower()}/2024-{dati_utente['mese_partenza']}-{dati_utente['giorno_partenza']}/2024-{dati_utente['mese_arrivo']}-{dati_utente['giorno_arrivo']}'

    print(url)

    # Ottieni il driver
    driver = get_driver()

    # Effettua la richiesta
    driver.get(url)
    driver.maximize_window()
    sleep(10)
    html_content = driver.page_source

    try:
        accept_button = driver.find_element(By.ID, "cookies_accept")
        accept_button.click()
    except Exception as e:
        print("Non è stato possibile trovare il bottone di accettazione dei cookie:", e)

    tag_name = "span"
    elements = driver.find_elements(By.TAG_NAME, tag_name)
    lista_arrivi = []
    if elements:
        for index, element in enumerate(elements):
            t_element = element.text
            if ('€' in t_element or t_element.isnumeric()) and len(t_element) > 1:
                lista_arrivi.append(t_element.replace(' ', ''))
    else:
        print('nessun elemento trovato')
    div = driver.find_element(By.CSS_SELECTOR, ".flex.min-h-screen.flex-col").get_attribute('textContent')
    sleep(1)
    lista = div.split('loading')
    lista_completa = []
    for elem in lista:
        if ',' in elem:
            lista_completa.append(elem.split(',')[0])
    for elem in lista_completa:
        if "\xa0" not in elem:
            lista_completa.pop(lista_completa.index(elem))
    lista_completa2 = []
    for elem in lista_completa:
        lista_completa2.append(elem.split("\xa0"))

    j = 0
    for i in range(len(lista_completa2)):
        if '€' in lista_arrivi[i]:
            lista_completa2[j].append(lista_arrivi[i])
            j += 1
        elif lista_arrivi[i].isnumeric():
            lista_completa2[j].append(str(lista_arrivi[i]) + '€')
            j += 1
    driver.quit()
    return lista_completa2


def caricamento_lista(connection, query, d):
    lista = []
    for k, v in d.items():
        lista.append(v)
    data = tuple(lista)
    mail = lista[0]
    print(data)
    print(mail)
    try:
        cursor = connection.cursor()
        cursor.execute(query_email, (mail,))
        risultati = cursor.fetchone()
        if risultati:
            flash('La mail è già in utilizzo da un altro utente', 'error')
            print('ti ho fregato di nuovo')
            return 1
        else:
            cursor.executemany(query, (data,))
            connection.commit()
            print("Query successful")
            return 0
    except Error as err:
        print(f"Error: '{err}'")


def create_db_connection():
    db_config = {
        'host': app.config['MYSQL_HOST'],
        'user': app.config['MYSQL_USER'],
        'password': app.config['MYSQL_PASSWORD'],
        'database': app.config['MYSQL_DB']
    }
    return mysql.connector.connect(**db_config)


def read_query(query, params):
    print(params)
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, (params['password'], params['email'],))
    except Error as e:
        print(e)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def read_query2(c, query):
    print(query)
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
    except Error as e:
        print(e)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    print(result)
    return result


def read_query3(c, q, p):
    print(q)
    print(p)
    cursor = c.cursor(dictionary=True)
    try:
        cursor.execute(q, (p['country'],))
    except Error as e:
        print(e)
    result = cursor.fetchall()
    cursor.close()
    c.close()
    print(result)
    return result


def read_query4(q1, p):
    c = create_db_connection()
    cursor = c.cursor(dictionary=True)
    try:
        cursor.execute(q1, (p['country'],))
    except Error as e:
        print(e)
    result = cursor.fetchall()
    cursor.close()
    c.close()
    print(result)
    return result


def inserisci_dati(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = [1, 4, 6, 9]
    ys = [10, 20, 30, 40]
    axis.plot(xs, ys)
    plt.xlabel('Numeri')
    plt.ylabel('Altro')
    plt.title('Esperimento di plotting')
    return fig


##########
##ROUTES##
##########
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/analisi-voli')
def analisivoli():
    return render_template("analisivoli.html")


@app.route('/chi-siamo')
def chisiamo():
    return render_template("chisiamo.html")


@app.route('/registra_utente', methods=['POST'])
def registra_utente():
    connection = create_db_connection()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        surname = request.form.get('surname')
        address = request.form.get('address')
        city = request.form.get('city')

        dati = {
            'email': email,
            'password': password,
            'nome': name.title(),
            'cognome': surname.title(),
            'indirizzo': address,
            'citta': city.title()
        }
        risultato = caricamento_lista(connection, q7, dati)
        if risultato == 0:
            return redirect(url_for('home'))
        elif risultato == 1:
            return render_template('registrati.html')


@app.route('/contattaci')
def contattaci():
    return render_template("contattaci.html")


@app.route('/', methods=['POST', 'GET'])
def login():
    connection = create_db_connection()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        dati = {
            "password": password,
            "email": email,
        }
        print(dati)
        user = read_query(accedi_su_sito, dati)
        print(user)
        if user:
            return redirect(url_for('home'))
        else:
            # If user does not exist, stay on the login page with an error message
            flash('Invalid email or password', 'error')
            return render_template("login.html")
    return render_template("login.html")


@app.route('/registrati')
def registrati():
    return render_template('registrati.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Rimuove l'ID dell'utente dalla sessione
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/prezzi-voli')
def prezzi_voli():
    return render_template('prezzivoli.html')


@app.route('/ricerca', methods=['POST', 'GET'])
def ricerca():
    if request.method == 'POST':
        paese_partenza = request.form.get('paese_partenza')
        paese_arrivo = request.form.get('paese_arrivo')
        citta_partenza = request.form.get('citta_partenza')
        citta_arrivo = request.form.get('citta_arrivo')
        mese_partenza = request.form.get('mese_partenza')
        mese_arrivo = request.form.get('mese_arrivo')
        giorno_partenza = request.form.get('giorno_partenza')
        giorno_arrivo = request.form.get('giorno_arrivo')
        dati = {
            "paese_partenza": paese_partenza,
            "paese_arrivo": paese_arrivo,
            "citta_partenza": citta_partenza,
            "citta_arrivo": citta_arrivo,
            "mese_partenza": mese_partenza,
            "mese_arrivo": mese_arrivo,
            "giorno_partenza": giorno_partenza,
            "giorno_arrivo": giorno_arrivo
        }
        print(dati)
        lista = funzione_mese(dati)
        destinazioni = []
        for i in range(10):
            for j in range(len(lista)):
                destinazioni.append(
                    {'partenza': lista[i][j], 'destinazione': lista[i][j + 1], 'prezzo': lista[i][j + 2]})
                break
        return render_template('prezzivoli.html', destinazioni=destinazioni, show_results=True)


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/citta')
def citta():
    print('ciao')
    connection = create_db_connection()
    result = read_query2(connection, city_airport)
    return render_template('search_citta.html', results=result)


@app.route('/aeroporto')
def aeroporto():
    print('ciao')
    connection = create_db_connection()
    result = read_query2(connection, airport_name)
    return render_template('search_aeroporto.html', results=result)


# @app.route('/search_citta')
# def search_citta():
#
#     return render_template('search_citta.html', result=result)


@app.route('/scelta2', methods=['POST', 'GET'])
def scelta2():
    scelta = request.form.get('country')
    s = {
        'country': scelta
    }
    print('ciao')
    res = read_query4(count_airport_p, s)
    res2 = read_query4(count_airport_a, s)
    return render_template('search_aeroporto.html', part=res, arr=res2, show_results=True)


@app.route('/scelta', methods=['POST', 'GET'])
def scelta():
    scelta = request.form.get('country')
    s = {
        'country': scelta
    }
    print(scelta)
    connection = create_db_connection()
    res = read_query3(connection, country_city_airport, s)
    if res:
        return render_template('search_citta.html', results=res, show_results=True)
    else:
        flash('Nessun risultato trovato per il paese selezionato.', 'error')
        return redirect(url_for('citta'))


if __name__ == '__main__':
    app.run(debug=True)
