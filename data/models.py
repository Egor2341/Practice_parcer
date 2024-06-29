from data.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Vacancies(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    employer: Mapped[str]
    salary: Mapped[str]
    area: Mapped[str]
    url: Mapped[str] = mapped_column(nullable=False, unique=True)
    requirement: Mapped[str]
    responsibility: Mapped[str]
    experience: Mapped[str]
    employment: Mapped[str]
    key_skills: Mapped[str]


