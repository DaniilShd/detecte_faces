import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
from detecte_faces.video_processing import detected_faces
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from repository.models import Video, Person
from repository.sqlite import engine
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import FastAPI, Request, UploadFile, File, Form, status, Response, HTTPException, Cookie
from fastapi.security import HTTPBasic
from itsdangerous import URLSafeSerializer
from logger.my_logger import logger
import pandas as pd
import uvicorn
import re

from models.models import VideoModel

logger.info("Start logging")

app = FastAPI()
templates = Jinja2Templates(directory="../templates")

# Сохраняю в переменную данные о пользователей из БД
with Session(autoflush=False, bind=engine) as db:
    users = db.query(Person).all()

# Секретный ключ для подписи cookies
SECRET_KEY = "your-secret-key"
serializer = URLSafeSerializer(SECRET_KEY)

lst_tokens=[]  # список токенов пользователей

# Базовый пример аутентификации
security = HTTPBasic()

@app.get("/", response_class=HTMLResponse)
async def path_to_login(request: Request):
    return RedirectResponse('/login', status_code=status.HTTP_302_FOUND)

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...) , response: Response = None):
    # Проверяем, существует ли пользователь в базе данных
    for user in users:
        if user.login == username and user.password == password:
            # Создаем сессию (подписанный токен)
            session_token = serializer.dumps({"username": username})
            response.set_cookie(key="session_token", value=session_token, httponly=True)
            lst_tokens.append(session_token)  # добавляем в список новый токен

            return RedirectResponse('/show_data', status_code=status.HTTP_301_MOVED_PERMANENTLY, headers=response.headers)

    return templates.TemplateResponse("login.html", {
        "request": request,
        'info': 'Incorrect username or password',
    })

# Маршрут для выхода пользователя
@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="session_token")
    return RedirectResponse('/login', status_code=status.HTTP_301_MOVED_PERMANENTLY, headers=response.headers)

@app.get("/show_data", response_class=HTMLResponse)
def show_data(request: Request,
              session_token: str = Cookie(None)):
    if session_token not in lst_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    with Session(autoflush=False, bind=engine) as db:
        data = db.execute(text("SELECT * FROM video_detected"))
        columns = data.keys()
        rows = data.fetchall()  # получаем данные
    df = pd.DataFrame(rows, columns=columns)
    print(df.to_dict(orient="records"))
    print(list(df.columns))

    return templates.TemplateResponse(
        "table.html",
        {
            "request": request,
            "data": df.to_dict(orient="records"),
            "cols": list(df.columns),
        }
    )

# -------------------- Загрузка локального файла --------------------
@app.get("/load_data_local", response_class=HTMLResponse)
async def load_data_local(request: Request, msg: str = None,
                          session_token: str = Cookie(None)):
    if session_token not in lst_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    logger.info('Отображение страницы с формой')
    return templates.TemplateResponse("load_data_local.html", {
        "request": request,
        "info": msg,
    })

@app.post("/fetch_data_local")
async def fetch_data_local(request: Request,
                           file: UploadFile = File(...),
                           session_token: str = Cookie(...)):

    if session_token not in lst_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    # Расшифровываем токен сессии
    data = serializer.loads(session_token)
    username = data["username"]

    if file.filename != "":
        try:
            if not bool(re.search(r"\.mp4", file.filename)):
                raise ValueError('Необходимо загрузить файл в формате mp4')
        except Exception as error:
            redirect_url = request.url_for('load_data_local').include_query_params(msg=error)
            return RedirectResponse(redirect_url, status_code=status.HTTP_301_MOVED_PERMANENTLY)
    else:
        return templates.TemplateResponse("load_data_local.html", {
            "request": request,
            "info": "Пустой файл",
        })

    try:
        contents = await file.read()

        # Создаю уникальное название для видеофайла
        uniq_name_video = f'{uuid.uuid4()}.mp4'

        # Записываю файл в mp4 формат
        with open(f'../repository/origin_video/{uniq_name_video}.mp4', 'wb') as f:
            f.write(contents)

        detected_faces(video_path=f'../repository/origin_video/{uniq_name_video}.mp4',
                       output_path=f'../repository/detected_video/{uniq_name_video}.mp4',
                       every=5,
                       chunk_size=1000)

        # Сохранение в базе данных пути к файлам и имя автора
        with Session(autoflush=False, bind=engine) as db:
            # создаем объект Video для добавления в бд
            new_video = Video(video_path_origin=f"/repository/origin_video/{uniq_name_video}.mp4",
                              video_path_detected=f"/repository/detected_video/{uniq_name_video}.mp4",
                              author=username)
            db.add(new_video)  # добавляем в бд
            db.commit()  # сохраняем изменения
    finally:
        await file.close()

    redirect_url = request.url_for('load_data_local').include_query_params(msg='Файл успешно сохранен')
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)


if __name__== "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8080)

