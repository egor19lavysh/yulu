from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class WritingHSK5(Base):
    __tablename__ = "hsk5_writing_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_type_tasks: Mapped[list["WritingFirstTaskHSK5"]] = relationship("WritingFirstTaskHSK5",
                                                                          back_populates="writing_var")
    second_type_tasks: Mapped[list["WritingSecondTaskHSK5"]] = relationship("WritingSecondTaskHSK5",
                                                                            back_populates="writing_var")
    third_type_tasks: Mapped[list["WritingSecondTaskHSK5"]] = relationship("WritingThirdTaskHSK5",
                                                                            back_populates="writing_var")


class WritingFirstTaskHSK5(Base):
    __tablename__ = "hsk5_writing_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_sentence: Mapped[str]
    words: Mapped[str]

    writing_var_id: Mapped[int] = mapped_column(ForeignKey("hsk5_writing_tasks.id"))
    writing_var: Mapped["WritingHSK5"] = relationship("WritingHSK5", back_populates="first_type_tasks")


class WritingSecondTaskHSK5(Base):
    __tablename__ = "hsk5_writing_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]

    writing_var_id: Mapped[int] = mapped_column(ForeignKey("hsk5_writing_tasks.id"))
    writing_var: Mapped["WritingHSK5"] = relationship("WritingHSK5", back_populates="second_type_tasks")


class WritingThirdTaskHSK5(Base):
    __tablename__ = "hsk5_writing_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]

    writing_var_id: Mapped[int] = mapped_column(ForeignKey("hsk5_writing_tasks.id"))
    writing_var: Mapped["WritingHSK5"] = relationship("WritingHSK5", back_populates="third_type_tasks")
