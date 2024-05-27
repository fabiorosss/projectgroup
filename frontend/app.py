from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.config.from_object('config.Config')


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
        cursor.execute(query, params)
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


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/analisi-voli')
def analisivoli():
    return render_template("analisivoli.html")

@app.route('/chi-siamo')
def chisiamo():
    return render_template("chisiamo.html")

@app.route('/registrati')
def registrati():
    return render_template("registrati.html")

@app.route('/contattaci')
def contattaci():
    return render_template("contattaci.html")

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
