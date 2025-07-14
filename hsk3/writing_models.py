from sqlalchemy.orm import Mapped, mapped_column, relationship, object_session
from database import Base


class WritingTaskTypeOne(Base):
    __tablename__ = "writing_tasks_type_one"

    id: Mapped[int] = mapped_column(primary_key=True)
    chars: Mapped[str]
    correct_sentence: Mapped[str]


class WritingTaskTypeTwo(Base):
    __tablename__ = "writing_tasks_type_two"

    id: Mapped[int] = mapped_column(primary_key=True)
    sentence: Mapped[str]
    correct_char: Mapped[str]
