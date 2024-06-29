from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from data.config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    pool_pre_ping=True
)


session_factory = sessionmaker(engine)

class Base(DeclarativeBase):
    pass