from pydantic import BaseModel
from typing import List, Optional


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class FirstTaskQuestionSchema(Base):
    is_correct: bool


class FirstTaskSchema(Base):
    picture_id: str
    questions: list[FirstTaskQuestionSchema]


class SecondTaskQuestionSchema(Base):
    correct_letter: str


class SecondTaskSchema(Base):
    picture_id: str
    questions: list[SecondTaskQuestionSchema]


class ThirdTaskOptionSchema(Base):
    letter: str
    text: str


class ThirdTaskQuestionSchema(Base):
    correct_letter: str
    options: list[ThirdTaskOptionSchema]


class ThirdTaskSchema(Base):
    questions: list[ThirdTaskQuestionSchema]


class ListeningSchema(Base):
    audio_id: str