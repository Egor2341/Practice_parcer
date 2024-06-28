import json
import requests
from data.database import session_factory
from data.models import Vacancies
import time
import re
from data.orm import create_tables
from fastapi import FastAPI

app = FastAPI()

areas_data = json.loads(requests.get("https://api.hh.ru/areas").content.decode())
areas = {"Россия": 113}
for area in areas_data[0]['areas']:
    areas[area["name"]] = area["id"]


def get_vacancies(text, area):
    page = 0
    cur_urls = []
    while True:
        params = {
            "text": text,
            "area": areas[area],
            "page": page,
            "per_page": 100
        }
        response = requests.get("https://api.hh.ru/vacancies", params)
        if response.status_code != 200:
            return {"message": "Что-то пошло не так"}
        data = json.loads(response.content.decode())

        # if page == data["pages"] - 1:
        if page == 2:
            break

        for item in data["items"]:
            cur_urls.append(item["alternate_url"])
            pattern = re.compile('<.*?>')
            with session_factory() as session:
                if session.query(Vacancies).filter(Vacancies.url == item["alternate_url"]).first():
                    continue

                vacancy = Vacancies(name=item["name"], url=item["alternate_url"])
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
                    vacancy.salary = res.capitalize()
                    res += item["salary"]["currency"]
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

                vac_url = requests.get(item["url"])
                if vac_url.status_code != 200:
                    return {"message": "Что-то пошло не так"}
                vac_url_data = json.loads(vac_url.content.decode())

                if vac_url_data["key_skills"] != []:
                    skills = vac_url_data["key_skills"]
                    key_skills = ''
                    for skill in skills:
                        key_skills += f'{skill["name"]} '

                    vacancy.key_skills = key_skills
                else:
                    vacancy.key_skills = "Не указано"

                session.add(vacancy)
                session.commit()

        page += 1
        time.sleep(1)

        return cur_urls

@app.get("/vacancies")
def vacancies(text, area):
    urls = get_vacancies(text, area)

    return


# get_vacancies("разработчик", "Россия")
# create_tables()

