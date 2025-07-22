from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Listening(Base):
    __tablename__ = "listening_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    audio_id: Mapped[str]


class FirstTask(Base):
    __tablename__ = "listening_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    questions: Mapped[list["FirstTaskQuestion"]] = relationship("FirstTaskQuestion", back_populates="task")


class FirstTaskQuestion(Base):
    __tablename__ = "listening_first_task_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("listening_first_tasks.id"))
    task = relationship("FirstTask", back_populates="questions")


class SecondTask(Base):
    __tablename__ = "listening_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    is_correct: Mapped[bool]


class ThirdTask(Base):
    __tablename__ = "listening_third_type_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    options = relationship("ListeningOption", back_populates="task")


class ListeningOption(Base):
    __tablename__ = "listening_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("listening_third_type_tasks.id"))
    task = relationship("ThirdTask", back_populates="options")
