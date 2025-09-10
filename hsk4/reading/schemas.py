from pydantic import BaseModel


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class FirstTaskOptionSchema(Base):
    letter: str
    text: str


class FirstTaskSentenceSchema(Base):
    correct_letter: str
    text: str


class FirstTaskSchema(Base):
    options: list[FirstTaskOptionSchema]
    sentences: list[FirstTaskSentenceSchema]


class SecondTaskOptionSchema(Base):
    letter: str
    text: str


class SecondTaskSchema(Base):
    correct_sequence: str
    options: list[SecondTaskOptionSchema]


class QuestionOptionSchema(Base):
    letter: str
    text: str


class ThirdTaskQuestion(Base):
    text: str
    correct_letter: str
    options: list[QuestionOptionSchema]


class ThirdTask(Base):
    text: str
    questions: list[ThirdTaskQuestion]
