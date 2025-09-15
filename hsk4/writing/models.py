from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class WritingHSK4(Base):
    __tablename__ = "hsk4_writing_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_type_tasks: Mapped[list["WritingFirstTaskHSK4"]] = relationship("WritingFirstTaskHSK4",
                                                                          back_populates="writing_var")
    second_type_tasks: Mapped[list["WritingSecondTaskHSK4"]] = relationship("WritingSecondTaskHSK4",
                                                                            back_populates="writing_var")


class WritingFirstTaskHSK4(Base):
    __tablename__ = "hsk4_writing_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_sentence: Mapped[str]
    words: Mapped[str]

    writing_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_writing_tasks.id"))
    writing_var: Mapped["WritingHSK4"] = relationship("WritingHSK4", back_populates="first_type_tasks")


class WritingSecondTaskHSK4(Base):
    __tablename__ = "hsk4_writing_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    words: Mapped[list["WritingSecondTaskWord"]] = relationship("WritingSecondTaskWord", back_populates="task")

    writing_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_writing_tasks.id"))
    writing_var: Mapped["WritingHSK4"] = relationship("WritingHSK4", back_populates="second_type_tasks")


class WritingSecondTaskWord(Base):
    __tablename__ = "hsk4_writing_second_task_words"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk4_writing_second_tasks.id"))
    task: Mapped["WritingSecondTaskHSK4"] = relationship("WritingSecondTaskHSK4", back_populates="words")
