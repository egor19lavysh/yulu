from pydantic import BaseModel
from typing import List, Optional


class FirstTaskSchema(BaseModel):
    id: int
    text: str
    is_correct: bool

    class Config:
        from_attributes = True


class SecondTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str
    task_id: int

    class Config:
        from_attributes = True


class SecondTaskSchema(BaseModel):
    id: int
    correct_letter: str
    options: List[SecondTaskOptionSchema]

    class Config:
        from_attributes = True


class ThirdTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str

    class Config:
        from_attributes = True


class ThirdTaskSchema(BaseModel):
    id: int
    correct_letter: str
    options: List[ThirdTaskOptionSchema]

    class Config:
        from_attributes = True


class ListeningSchema(BaseModel):
    id: int
    audio_id: str

    class Config:
        from_attributes = True
