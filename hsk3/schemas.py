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


class ListeningPictureSchema(BaseModel):
    id: int
    picture_id: str
    letter: str


class FirstTaskQuestionSchema(BaseModel):
    id: int
    correct_letter: str


class FirstTaskSchema(BaseModel):
    id: int
    picture_id: str
    questions: list[FirstTaskQuestionSchema]


class SecondTaskSchema(BaseModel):
    id: int
    text: str
    is_correct: bool
