from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Integer, String

# создаем модель, объекты которой будут храниться в бд
class Base(DeclarativeBase): pass

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    password = Column(String)

class Video(Base):
    __tablename__ = "video_detected"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    video_path_origin = Column(String)
    video_path_detected = Column(String)
    author = Column(String)

