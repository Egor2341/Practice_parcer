from data.models import Vacancies
from data.database import session_factory

with session_factory() as session:
    # experience = ["От 1 года до 3 лет", "От 3 до 6 лет", "Нет опыта", "Более 6 лет"]
    # employment = ["Полная занятость", "Частичная занятость", "Стажировка", "Проектная работа", "Волонтерство"]
    experience = ["От 1 года до 3 лет", "От 3 до 6 лет", "Нет опыта", "Более 6 лет"]
    employment = ["Полная занятость",]
    results = session.query(Vacancies).filter(Vacancies.experience.in_(experience), Vacancies.employment.in_(employment)).all()
    for res in results:
        print(res.experience, res.employment)