import secrets
import os

from flask import Flask, render_template, request, flash, redirect, url_for
from yandex_music import Client
from flask_sqlalchemy import SQLAlchemy

# from flask_login import LoginManager
# from UserLogin import UserLogin


app = Flask(__name__)
key = secrets.token_hex(16)
app.secret_key = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
db = SQLAlchemy(app)
token = 'y0_AgAAAAA2DZGJAAG8XgAAAAD4hlk7I8DRDKyCS7Sj-76dHMBPd9IUD1Q'
client = Client(token).init()
# login_manager = LoginManager(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)


class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    tracks = db.Column(db.Text)


@app.route('/main', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        track_name = request.form['track_name']
        search_results = client.search(track_name)
        trackss = []
        for elem in search_results.tracks.results:
            track_info = {
                'title': elem.title,
                'artist': elem.artists[0].name,
                'track_id': elem.id
            }
            trackss.append(track_info)
        return render_template('main.html', tracks=trackss)

    else:
        return render_template('main.html', tracks=[])


@app.route('/playlists', methods=["GET", "POST"])
def playlists():
    playlists = Playlists.query.all()
    if request.method == 'POST':
        playlist_name = request.form['playlist_name']
        playlist_image = request.form['playlist_image']
        playlist = Playlists(title=playlist_name, image=playlist_image)
        try:
            db.session.add(playlist)
            db.session.commit()
            return render_template('playlists.html', playlists=playlists)
        except:
            return 'Ошибка при добавлении пользователя'
    else:
        return render_template('playlists.html', playlists=playlists)


@app.route('/begin', methods=["GET", "POST"])
def begin():
    return render_template('begin.html')


@app.route('/registre', methods=["GET", "POST"])
def registre():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user = Users(login=login, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка при добавлении пользователя'
    else:
        return render_template('registre.html')


if __name__ == '__main__':
    app.run(debug=True)
