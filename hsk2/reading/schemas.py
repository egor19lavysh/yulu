from pydantic import BaseModel
from typing import Optional


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class FirstTaskSentenceSchema(Base):
    text: str
    correct_letter: str


class FirstTaskSchema(Base):
    picture_id: str
    sentences: list[FirstTaskSentenceSchema]


class SecondTaskQuestionSchema(Base):
    text: str
    correct_letter: str


class SecondTaskOptionSchema(Base):
    correct_letter: str
    text: str


class SecondTaskSchema(Base):
    options: list[SecondTaskOptionSchema]
    qustions: list[SecondTaskQuestionSchema]


class ThirdTaskSchema(Base):
    text: str
    is_correct: bool


class FourthTaskQuestionSchema(Base):
    text: str
    correct_letter: str


class FourthTaskOptionSchema(Base):
    letter: str
    text: str


class FourthTaskSchema(Base):
    options: list[SecondTaskOptionSchema]
    qustions: list[SecondTaskQuestionSchema]


class ReadingVariantSchema(Base):
    pass