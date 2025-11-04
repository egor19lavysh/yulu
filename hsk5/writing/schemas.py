from pydantic import BaseModel


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class FirstTaskSchema(Base):
    correct_sentence: str
    words: str


class SecondTaskSchema(Base):
    text: str


class ThirdTaskSchema(Base):
    picture_id: str


class WritingSchema(Base):
    pass