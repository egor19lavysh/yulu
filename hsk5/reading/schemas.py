from pydantic import BaseModel


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class FirstTaskOptionSchema(Base):
    letter: str
    text: str


class FirstTaskSchema(Base):
    text: str
    correct_letter: str
    options: list[FirstTaskOptionSchema]


class SecondTaskOptionSchema(Base):
    letter: str
    text: str


class SecondTaskSchema(Base):
    text: str
    correct_letter: str
    options: list[SecondTaskOptionSchema]


class QuestionOptionSchema(Base):
    letter: str
    text: str


class ThirdTaskQuestionSchema(Base):
    text: str
    correct_letter: str
    options: list[QuestionOptionSchema]


class ThirdTaskSchema(Base):
    text: str
    questions: list[ThirdTaskQuestionSchema]

class ReadingVariantSchema(Base):
    pass