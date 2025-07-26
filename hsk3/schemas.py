from pydantic import BaseModel
from typing import List


class SentenceOption(BaseModel):
    id: int
    letter: str
    text: str


class ReadingQuestion(BaseModel):
    id: int
    text: str
    correct_letter: str


class ReadingTaskTypeOneSchema(BaseModel):
    id: int
    description: str
    sentence_options: List[SentenceOption]
    questions: List[ReadingQuestion]


class ReadingTaskTypeTwoSchema(BaseModel):
    id: int
    description: str
    sentence_options: List[SentenceOption]
    questions: List[ReadingQuestion]


class ReadingTaskTypeThreeSchema(BaseModel):
    id: int
    description: str
    text: str
    question: str
    sentence_options: List[SentenceOption]


class WritingTaskTypeOneSchema(BaseModel):
    id: int
    chars: str
    correct_sentence: str


class WritingTaskTypeTwoSchema(BaseModel):
    id: int
    sentence: str
    correct_char: str


# schemas.py (добавить к существующим схемам)
