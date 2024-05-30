from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Response
from q import *
from mysql.connector import Error
import hashlib
import base64
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from q import *






app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'


def get_driver(dati_utente):
    options = Options()
    # options.add_argument('--headless')  # Esegui il browser in modalità headless
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def funzione(dati_utente):

    if dati_utente['giorno_partenza'] == None and dati_utente['giorno_arrivo'] == None:
        mese_partenza = f'2024-{dati_utente["mese_partenza"]}-01_2024-{dati_utente["mese_arrivo"]}-31'  # nel caso si effettui la ricerca per mese
        mese_arrivo = f'2024-{dati_utente["mese_partenza"]}-01_2024-{dati_utente["mese_partenza"]}-31'
        if dati_utente['citta_partenza'] == None and dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_partenza'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        else:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"

    elif dati_utente['giorno_partenza'] == None:
        mese_partenza = f'2024-{dati_utente["mese_partenza"]}-01_2024-{dati_utente["mese_arrivo"]}-31'  # nel caso si effettui la ricerca per mese
        mese_arrivo = f'2024-{dati_utente["mese_arrivo"]}-{dati_utente['giorno_arrivo']}'
        if dati_utente['citta_partenza'] == None and dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_partenza'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        else:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"

    elif dati_utente['giorno_arrivo'] == None:
        mese_partenza = f'2024-{dati_utente["mese_partenza"]}-{dati_utente['giorno_partenza']}'
        mese_arrivo = f'2024-{dati_utente["mese_partenza"]}-01_2024-{dati_utente["mese_arrivo"]}-31'
        if dati_utente['citta_partenza'] == None and dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_partenza'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        else:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"

    else:
        mese_partenza = f'2024-{dati_utente["mese_partenza"]}-{dati_utente['giorno_partenza']}'
        mese_arrivo = f'2024-{dati_utente["mese_arrivo"]}-{dati_utente['giorno_arrivo']}'
        if dati_utente['citta_partenza'] == None and dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_partenza'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        elif dati_utente['citta_arrivo'] == None:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"
        else:
            url = f"https://www.kiwi.com/it/search/tiles/{dati_utente['citta_partenza']}-{dati_utente['paese_partenza']}/{dati_utente['citta_arrivo']}-{dati_utente['paese_arrivo']}/{mese_partenza}/{mese_arrivo}"

    print(url)

    # Ottieni il driver
    driver = get_driver()

    # Effettua la richiesta
    driver.get(url)
    driver.maximize_window()

    input("Vai avanti")

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
            print(t_element)
            if t_element.isalpha() and t_element != 'Feedback':
                lista_arrivi.append(t_element)
            elif '€' in t_element:
                lista_arrivi.append(t_element.replace(' ', ''))
    else:
        print('nessun elemento trovato')

    lista_finale = []
    for i in range(1, len(lista_arrivi), 1):
        if arrivo.title() in lista_arrivi[0]:
            lista_finale.append(lista_arrivi[0])
        if lista_arrivi[i].isalpha() and '€' in lista_arrivi[i - 1]:
            lista_finale.append(lista_arrivi[i])
        elif lista_arrivi[i].isalpha() and '€' in lista_arrivi[i - 1]:
            lista_finale.append(lista_arrivi[i])
        elif '€' in lista_arrivi[i] and lista_arrivi[i - 1].isalpha:
            lista_finale.append(lista_arrivi[i])
        else:
            continue

    print(lista_finale)
    input()




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
        if giorno_partenza is None or giorno_arrivo is None:
            funzione_mese(dati)


if __name__ == '__main__':
    app.run(debug=True)
