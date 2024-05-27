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


@app.route('/artisti')
def artisti():
    lista_artisti = execute_query('SELECT * from artist')
    return render_template("artisti.html", artisti=lista_artisti)


@app.route('/artista/<id>')
def artista(id):
    artista = execute_query('SELECT * FROM artist WHERE artist_id = %s', (id,))
    lista_opere_r = execute_query("""SELECT artwork.title
                                    FROM artist
                                    JOIN make_artwork ON artist.artist_id = make_artwork.artist_id
                                    JOIN artwork ON artwork.artwork_id = make_artwork.artwork_id
                                    WHERE artist.artist_id = %s""", (id,))
    return render_template("artista.html", artista=artista[0], lista_opere=lista_opere_r)


@app.route('/artisti/<nationality>')
def artista_n(nationality):
    lista_artisti = execute_query('SELECT * FROM artist WHERE artist.nationality = %s', (nationality,))
    return lista_artisti


@app.route('/opere')
def opere():
    lista_opere = execute_query('SELECT * FROM artwork LIMIT 0,50')
    return render_template("opere.html", opere=lista_opere)


if __name__ == '__main__':
    app.run(debug=True)
