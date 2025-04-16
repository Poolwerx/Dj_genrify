from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, BigInteger, ARRAY
from werkzeug.security import generate_password_hash, check_password_hash


def define_models(base):
    class User(base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        tg_id = Column(BigInteger, unique=True, nullable=False)
        playlists = relationship('Playlist', back_populates='user')

    class SiteUser(base):
        __tablename__ = 'site_users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True, nullable=False)
        email = Column(String, unique=True, nullable=True)
        password_hash = Column(String, nullable=False)
        playlists = relationship('Playlist', back_populates='site_user')

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

    class Playlist(base):
        __tablename__ = 'playlists'
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
        user_site_id = Column(Integer, ForeignKey('site_users.id', ondelete='CASCADE'), nullable=True)
        name = Column(String, nullable=False)
        from_platform = Column(String, nullable=False)
        unique_genres = Column(ARRAY(String), nullable=True)
        tracks = Column(JSON, nullable=False)

        user = relationship('User', back_populates='playlists')
        site_user = relationship('SiteUser', back_populates='playlists')

    return User, SiteUser, Playlist
