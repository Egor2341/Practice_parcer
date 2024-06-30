import json
from typing import Annotated, Union

import requests
from data.database import session_factory
from data.models import Vacancies
import time
import re
from data.orm import create_tables
from fastapi import FastAPI, Query

app = FastAPI()

areas_data = json.loads(requests.get("https://api.hh.ru/areas").content.decode())
areas = {"Россия": 113}
for area in areas_data[0]['areas']:
    areas[area["name"]] = area["id"]
    cities = area["areas"]
    for city in cities:
        areas[city["name"]] = city["id"]


def get_vacancies(text: str = "", area: str = "Россия", salary: int = None):
    page = 0
    cur_urls = []
    while True:
        try:
            params = {
                "text": text,
                "area": areas[area.lower().capitalize()],
                "salary": salary,
                "page": page,
                "per_page": 100
            }
        except:
            return {"urls": [], "message": "Неккоректный ввод"}

        response = requests.get("https://api.hh.ru/vacancies", params=params)
        if response.status_code != 200:
            return {"urls": [], "message": "Что-то пошло не так"}
        data = json.loads(response.content.decode())

        # if page == data["pages"] - 1:
        if page == 1:
            break
        for item in data["items"]:
            cur_urls.append(item["alternate_url"])
            pattern = re.compile('<.*?>')
            with session_factory() as session:
                if session.query(Vacancies).filter(Vacancies.url == item["alternate_url"]).first():
                    continue

                vacancy = Vacancies(name=item["name"], url=item["alternate_url"])
                if item["area"]:
                    vacancy.area = item["area"]["name"]
                else:
                    vacancy.area = "Не указано"
                if item["employer"]:
                    vacancy.employer = item["employer"]["name"]
                else:
                    vacancy.employer = "Не указано"

                if item["salary"]:
                    res = ''
                    if item["salary"]["from"]:
                        res += f"от {item['salary']['from']} "
                    if item["salary"]["to"]:
                        res += f"до {item['salary']['to']} "
                    res = res.capitalize()
                    res += item["salary"]["currency"].upper()
                    vacancy.salary = res
                else:
                    vacancy.salary = "Не указано"

                if item["snippet"]:
                    if item["snippet"]["requirement"]:
                        vacancy.requirement = re.sub(pattern, '', item["snippet"]["requirement"])
                    else:
                        vacancy.requirement = "Не указано"
                    if item["snippet"]["responsibility"]:
                        vacancy.responsibility = re.sub(pattern, '', item["snippet"]["responsibility"])
                    else:
                        vacancy.responsibility = "Не указано"
                else:
                    vacancy.requirement = "Не указано"
                    vacancy.responsibility = "Не указано"

                if item["experience"]:
                    vacancy.experience = item["experience"]["name"]
                else:
                    vacancy.experience = "Не указано"

                if item["employment"]:
                    vacancy.employment = item["employment"]["name"]
                else:
                    vacancy.employment = "Не указано"

                if item["schedule"]:
                    vacancy.schedule = item["schedule"]["name"]
                else:
                    vacancy.schedule = "Не указано"

                vac_url = requests.get(item["url"])
                if vac_url.status_code != 200:
                    return {"urls": [], "message": "Что-то пошло не так"}
                vac_url_data = json.loads(vac_url.content.decode())

                if vac_url_data["key_skills"] != []:
                    skills = vac_url_data["key_skills"]
                    key_skills = []
                    for skill in skills:
                        key_skills.append(skill["name"])

                    vacancy.key_skills = ", ".join(key_skills)
                else:
                    vacancy.key_skills = "Не указано"

                session.add(vacancy)
                session.commit()

        page += 1
        time.sleep(1)

        return {"urls": cur_urls, "message": "OK"}


def list_vacs_to_dict(vacs: list = None):
    res_vacs = {"items": []}
    try:
        for vac in vacs:
            res_vacs["items"].append(
                {
                    "name": vac.name,
                    "employer": vac.employer,
                    "salary": vac.salary,
                    "area": vac.area,
                    "url": vac.url,
                    "requirement": vac.requirement,
                    "responsibility": vac.responsibility,
                    "experience": vac.experience,
                    "employment": vac.employment,
                    "schedule": vac.schedule,
                    "key_skills": vac.key_skills
                }
            )
        if res_vacs["items"]:
            res_vacs["message"] = "OK"
        else:
            res_vacs["message"] = "По данному запросу ничего не найдено"
        return res_vacs
    except:
        res_vacs["message"] = "Что-то пошло не так"
        return res_vacs



@app.get("/vacancies")
def vacancies(text: str = "", area: str = "Россия", salary: int = None):
    parse_vacs = get_vacancies(text, area, salary)
    if parse_vacs["message"] != "OK":
        return {"items": [], "message": parse_vacs["message"]}
    with session_factory() as session:
        vacs = session.query(Vacancies).filter(Vacancies.url.in_(parse_vacs["urls"])).all()
        return list_vacs_to_dict(vacs)

@app.get("/filters")
def filters(exp: str = "Не имеет значения",
            empl: Annotated[Union[list[str], None], Query()] = None,
            sch: Annotated[Union[list[str], None], Query()] = None,
            urls: Annotated[Union[list[str], None], Query()] = None):
    print(urls)
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
    with session_factory() as session:
        vacs = session.query(Vacancies).filter(Vacancies.experience.in_(experience),
                                                  Vacancies.employment.in_(employment),
                                                  Vacancies.schedule.in_(schedule),
                                                  Vacancies.url.in_(urls)).all()
    return list_vacs_to_dict(vacs)

# create_tables()
