from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from fastapi import FastAPI, Request, UploadFile, File, Form, status

from models.models import VideoModel
from logger.my_logger import logger
import uvicorn
import re
import aiofiles
import httpx

from models.models import VideoModel


logger.info("Start logging")

app = FastAPI()
templates = Jinja2Templates(directory="../templates")

# Создание локальной базы данных
engine = create_engine("sqlite:///example.db", echo=True)

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
                           name: str = Form(...),
                           check_filename: bool = Form(default=False)):

    if check_filename:
        try:
            pattern = re.compile('.*\.mp4')
            if not pattern.search(file.filename):
                raise ValueError('Необходимо загрузить файл в формате mp4')
        except Exception as error:
            logger.error(error)
            msg="Необходимо загрузить файл mp4"

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

    redirect_url = request.url_for('load_data_local').include_query_params(msg=msg)
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)



# test = CascadeHaara('classifier/haarcascade_frontalface_alt.xml')
# test.load_image('image_for_test/face1.jpg')
# test.return_result()


if __name__== "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8080)

