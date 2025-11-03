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


class SecondTaskSentenceSchema(Base):
    text: str
    correct_letter: str


class SecondTaskOptionSchema(Base):
    letter: str
    text: str


class SecondTaskSchema(Base):
    options: list[SecondTaskOptionSchema]
    sentences: list[SecondTaskSentenceSchema]


class ThirdTaskSchema(Base):
    first_sentence: str
    second_sentence: str
    is_correct: bool


class FourthTaskQuestionSchema(Base):
    text: str
    correct_letter: str


class FourthTaskOptionSchema(Base):
    letter: str
    text: str


class FourthTaskSchema(Base):
    options: list[FourthTaskOptionSchema]
    questions: list[FourthTaskQuestionSchema]


class ReadingVariantSchema(Base):
    pass