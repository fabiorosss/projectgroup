from flask import Flask, render_template, request, redirect, url_for
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


def caricamento_lista(connection, query, d):
    lista = []
    for k, v in d.items():
        lista.append(v)
    data = tuple(lista)
    print(data)
    try:
        cursor = connection.cursor()
        cursor.executemany(query, (data,))
        connection.commit()
        print("Query successful")
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


def execute_query(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        try:
            cursor.execute(query, params)
        except Error as e:
            print(e)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
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
@app.route('/')
def home():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return render_template("home.html", output=Response(output.getvalue(), mimetype='image/png'))


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

        password = hashlib.md5(password.encode())
        print(password.hexdigest())

        dati = {
            'email': email,
            'password': str(password).replace('md5 _hashlib.HASH object @ ',''),
            'nome': name.title(),
            'cognome': surname.title(),
            'indirizzo': address,
            'citta': city.title()
        }
        caricamento_lista(connection, q7, dati)

    return redirect(url_for('home'))


@app.route('/contattaci')
def contattaci():
    return render_template("contattaci.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/registrati')
def registrati():
    return render_template('registrati.html')


if __name__ == '__main__':
    app.run(debug=True)
