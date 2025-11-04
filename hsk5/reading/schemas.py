from pydantic import BaseModel


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class FirstTaskQuestionOptionSchema(Base):
    letter: str
    text: str


class FirstTaskQuestionSchema(Base):
    text: str
    correct_letter: str
    options: list[FirstTaskQuestionOptionSchema]


class FirstTaskSchema(Base):
    text: str
    questions: list[FirstTaskQuestionSchema]


class SecondTaskOptionSchema(Base):
    letter: str
    text: str


class SecondTaskSchema(Base):
    text: str
    correct_letter: str
    options: list[SecondTaskOptionSchema]


class ThirdTaskQuestionOptionSchema(Base):
    letter: str
    text: str


class ThirdTaskQuestionSchema(Base):
    text: str
    correct_letter: str
    options: list[ThirdTaskQuestionOptionSchema]


class ThirdTaskSchema(Base):
    photo_id: str | None
    text: str
    questions: list[ThirdTaskQuestionSchema]

class ReadingVariantSchema(Base):
    pass