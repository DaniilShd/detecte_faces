import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory="../templates")

@app.get("/main", response_class=HTMLResponse)
async def main_template(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})