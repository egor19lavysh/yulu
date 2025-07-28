from pydantic import BaseModel


class FirstTaskSchema(BaseModel):
    id: int
    chars: str
    correct_answer: str


class SecondTaskSchema(BaseModel):
    id: int
    text: str
    correct_answer: str


class WritingVariantListSchema(BaseModel):
    id: int


class WritingVariantSchema(WritingVariantListSchema):
    first_tasks: list[FirstTaskSchema]
    second_tasks: list[SecondTaskSchema]
