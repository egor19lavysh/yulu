from pydantic import BaseModel


class Base(BaseModel):
    id: int

    class Config:
        from_attributes = True

class FirstTaskOptionSchema(Base):
    letter: str
    text: str


class FirstTaskSchema(Base):
    correct_letter: str
    options: list[FirstTaskOptionSchema]


class ListeningSchema(Base):
    audio_id: str