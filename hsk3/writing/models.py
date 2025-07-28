from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Writing(Base):
    __tablename__ = "writing_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_tasks: Mapped[list["WritingFirstTask"]] = relationship("WritingFirstTask",
                                                                 back_populates="writing_var")
    second_tasks: Mapped[list["WritingSecondTask"]] = relationship("WritingSecondTask",
                                                                   back_populates="writing_var")


class WritingFirstTask(Base):
    __tablename__ = "writing_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    chars: Mapped[str]
    correct_answer: Mapped[str]

    writing_var: Mapped["Writing"] = relationship("Writing", back_populates="first_tasks")
    writing_var_id: Mapped[int] = mapped_column(ForeignKey("writing_tasks.id"))


class WritingSecondTask(Base):
    __tablename__ = "writing_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_answer: Mapped[str]

    writing_var: Mapped["Writing"] = relationship("Writing", back_populates="second_tasks")
    writing_var_id: Mapped[int] = mapped_column(ForeignKey("writing_tasks.id"))
