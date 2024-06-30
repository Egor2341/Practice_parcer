from pydantic import BaseModel
from typing import Optional

class Params(BaseModel):
    text: str
    area: str
    salary: Optional[int] = None
