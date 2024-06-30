# from data.models import Vacancies
# from data.database import session_factory
#
# with session_factory() as session:
#     experience = ["От 1 года до 3 лет"]
#     employment = ["Полная занятость"]
#     schedule = ["Полный день"]
#     # experience = ["От 1 года до 3 лет"]
#     # schedule = ["Полный день", "Удаленная работа", "Гибкий график", "Сменный график", "Вахтовый метод"]
#     # employment = ["Полная занятость", "Частичная занятость", "Стажировка", "Проектная работа", "Волонтерство"]
#     results = session.query(Vacancies).filter(Vacancies.experience.in_(experience),
#                                                   Vacancies.employment.in_(employment),
#                                                   Vacancies.schedule.in_(schedule)).all()
#     for res in results:
#         print(res.experience, res.employment, res.schedule)


a = []
sa = set(a)
b = [1, 4, 5]
sb = set(b)
c = []
sc = set(c)
d = [2, 4, 6]
sd = set(d)
res = list(sb & sd)
r = []
r += b
print(r)
print(res)