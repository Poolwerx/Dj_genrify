from db.queries import DBquaries
from analys.genres_serch_yandex import get_playlist_tracks
from config import DATABASE_URL
from db.engine import DatabaseEngine
from flask import flash, url_for, redirect
import time
import re

db_engine = DatabaseEngine(DATABASE_URL)
session = db_engine.get_session()
Base = db_engine.get_base()
db_queries = DBquaries(session, Base)


# функция проверки
def check_register_form(username, password, confirm_password):
    user = db_queries.get_user_site_by_username(username)
    if user:
        flash('Пользователь c таким ником уже существует!', 'warning')
    elif len(password) < 6:
        flash('Пароль слишком короткий, минимум 6 символов!', 'danger')
    elif password != confirm_password:
        flash('Пароли не совпадают!', 'danger')
    else:
        db_queries.add_site_user(username, password)  # Добавляем пользователя
        flash('Регистрация успешна! Теперь войдите.', 'success')
        return True


# проверка логин формы + доделать
def check_login_form(username, password):
    user = db_queries.get_user_site_by_username(username)
    if not (user):
        flash('Пользователя c таким ником не существует!', 'danger')
        return False
    else:
        ans = user.check_password(password)
        if ans:
            return user
        flash('Пароль неверный!', 'danger')
        return False


def check_form_add_playlist(playlist_url, checkbox, current_user):
    # регулярки
    ya_music_pattern = r"^https:\/\/music\.yandex\.ru\/users\/[\w-]+\/playlists\/\d+"
    user = db_queries.get_user_site_by_username(current_user)
    if checkbox == 'ya_music':
        if not re.match(ya_music_pattern, playlist_url):
            return False
        else:
            playlist_title, tracks, unique_genres = get_playlist_tracks(playlist_url)
            db_queries.add_playlist_for_site(user.id,
                                             playlist_title,
                                             'Яндекс',
                                             unique_genres,
                                             tracks)
            return True
    elif checkbox == 'yt_music':
        pass
    elif checkbox == 'vk_music':
        pass

    return True
