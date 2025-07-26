from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Reading(Base):
    __tablename__ = "reading_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_tasks: Mapped[list["ReadingFirstTask"]] = relationship("ReadingFirstTask", back_populates="reading_var") # Изменено
    second_tasks: Mapped[list["ReadingSecondTask"]] = relationship("ReadingSecondTask", back_populates="reading_var") # Изменено
    third_tasks: Mapped[list["ReadingThirdTask"]] = relationship("ReadingThirdTask", back_populates="reading_var") # Изменено


class ReadingFirstTask(Base): # Изменено
    __tablename__ = "reading_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    options: Mapped[list["ReadingFirstTaskOption"]] = relationship("ReadingFirstTaskOption", back_populates="task") # Изменено
    questions: Mapped[list["ReadingFirstTaskQuestion"]] = relationship("ReadingFirstTaskQuestion", back_populates="task") # Изменено

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("reading_tasks.id"))
    reading_var: Mapped["Reading"] = relationship("Reading", back_populates="first_tasks")


class ReadingFirstTaskOption(Base): # Изменено
    __tablename__ = "reading_first_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("reading_first_tasks.id"))
    task: Mapped["ReadingFirstTask"] = relationship("ReadingFirstTask", back_populates="options") # Изменено


class ReadingFirstTaskQuestion(Base): # Изменено
    __tablename__ = "reading_first_task_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("reading_first_tasks.id"))
    task: Mapped["ReadingFirstTask"] = relationship("ReadingFirstTask", back_populates="questions") # Изменено


class ReadingSecondTask(Base): # Изменено
    __tablename__ = "reading_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    options: Mapped[list["ReadingSecondTaskOption"]] = relationship("ReadingSecondTaskOption", back_populates="task") # Изменено
    questions: Mapped[list["ReadingSecondTaskQuestion"]] = relationship("ReadingSecondTaskQuestion", back_populates="task") # Изменено

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("reading_tasks.id"))
    reading_var: Mapped["Reading"] = relationship("Reading", back_populates="second_tasks")

class ReadingSecondTaskOption(Base): # Изменено
    __tablename__ = "reading_second_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("reading_second_tasks.id"))
    task: Mapped["ReadingSecondTask"] = relationship("ReadingSecondTask", back_populates="options") # Изменено


class ReadingSecondTaskQuestion(Base): # Изменено
    __tablename__ = "reading_second_task_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("reading_second_tasks.id"))
    task: Mapped["ReadingSecondTask"] = relationship("ReadingSecondTask", back_populates="questions") # Изменено


class ReadingThirdTask(Base): # Изменено
    __tablename__ = "reading_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    options: Mapped[list["ReadingThirdTaskOption"]] = relationship("ReadingThirdTaskOption", back_populates="task") # Изменено

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("reading_tasks.id"))
    reading_var: Mapped["Reading"] = relationship("Reading", back_populates="third_tasks")

class ReadingThirdTaskOption(Base): # Изменено
    __tablename__ = "reading_third_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("reading_third_tasks.id"))
    task: Mapped["ReadingThirdTask"] = relationship("ReadingThirdTask", back_populates="options") # Изменено