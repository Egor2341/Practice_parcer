# import requests
#
# params = {
#     "text": "разработчик",
#     "area": "Москва",
#     "salary": 50000
# }
# res = requests.get("http://127.0.0.1:3000/vacancies")
# urls = []
# for i in res.json()["items"]:
#     urls.append(i["url"])
# urls = "', '".join(urls)
# urls = "['" + urls + "']"
# print(urls)

from server.data.models import Vacancies
item = {"area": {"name": "fadfa"}, "employer": {"name": "fasdfadasf"}}
vacancy = Vacancies
fields = ["area", "employer", "experience", "employment", "schedule"]  # поля, которые обрабатываются одинаково
vac_fields = [vacancy.area, vacancy.employer, vacancy.experience,
              vacancy.employment, vacancy.schedule]
for i in range(len(fields)):
    if item[fields[i]]:
        vac_fields[i] = item[fields[i]]
    else:
        vac_fields[i] = "Не указано"
print(vacancy.employer)
print(vacancy.schedule)
