from pydantic import BaseModel


class FirstTaskOptionSchema(BaseModel):
    id: int
    is_correct: bool

    class Config:
        from_attributes = True


class FirstTaskSchema(BaseModel):
    id: int
    picture_id: str
    options: list[FirstTaskOptionSchema]

    class Config:
        from_attributes = True


class SecondTaskSentenceSchema(BaseModel):
    id: int
    text: str
    correct_letter: str

    class Config:
        from_attributes = True


class SecondTaskSchema(BaseModel):
    id: int
    picture_id: str
    sentences: list[SecondTaskSentenceSchema]

    class Config:
        from_attributes = True


class ThirdTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str

    class Config:
        from_attributes = True


class ThirdTaskSentenceSchema(BaseModel):
    id: int
    text: str
    correct_letter: str

    class Config:
        from_attributes = True


class ThirdTaskSchema(BaseModel):
    id: int
    options: list[ThirdTaskOptionSchema]
    sentences: list[ThirdTaskSentenceSchema]

    class Config:
        from_attributes = True


class FourthTaskOptionSchema(BaseModel):
    id: int
    letter: str
    text: str

    class Config:
        from_attributes = True


class FourthTaskSentenceSchema(BaseModel):
    id: int
    text: str
    correct_letter: str

    class Config:
        from_attributes = True


class FourthTaskSchema(BaseModel):
    id: int
    options: list[FourthTaskOptionSchema]
    sentences: list[FourthTaskSentenceSchema]

    class Config:
        from_attributes = True

class ReadingVariantSchema(BaseModel):
    id: int
