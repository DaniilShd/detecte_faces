import httpx
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from fastapi import FastAPI, Request, UploadFile, File, Query
from io import BytesIO
from io import StringIO

from detecte_faces.detecte import CascadeHaara
from models.models import VideoModel



app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
async def load_data_local(request: Request):
    return templates.TemplateResponse("load_data_local.html", {"request": request})

@app.post("/fetch_data_local")
async def fetch_data_local(video_file: UploadFile = File(...)):
    try:
        contents = await video_file.read()

        video = VideoModel(name="test")

        print(video.model_dump())


        # df = pd.read_csv(BytesIO(contents))
        #
        # df.dropna(inplace=True)
        # df.drop_duplicates(inplace=True)
        #
        # df.to_sql("mytable", con=engine, if_exists="replace", index=False)
        # return {
        #     "status": "ok",
        #     "file_name": file.filename,
        #     "rows_loaded": len(df),
        #     "columns": list(df.columns),
        # }
    except Exception as e:
        return {"status": "error", "details": str(e)}



# test = CascadeHaara('classifier/haarcascade_frontalface_alt.xml')
# test.load_image('image_for_test/face1.jpg')
# test.return_result()




