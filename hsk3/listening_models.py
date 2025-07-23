from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Listening(Base):
    __tablename__ = "listening_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    audio_id: Mapped[str]

    first_type_tasks: Mapped[list["FirstTask"]] = relationship("FirstTask", back_populates="listening_var")
    second_type_tasks: Mapped[list["SecondTask"]] = relationship("SecondTask", back_populates="listening_var")
    third_type_tasks: Mapped[list["ThirdTask"]] = relationship("ThirdTask", back_populates="listening_var")


class FirstTask(Base):
    __tablename__ = "listening_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    questions: Mapped[list["FirstTaskQuestion"]] = relationship("FirstTaskQuestion", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("listening_tasks.id"))
    listening_var = relationship("Listening", back_populates="first_type_tasks")


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

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("listening_tasks.id"))
    listening_var = relationship("Listening", back_populates="second_type_tasks")


class ThirdTask(Base):
    __tablename__ = "listening_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    options = relationship("ThirdTaskOption", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("listening_tasks.id"))
    listening_var = relationship("Listening", back_populates="third_type_tasks")


class ThirdTaskOption(Base):
    __tablename__ = "listening_third_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("listening_third_tasks.id"))
    task = relationship("ThirdTask", back_populates="options")
