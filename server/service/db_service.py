from data.database  import session_factory, engine
from data.models import Vacancies
import sqlalchemy

def database_is_empty():
    return sqlalchemy.inspect(engine).get_table_names() == []

def get_vacancy_by_url(url):
    with session_factory() as session:
        return session.query(Vacancies).filter(Vacancies.url == url).first()

def add_vacancy(vacancy):
    with session_factory() as session:
        session.add(vacancy)
        session.commit()

def all_vacancies(urls):
    with session_factory() as session:
        return session.query(Vacancies).filter(Vacancies.url.in_(urls)).all()

def filter_vacancies(experience, employment, schedule, urls):
    with session_factory() as session:
        return session.query(Vacancies).filter(Vacancies.experience.in_(experience),
                                               Vacancies.employment.in_(employment),
                                               Vacancies.schedule.in_(schedule),
                                               Vacancies.url.in_(urls)).all()

