from data.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class Vacancies(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    employer: Mapped[Optional[str]]
    salary: Mapped[Optional[str]]
    url: Mapped[str] = mapped_column(nullable=False, unique=True)
    requirement: Mapped[Optional[str]]
    responsibility: Mapped[Optional[str]]
    experience: Mapped[Optional[str]]
    employment: Mapped[Optional[str]]
    key_skills: Mapped[Optional[str]]

