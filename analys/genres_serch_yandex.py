from yandex_music import Client
from analys.pylast_genres import search_pylast_genre
import os
from dotenv import load_dotenv


def get_playlist_tracks(link):
    load_dotenv()
    """Получение объекта плейлиста по ссылке (ЯНДЕКС) -> dict, set возвращает"""

    secret_key = os.getenv('YANDEX_KEY')
    client = Client(secret_key).init()
    try:
        # извлечение данных
        parts = link.rstrip('/').split('/')
        user_id = parts[-3]
        playlist_id = parts[-1]
        playlist = client.users_playlists(playlist_id, user_id)
        song_artist_dict = dict()
        song_artist_set = set()

        for i, track in enumerate(playlist.tracks, start=1):
            track_title = track.track.title
            artists = ', '.join(artist.name for artist in track.track.artists)
            genres = search_pylast_genre(artists, track_title)  # получение жанров
            # группировка по жанрам + добавление в множество
            song_artist_set.update(genres)
            for genre in genres:
                if genre not in song_artist_dict:
                    song_artist_dict[genre] = []

                song_artist_dict[genre].append({
                    'title': track_title,
                    'artists': artists
                })
        print(song_artist_dict)
        print(song_artist_set)
        return playlist.title, song_artist_dict, list(song_artist_set)  # возвращение dict-а, list-а с жанрами по трекам

    except Exception as e:
        print(f"Ошибка: {e}")
