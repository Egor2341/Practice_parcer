import requests
from data.database import Base, engine
from service.db_service import database_is_empty
import json


def init():
    if database_is_empty():
        Base.metadata.create_all(engine)

    with open('file_areas.json', 'r') as file:
        if len(file.read()) != 0:
            return

    areas_data = json.loads(requests.get("https://api.hh.ru/areas").content.decode())
    areas = {"Россия": 113}
    for area in areas_data[0]['areas']:
        areas[area["name"]] = area["id"]
        cities = area["areas"]
        for city in cities:
            areas[city["name"]] = city["id"]

    with open("file_areas.json", "w") as file:
        json.dump(areas, file)




