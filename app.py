import csv
# import requests

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/movies')
def movies():
    with open('dataset/film.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    return render_template('movies.html', data=data)


@app.route('/music')
def music():
    with open('dataset/music.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return render_template('music.html', data=data)


@app.route('/books')
def books():
    with open('dataset/book.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return render_template('books.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)  # default debug è false
