from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from logger.my_logger import logger
from repository.models import Base, Person

# Создание локальной базы данных
engine = create_engine("sqlite:///example.db", echo=True)

# создаем таблицы
Base.metadata.create_all(bind=engine)

# создаем сессию подключения к бд. Добавляю данные пользователей в БД
# with Session(autoflush=False, bind=engine) as db:
#     # создаем объект Person для добавления в бд
#     daniil = Person(login="Daniil", password='1234')
#     alex = Person(login="Alex", password='4321')
#     db.add(daniil)  # добавляем в бд
#     db.add(alex)  # добавляем в бд
#     db.commit()  # сохраняем изменения
#     print(daniil.id)  # можно получить установленный id

db = Session(autoflush=False, bind=engine)

logger.info("Таблица базы данных готова")