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
class ListeningSchema(BaseModel):
    id: int
    audio_id: str

    class Config:
        from_attributes = True

# Если у вас еще нет этих схем, добавьте их:
class FirstTaskQuestionSchema(BaseModel):
    id: int
    correct_letter: str

    class Config:
        from_attributes = True

class FirstTaskSchema(BaseModel):
    id: int
    picture_id: str
    questions: list[FirstTaskQuestionSchema]

    class Config:
        from_attributes = True

class SecondTaskSchema(BaseModel):
    id: int
    text: str
    is_correct: bool

    class Config:
        from_attributes = True

# ... (другие импорты и схемы)

class ThirdTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str

    class Config:
        from_attributes = True

class ThirdTaskQuestionSchema(BaseModel):
    id: int
    correct_letter: str
    options: list[ThirdTaskOptionSchema] # Список опций для конкретного вопроса

    class Config:
        from_attributes = True

class ThirdTaskSchema(BaseModel):
    id: int
    # ИЗМЕНЕНО: Поле должно называться "questions", как в модели SQLAlchemy
    questions: list[ThirdTaskQuestionSchema]

    class Config:
        from_attributes = True

# ... (остальные схемы)