import secrets
import sqlite3
import os

from flask import Flask, render_template, request, g, flash, redirect, url_for
from yandex_music import Client
from flask_login import LoginManager
from FDataBase import FDataBase
from UserLogin import UserLogin

DATABASE = 'templates/app.db'
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'you-will-never-guess'
key = secrets.token_hex(16)
app.secret_key = key
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'app.db')))

token = 'y0_AgAAAAA2DZGJAAG8XgAAAAD4hlk7I8DRDKyCS7Sj-76dHMBPd9IUD1Q'
client = Client(token).init()
login_manager = LoginManager(app)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''соединение с бд, если его еще нет'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''закрываем соединение с бд, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@login_manager.user_loader()
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


@app.route('/main', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def main():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        # Получаем значение названия трека из формы
        track_name = request.form['track_name']
        # Поиск трека по названию
        search_results = client.search(track_name)

        # Создаем список треков для передачи в шаблон HTML
        trackss = []
        # через цикл заполняем массив словарями (потом поможет при разработки БД)
        for elem in search_results.tracks.results:
            track_info = {
                'title': elem.title,
                'artist': elem.artists[0].name,
                'track_id': elem.id
            }
            trackss.append(track_info)

        return render_template('main.html', tracks=trackss)
    else:
        # пустой массив не отобразит никаких треков
        return render_template('main.html', tracks=[])


@app.route('/begin', methods=["GET", "POST"])
def begin():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['login']) > 4 and len(request.form['password']) > 4:
            res = dbase.addUser(request.form['login'], request.form['password'])
            if res:
                flash('Success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавлении в БД', 'error')
        else:
            flash('Неверно заполнены поля', 'error')
    return render_template('begin.html')


if __name__ == '__main__':
    app.run(debug=True)

