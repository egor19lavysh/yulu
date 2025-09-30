from pydantic import BaseModel


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class FirstTaskSchema(Base):
    correct_sentence: str
    words: str


class SecondTaskSchema(Base):
    pass


class WritingSchema(Base):
    pass