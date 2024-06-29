from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text
from data.config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    pool_pre_ping=True
)


session_factory = sessionmaker(engine)

class Base(DeclarativeBase):
    pass