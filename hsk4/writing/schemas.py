from pydantic import BaseModel


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True


class WritingVarSchema(Base):
    pass


class TaskWordSchema(Base):
    text: str


class FirstTaskSchema(Base):
    correct_sentence: str
    words: str


class SecondTaskSchema(Base):
    picture_id: str
    words: list[TaskWordSchema]
