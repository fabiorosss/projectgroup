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

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'


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


@app.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('q')
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT city_name FROM cities WHERE city_name LIKE %s LIMIT 3", (f"%{query}%",))
    results = cursor.fetchall()
    suggestions = [row[0] for row in results]
    cursor.close()
    connection.close()
    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=True)
