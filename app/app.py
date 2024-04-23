import secrets
import base64
import os

from flask import Flask, render_template, request, session, redirect, send_from_directory
from yandex_music import Client
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
key = secrets.token_hex(16)
app.secret_key = key

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'

TRACKS_FOLDER = os.path.join(os.getcwd(), 'tracks')
app.config['UPLOAD_FOLDER'] = TRACKS_FOLDER

db = SQLAlchemy(app)
Session(app)

TOKEN = 'y0_AgAAAAA2DZGJAAG8XgAAAAD4hlk7I8DRDKyCS7Sj-76dHMBPd9IUD1Q'
client = Client(TOKEN).init()


class Users(db.Model):
    '''
    Класс работы с базой данных пользователей
    '''
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)


class Playlists(db.Model):
    '''
    Класс работы с базой данных плэйлистов треков
    '''
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    tracks = db.Column(db.Text)


@app.route('/main', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def main():
    '''
    Страница с возможностью поиска трека по названию.
    '''

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
        return render_template('main.html', tracks=trackss, playlists=Playlists.query.all())

    else:
        return render_template('main.html', tracks=[], audio_file="")


@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory('uploads', filename)


@app.route('/playlists', methods=["GET", "POST"])
def playlists():
    '''
    Страница с возможностью создания и отображения собственных плэйлистов пользователя.
    '''

    if 'username' in session:
        playlists = [elem for elem in Playlists.query.all() if elem.userid == session['userid']]
        if request.method == 'POST':

            playlist_name = request.form['playlist_name']
            image = request.files['playlist_image']
            data = image.read()

            try:
                # фиксинг
                ls = [elem[0] for elem in Playlists.query.with_entities(Playlists.title).all()]
                if playlist_name not in ls:
                    newplaylist = Playlists(title=playlist_name, userid=int(session['userid']), image=data)
                    db.session.add(newplaylist)
                    db.session.commit()

                # преобразуем картинки
                images = []
                for img in [elem[0] for elem in Playlists.query.with_entities(Playlists.image).all()]:
                    try:
                        images.append(base64.b64encode(img).decode('utf-8'))
                    except:
                        images.append(None)

                return render_template('playlists.html', datas=zip(playlists, images))
            except:
                return 'Ошибка при добавлении пользователя'
        else:
            images = []
            for img in [elem[0] for elem in Playlists.query.with_entities(Playlists.image).all()]:
                try:
                    images.append(base64.b64encode(img).decode('utf-8'))
                except:
                    images.append(None)

            return render_template('playlists.html', datas=zip(playlists, images))
    return redirect('/begin')


@app.route('/begin', methods=["GET", "POST"])
def begin():
    '''
    Страница регистарции и авторизации пользователя.
    В конце создается новая активная сессия работы.
    '''

    if request.method == 'POST':

        action = request.form['action']
        login = request.form['login']
        password = request.form['password']
        if len(login) < 5 or len(password) < 5:
            return render_template('begin.html', error_message="слишком короткий логин или пароль")
        if action == "register":
            answ = register(login, password)
            return answ

        elif action == "login":
            answ = login_func(login, password)
            return answ
    else:
        return render_template('begin.html', error_message="")


def register(login: str, password: str):
    '''
    Функция проведения этапа регистрации пользователя на сайте
    '''

    user = Users(login=login, password=password)
    try:
        # массив уже зарегистрированных пользователей
        ls_users = [elem[0] for elem in Users.query.with_entities(Users.login).all()]
        # логины не должны повторяться
        if login not in ls_users:
            db.session.add(user)
            db.session.commit()

            session['username'] = login
            user = Users.query.filter_by(login=login).first()
            session['userid'] = user.id
            return redirect('/')
        else:
            return render_template("begin.html", error_message="Пользватель с таким логином уже зарегистрирован")
    except:
        return render_template("begin.html", error_message="Неккоректно введены логин или пароль")


def login_func(login: str, password: str):
    '''
    Функция авторизации пользователя в системе с использованием активной сессии.
    '''

    user = Users.query.filter_by(login=login).first()

    if user is None:
        return render_template("begin.html", error_message="Пользватель с таким логином еще не зарегистрирован")

    if user.password == password:
        session['username'] = login
        user = Users.query.filter_by(login=login).first()
        session['userid'] = user.id
        return redirect('/')

    return render_template("begin.html", error_message="Неверный логин или пароль")


if __name__ == '__main__':
    app.run(debug=True)
