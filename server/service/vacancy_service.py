import re
import requests
import json
import service.db_service as db_service
from data.models import Vacancies
import time


def get_urls(text: str = "", area: str = "Россия", salary: int = None):
    with open('file_areas.json', 'r') as file:
        areas = json.load(file)
    page = 0
    cur_urls = []
    pattern = re.compile('<.*?>')

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
            return {"urls": [], "message": "Некорректный ввод"}

        try:
            response = requests.get("https://api.hh.ru/vacancies", params=params)
        except:
            return {"urls": [], "message": "Что-то пошло не так"}

        if response.status_code != 200:
            return {"urls": [], "message": "Что-то пошло не так"}

        data = json.loads(response.content.decode())
        if not data["items"]:
            return {"urls": [], "message": "По данному запросу ничего не найдено"}

        if page == 1 or page == data["pages"]:
            break

        for item in data["items"]:
            cur_urls.append(item["alternate_url"])
            if db_service.get_vacancy_by_url(item["alternate_url"]):
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
                vacancy.key_skills = "Не указано"
            else:
                vac_url_data = json.loads(vac_url.content.decode())

                if vac_url_data["key_skills"] != []:
                    skills = vac_url_data["key_skills"]
                    key_skills = []
                    for skill in skills:
                        key_skills.append(skill["name"])
                    vacancy.key_skills = ", ".join(key_skills)
                else:
                    vacancy.key_skills = "Не указано"

            db_service.add_vacancy(vacancy)
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
