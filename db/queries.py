from db.models import define_models
from db.engine import DatabaseEngine
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DATABASE_URL


class DBquaries:
    def __init__(self, session, base):
        """Инициализация"""
        self.session = session
        self.User, self.SiteUser, self.Playlist = define_models(base)

    # добавления юзера для тг
    def add_user(self, tg_id: int):
        """Добавление нового пользователя, если он не существует"""
        user = self.session.query(self.User).filter_by(tg_id=tg_id).first()
        if user:
            return user

        # Если пользователя нет, добавляем нового
        new_user = self.User(tg_id=tg_id)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def add_playlist(self, user_id: int, name: str, from_platform: str, unique_genres: list, tracks: dict):
        """Добавление нового плейлиста"""
        new_playlist = self.Playlist(user_id=user_id,
                                     name=name,
                                     from_platform=from_platform,
                                     unique_genres=unique_genres,
                                     tracks=tracks)
        self.session.add(new_playlist)
        self.session.commit()
        return new_playlist

    def add_playlist_for_site(self, user_id: int, name: str, from_platform: str, unique_genres: list, tracks: dict):
        """Добавление нового плейлиста"""
        new_playlist = self.Playlist(user_site_id=user_id,
                                     name=name,
                                     from_platform=from_platform,
                                     unique_genres=unique_genres,
                                     tracks=tracks)
        self.session.add(new_playlist)
        self.session.commit()
        return new_playlist

    def get_user_playlists(self, tg_id: int):
        """Получение всех плейлистов по айдишнику"""
        user = self.session.query(self.User).filter_by(tg_id=tg_id).first()
        return user.playlists if user else None

    def get_site_user_playlists(self, site_user_id: int):
        """Получение всех плейлистов по айдишнику"""
        user = self.session.query(self.SiteUser).filter_by(id=site_user_id).first()
        return user.playlists if user else None

    def get_playlist_by_id(self, playlist_id: int):
        """Получение плейлиста по айдишнику"""
        playlist = self.session.query(self.Playlist).filter_by(id=playlist_id).first()
        return playlist if playlist else None

    def get_user_site_by_username(self, username: str):
        """Получение плейлиста по айдишнику"""
        user = self.session.query(self.SiteUser).filter_by(username=username).first()
        return user if user else None

    # тут нет в добавлении почты, потомучт она не используется пока
    def add_site_user(self, username: str, password: str):
        """Добавление нового плейлиста"""
        new_site_user = self.SiteUser(username=username)
        new_site_user.set_password(password)
        self.session.add(new_site_user)
        self.session.commit()
        return new_site_user


def create_all_tables():
    """Создание всех таблиц"""
    db_engine = DatabaseEngine(DATABASE_URL)
    Base = db_engine.get_base()
    define_models(Base)
    db_engine.create_tables(Base)
    print('Все таблицы созданы')
