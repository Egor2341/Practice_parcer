# from data.models import Vacancies
# from data.database import session_factory
#
# with session_factory() as session:
#     # experience = ["От 1 года до 3 лет", "От 3 до 6 лет", "Нет опыта", "Более 6 лет"]
#     # employment = ["Полная занятость", "Частичная занятость", "Стажировка", "Проектная работа", "Волонтерство"]
#     experience = ["От 1 года до 3 лет", "От 3 до 6 лет", "Нет опыта", "Более 6 лет"]
#     employment = ["Полная занятость",]
#     results = session.query(Vacancies).filter(Vacancies.experience.in_(experience), Vacancies.employment.in_(employment)).all()
#     for res in results:
#         print(res.experience, res.employment)
import json

import requests


def get_vacancies(text:str = "", area:str = "Россия", salary:int = None):
    page = 0
    while True:
        try:
            params = {
                "text": text,
                "area": 113,
                "salary": salary,
                "page": page,
                "per_page": 100
            }
        except:
            return {"urls": [], "message": "Неккоректный ввод"}

        response = requests.get("https://api.hh.ru/vacancies", params)
        if response.status_code != 200:
            return {"urls": [], "message": "Что-то пошло не так"}
        data = json.loads(response.content.decode())
        break
    return data


print(get_vacancies("разработчик"))

