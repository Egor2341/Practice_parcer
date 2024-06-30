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
    return templates.TemplateResponse("home.html", {"request": request})


count_of_pages = 0
c = 0
global_data = {}


@front_app.post("/list_of_vacancies/{todo}", response_class=HTMLResponse)
def list_of_vacancies(request: Request,
                      todo: str, next: str = Form(default=None),
                      prev: str = Form(default=None),
                      text: str = Form(default=""),
                      area: str = Form(default="Россия"),
                      salary: int = Form(default=None),
                      f_exp: str= Form(default=None),
                      empl_check: list= Form(default=None),
                      sch_check: list= Form(default=None)):
    global c, count_of_pages, global_data
    print(area)
    if todo == "all":
        params = {
            "text": text,
            "area": area,
            "salary": salary
        }
        print(params)
        data = requests.post("http://127.0.0.1:3000/vacancies", params).json()
        global_data = data

        if data["message"] == "OK":
            c = 0
            count_of_pages = len(data["items"]) // 20 if len(data["items"]) % 20 == 0 else len(data["items"]) // 20 + 1
    elif todo == "filter":
        c = 0
        print(f_exp)
        print(empl_check)
        print(sch_check)
    elif todo == "page":
        if next == ">":
            if c < count_of_pages - 1:
                c += 1
        if prev == "<":
            if c > 0:
                c -= 1

    return templates.TemplateResponse("list_of_vacancies.html", {"request": request, "data": global_data, "c": c,
                                                                 "count_of_pages": count_of_pages})
