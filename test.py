import requests

params = {
    "text": "разработчик",
    "area": "Москва",
    "salary": 50000
}
res = requests.get("http://127.0.0.1:3000/vacancies")
urls = []
for i in res.json()["items"]:
    urls.append(i["url"])
urls = "', '".join(urls)
urls = "['" + urls + "']"
print(urls)