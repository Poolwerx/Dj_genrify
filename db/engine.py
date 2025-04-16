from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class DatabaseEngine:
    def __init__(self, db_url: str):
        """Инициализация движка"""
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_base(self):
        """Создание базового класса для моделей"""
        return declarative_base()

    def get_session(self):
        """Получение новой сессии"""
        return self.Session()

    def create_tables(self, base):
        """Создание всех таблиц"""
        base.metadata.create_all(self.engine)
