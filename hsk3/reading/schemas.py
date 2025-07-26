from pydantic import BaseModel
from typing import List, Optional


# --- First Task Schemas ---
class FirstTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str


class FirstTaskQuestionSchema(BaseModel):
    id: int
    text: str
    correct_letter: str


class FirstTaskSchema(BaseModel):
    id: int
    options: List[FirstTaskOptionSchema]
    questions: List[FirstTaskQuestionSchema]


# --- Second Task Schemas ---
class SecondTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str


class SecondTaskQuestionSchema(BaseModel):
    id: int
    text: str
    correct_letter: str


class SecondTaskSchema(BaseModel):
    id: int
    options: List[SecondTaskOptionSchema]
    questions: List[SecondTaskQuestionSchema]


# --- Third Task Schemas ---
class ThirdTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str


class ThirdTaskSchema(BaseModel):
    id: int
    text: str
    correct_letter: str  # Предполагается, что это буква правильного варианта (A, B, C...)
    options: List[ThirdTaskOptionSchema]


# --- Reading Variant Schema ---
class ReadingVariantSchema(BaseModel):
    id: int
    first_tasks: List[FirstTaskSchema]
    second_tasks: List[SecondTaskSchema]
    third_tasks: List[ThirdTaskSchema]


