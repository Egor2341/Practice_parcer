import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

front_app = FastAPI()

script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
st_abs_file_path_templates = os.path.join(script_dir, "templates/")

front_app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")
templates = Jinja2Templates(directory=st_abs_file_path_templates)


@front_app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


@front_app.post("/list_of_vacancies/{todo}", response_class=HTMLResponse)
def list_of_vacancies(request: Request, text: str = Form(default=""), area: str = Form(default="Россия"),
                      salary: int = Form(default=None)):
    params = {
        "text": text,
        "area": area,
        "salary": salary
    }
    data = requests.post("http://127.0.0.1:3000/vacancies", json=params)
    print(data.json())
    return templates.TemplateResponse(request=request, name="list_of_vacancies.html")
