from pydantic import BaseModel


class FirstTaskQuestionSchema(BaseModel):
    id: int
    is_correct: bool

    class Config:
        from_attributes = True


class FirstTaskSchema(BaseModel):
    id: int
    picture_id: str
    questions: list[FirstTaskQuestionSchema]

    class Config:
        from_attributes = True


class SecondTaskQuestionSchema(BaseModel):
    id: int
    correct_letter: str

    class Config:
        from_attributes = True


class SecondTaskSchema(BaseModel):
    id: int
    picture_id: str
    questions: list[SecondTaskQuestionSchema]

    class Config:
        from_attributes = True


class ThirdTaskQuestionSchema(BaseModel):
    id: int
    correct_letter: str

    class Config:
        from_attributes = True


class ThirdTaskSchema(BaseModel):
    id: int
    picture_id: str
    questions: list[ThirdTaskQuestionSchema]

    class Config:
        from_attributes = True


class FourthTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str

    class Config:
        from_attributes = True


class FourthTaskQuestionSchema(BaseModel):
    id: int
    correct_letter: str
    options: list[FourthTaskOptionSchema]

    class Config:
        from_attributes = True


class FourthTaskSchema(BaseModel):
    id: int
    questions: list[FourthTaskQuestionSchema]

    class Config:
        from_attributes = True

class ListeningSchema(BaseModel):
    id: int
    audio_id: str

    class Config:
        from_attributes = True