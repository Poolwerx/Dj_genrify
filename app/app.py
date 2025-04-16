from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_login import (LoginManager, UserMixin, login_required, login_user, logout_user, current_user)
from check_forms import check_register_form, check_login_form, check_form_add_playlist
from db.queries import DBquaries  # Теперь просто импортируем уже готовый объект
from config import DATABASE_URL
from db.engine import DatabaseEngine
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db_engine = DatabaseEngine(DATABASE_URL)
session2 = db_engine.get_session()
Base = db_engine.get_base()
db_queries = DBquaries(session2, Base)


class UserLogin(UserMixin):
    def __init__(self, user):
        self.id = user.username  # Flask-Login требует строковый id
        self.username = user.username


@login_manager.user_loader
def load_user(username):
    user = db_queries.get_user_site_by_username(username=username)
    return UserLogin(user) if user else None


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Проверяем, вошёл ли пользователь
        return redirect(url_for('account'))  # Если да, отправляем в аккаунт
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_login_form(username, password)
        if user:
            login_user(UserLogin(user))
            return redirect(url_for('account', username=user.username))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # Проверяем, вошёл ли пользователь
        return redirect(url_for('account'))  # Если да, отправляем в аккаунт
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if check_register_form(username, password, confirm_password):
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/account_<username>')
@login_required
def account(username):
    if username != current_user.username:
        flash("Доступ запрещен!", "danger")
        return redirect(url_for('index'))
    playlists = db_queries.get_site_user_playlists(db_queries.get_user_site_by_username(current_user.username).id)
    return render_template('account.html', username=current_user.username, playlists=playlists)


@app.route('/add_playlist', methods=['GET', 'POST'])
def add_playlist():
    if request.method == 'POST':
        playlist_url = request.form['playlist_url']
        checkbox = request.form.get('service')
        check_form_add_playlist(playlist_url, checkbox, current_user.username)
    return render_template('add_playlist.html')


@app.route('/playlist_<id>', methods=['GET', 'POST'])
def playlist(id):
    playlist = db_queries.get_playlist_by_id(id)
    track_dict = {}
    for genre, tracks in playlist.tracks.items():
        for track in tracks:
            key = (track["title"], track["artists"])
            if key not in track_dict:
                track_dict[key] = {"title": track["title"], "artists": track["artists"], "genres": []}
            track_dict[key]["genres"].append(genre)
    flattened_tracks = list(track_dict.values())
    return render_template('playlist.html', playlist=playlist, flattened_tracks=flattened_tracks)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта.", "warning")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=False)
