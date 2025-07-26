from pydantic import BaseModel


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


class ThirdTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str

    class Config:
        from_attributes = True


class ThirdTaskQuestionSchema(BaseModel):
    id: int
    correct_letter: str
    options: list[ThirdTaskOptionSchema]

    class Config:
        from_attributes = True


class ThirdTaskSchema(BaseModel):
    id: int
    # ИЗМЕНЕНО: Поле должно называться "questions", как в модели SQLAlchemy
    questions: list[ThirdTaskQuestionSchema]

    class Config:
        from_attributes = True
