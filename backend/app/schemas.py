# Pydantic models for the request and response bodies of the API

from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime, date
from typing import Optional


class TextInput(BaseModel):
    text: str

class ExamOut(BaseModel): # (exam.py) response model for the create_exam and get_exam
    #id: int
    name: str
    #created_at: datetime
    table_name: str

    class Config:
        orm_mode = True    


class ExamsView(BaseModel): # (view.py) response model for the view_exams
    name: str
    date: date
    max_marks: int
    avg_marks: Optional[int]
    contestants: Optional[int]
    qstn_count: Optional[int]

    class Config:
        orm_mode = True        