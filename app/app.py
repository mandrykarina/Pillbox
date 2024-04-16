from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/main')
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('main.html')


@app.route('/begin')
def begin():
    return render_template('begin.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)

