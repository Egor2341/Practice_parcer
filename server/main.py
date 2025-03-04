from typing import Annotated, Union
from fastapi import FastAPI, Query
from __init__ import init
from service import db_service, vacancy_service

app = FastAPI()
init()

@app.get("/vacancies")
def vacancies(text: str = "", area: str = "Россия", salary: int = None):
    parse_vacs = vacancy_service.get_urls(text, area, salary)
    if parse_vacs["message"] != "OK":
        return {"items": [], "message": parse_vacs["message"]}
    return vacancy_service.list_vacs_to_dict(db_service.all_vacancies(parse_vacs["urls"]))


@app.get("/filters")
def filters(exp: str = "Не имеет значения",
            empl: Annotated[Union[list[str], None], Query()] = None,
            sch: Annotated[Union[list[str], None], Query()] = None,
            urls: Annotated[Union[list[str], None], Query()] = None):
    if not urls:
        return {"items": [], "message": "Ничего не найдено"}
    if exp == "Не имеет значения":
        experience = ["От 1 года до 3 лет", "От 3 до 6 лет", "Нет опыта", "Более 6 лет"]
    else:
        experience = [exp]
    if not empl:
        employment = ["Полная занятость", "Частичная занятость", "Стажировка", "Проектная работа", "Волонтерство"]
    else:
        employment = empl
    if not sch:
        schedule = ["Полный день", "Удаленная работа", "Гибкий график", "Сменный график", "Вахтовый метод"]
    else:
        schedule = sch
    return vacancy_service.list_vacs_to_dict(db_service.filter_vacancies(experience, employment,
                                                                         schedule, urls))