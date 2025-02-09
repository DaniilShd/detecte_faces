from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from logger.my_logger import logger
from repository.models import Base, Video, Person

import sys
import os

# Получаем абсолютный путь к корневой папке проекта
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Указываем путь к базе данных
db_path = os.path.join(base_dir, 'app', 'example.db')

# Создаем движок SQLAlchemy
engine = create_engine(f'sqlite:///{db_path}')

# создаем таблицы
Base.metadata.create_all(bind=engine)

# создаем сессию подключения к бд. Добавляю данные пользователей в БД
with Session(autoflush=False, bind=engine) as db:
    # создаем объект Person для добавления в бд
    daniil = Person(login="Daniil", password='1234')
    alex = Person(login="Alex", password='4321')
    db.add(daniil)  # добавляем в бд
    db.add(alex)  # добавляем в бд
    db.commit()  # сохраняем изменения
    print(daniil.id)  # можно получить установленный id

logger.info("Таблица базы данных готова")