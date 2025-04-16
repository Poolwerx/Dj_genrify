import pylast
import time
import webbrowser
from functools import lru_cache
import os
from dotenv import load_dotenv


class PylastClient:
    """Клиент для работы с Last.fm."""
    load_dotenv()
    API_KEY = os.getenv("API_KEY_LASTFM")
    API_SECRET = os.getenv("API_SECRET_LASTFM")
    SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".session_key")

    # Список запрещенных тегов
    FORBIDDEN_TAGS = {"govno", "myspotigrambot", "russian cock"}  # Здесь можно добавить любые нежелательные теги

    def __init__(self):
        self.network = pylast.LastFMNetwork(api_key=self.API_KEY, api_secret=self.API_SECRET)
        self.session_key = self._get_or_create_session_key()
        self.network.session_key = self.session_key

    def _get_or_create_session_key(self):
        """Получение или создание session_key для работы с API."""
        if os.path.exists(self.SESSION_KEY_FILE):
            with open(self.SESSION_KEY_FILE, "r") as f:
                return f.read()

        skg = pylast.SessionKeyGenerator(self.network)
        url = skg.get_web_auth_url()
        print(f"Please authorize this script to access your account: {url}\n")
        webbrowser.open(url)

        while True:
            try:
                session_key = skg.get_web_auth_session_key(url)
                with open(self.SESSION_KEY_FILE, "w") as f:
                    f.write(session_key)
                return session_key
            except pylast.WSError:
                time.sleep(1)

    @lru_cache(maxsize=128)
    def get_track_tags(self, artists, title, limit=2):
        """
        Получить теги трека. Если у трека нет тегов, попробовать взять теги артиста.
        """
        try:
            track = self.network.get_track(artists, title)
            tags = track.get_top_tags()
            if not tags:  # Если нет тегов у трека
                artist = track.get_artist()
                tags = artist.get_top_tags()

            # Фильтрация нежелательных тегов
            filtered_tags = []
            for tag in tags[:limit]:
                tag_name = tag.item.get_name().lower()
                if tag_name not in self.FORBIDDEN_TAGS:  # Проверяем, что тег не запрещённый
                    filtered_tags.append(tag_name)

            if not filtered_tags:  # Если все теги запрещены, возвращаем "unknown"
                return ["unknown"]
            return filtered_tags
        except Exception as e:
            print(f"Ошибка при получении тегов для {artists} - {title}: {e}")
            return ["unknown"]


# использование клиента
def search_pylast_genre(artists, title):
    """
    функция для поиска жанров.
    возвращает основной жанр трека (первый из списка) или "unknown", если жанры не найдены.
    """
    client = PylastClient()
    genres = client.get_track_tags(artists, title)

    if genres:
        print(f"Жанры для {artists} - {title}: {', '.join(genres)}")
        return genres
    else:
        print(f"Жанры для {artists} - {title} не найдены.")
        return ["not defined"]
