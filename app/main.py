from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from repository.sqlite import db, Person
from sqlalchemy.orm import Session
from fastapi import FastAPI, Request, UploadFile, File, Form, status, Depends, Response, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from itsdangerous import URLSafeSerializer
import numpy as np
import cv2

from logger.my_logger import logger
import uvicorn
import re

from models.models import VideoModel

logger.info("Start logging")

app = FastAPI()
templates = Jinja2Templates(directory="../templates")

# Сохраняю в переменную данные о пользователей из БД
users = db.query(Person).all()

# Секретный ключ для подписи cookies
SECRET_KEY = "your-secret-key"
serializer = URLSafeSerializer(SECRET_KEY)

# Базовый пример аутентификации
security = HTTPBasic()

@app.get("/login", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...) , response: Response = None):
    # Проверяем, существует ли пользователь в базе данных
    for user in users:
        print(username)
        print(password)
        if user.login == username and user.password == password:
            # Создаем сессию (подписанный токен)
            session_token = serializer.dumps({"username": username})
            response.set_cookie(key="session_token", value=session_token, httponly=True)


            return RedirectResponse('/load_data_local', status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("login.html", {
        "request": request,
        'info': 'Incorrect username or password',
    })





# Маршрут для выхода пользователя
@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="session_token")
    return {"message": "Logout successful"}


@app.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.get("/main", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

# -------------------- Загрузка локального файла --------------------
@app.get("/load_data_local", response_class=HTMLResponse)
async def load_data_local(request: Request, msg: str = None):
    logger.info('Отображение страницы с формой')
    return templates.TemplateResponse("load_data_local.html", {
        "request": request,
        "info": msg,
    })

@app.post("/fetch_data_local")
async def fetch_data_local(request: Request,
                           file: UploadFile = File(...),
                           check_filename: bool = Form(default=False)):


    if check_filename:
        try:
            if not bool(re.search(r"\.mp4", file.filename)):
                raise ValueError('Необходимо загрузить файл в формате mp4')
        except Exception as error:
            redirect_url = request.url_for('load_data_local').include_query_params(msg=error)
            return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

    try:
        contents = await file.read()
        img_array = np.asarray(bytearray(contents), dtype=np.uint8)
        im = cv2.imdecode(img_array, 0)
        # tst = cv2.VideoCapture
        # cv2.imshow("test", im)
        # cv2.waitKey()

        with open('test2.mp4', 'wb') as f:
            f.write(contents)



        # cap = cv2.VideoCapture(0)
        # # Define the codec and create VideoWriter object
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # out = cv2.VideoWriter('../tmp/output.mp4', fourcc, 20.0, (640, 480))
        # # write the flipped frame
        # out.write(im)

        # while (cap.isOpened()):
        #     ret, frame = cap.read()
        #     if ret == True:
        #         frame = cv2.flip(frame, 0)
        #
        #         # write the flipped frame
        #         out.write(frame)
        #
        #         cv2.imshow('frame', frame)
        #         if cv2.waitKey(1) & 0xFF == ord('q'):
        #             break
        #     else:
        #         break
        # # Release everything if job is finished
        # cap.release()
        # out.release()
        # cv2.destroyAllWindows()

    finally:
        await file.close()

    # with engine.connect() as conn:
    #     # Выполняем параметризированный запрос
    #     query_str = f"SELECT * FROM mytable WHERE {column} LIKE :val"
    #     result = conn.execute(text(query_str), {"val": f"%{value}%"})
    #
    #     columns = result.keys()       # берем названия столбцов
    #     rows = result.fetchall()      # берем все строки

    # try:
    #     contents = await data.file.read()
    #     # Проверка файла на формат mp4
    #     match = re.fullmatch("\S.mp4", data.file.filename)
    #     # logger.info(f'загружаемый файл соответсвует mp4 - {match}')
    #     if not match:
    #         error = 'Прошу загрузить файл в формате mp4'
    #         # return RedirectResponse("/load_data_local", 302,  )
    #         return templates.TemplateResponse("load_data_local.html", {
    #             "request": request,
    #             "error": error,
    #         })
    #     # df.to_sql("mytable", con=engine, if_exists="replace", index=False)
    # except Exception as e:
    #     logger.error(e)
    # finally:
    #     await data.file.close()

    redirect_url = request.url_for('load_data_local').include_query_params(msg='Файл успешно сохранен')
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)



# test = CascadeHaara('classifier/haarcascade_frontalface_alt.xml')
# test.load_image('image_for_test/face1.jpg')
# test.return_result()


if __name__== "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8080)

