from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ListeningHSK1(Base):
    __tablename__ = "hsk1_listening_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    audio_id: Mapped[str]

    first_type_tasks: Mapped[list["FirstTaskHSK1"]] = relationship("FirstTaskHSK1", back_populates="listening_var")
    second_type_tasks: Mapped[list["SecondTaskHSK1"]] = relationship("SecondTaskHSK1", back_populates="listening_var")
    third_type_tasks: Mapped[list["ThirdTaskHSK1"]] = relationship("ThirdTaskHSK1", back_populates="listening_var")
    fourth_type_tasks: Mapped[list["FourthTaskHSK1"]] = relationship("FourthTaskHSK1", back_populates="listening_var")


class FirstTaskHSK1(Base):
    __tablename__ = "hsk1_listening_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    questions: Mapped[list["FirstTaskHSK1Question"]] = relationship("FirstTaskHSK1Question", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK1"] = relationship("ListeningHSK1", back_populates="first_type_tasks")


class FirstTaskHSK1Question(Base):
    __tablename__ = "hsk1_listening_first_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_correct: Mapped[bool]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_first_tasks.id"))
    task = relationship("FirstTaskHSK1", back_populates="questions")


class SecondTaskHSK1(Base):
    __tablename__ = "hsk1_listening_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    questions: Mapped[list["SecondTaskHSK1Question"]] = relationship("SecondTaskHSK1Question", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK1"] = relationship("ListeningHSK1", back_populates="second_type_tasks")


class SecondTaskHSK1Question(Base):
    __tablename__ = "hsk1_listening_second_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_second_tasks.id"))
    task = relationship("SecondTaskHSK1", back_populates="questions")


class ThirdTaskHSK1(Base):
    __tablename__ = "hsk1_listening_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    questions: Mapped[list["ThirdTaskHSK1Question"]] = relationship("ThirdTaskHSK1Question", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK1"] = relationship("ListeningHSK1", back_populates="third_type_tasks")


class ThirdTaskHSK1Question(Base):
    __tablename__ = "hsk1_listening_third_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_third_tasks.id"))
    task = relationship("ThirdTaskHSK1", back_populates="questions")


class FourthTaskHSK1(Base):
    __tablename__ = "hsk1_listening_fourth_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    questions: Mapped[list["FourthTaskHSK1Question"]] = relationship("FourthTaskHSK1Question", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK1"] = relationship("ListeningHSK1", back_populates="fourth_type_tasks")


class FourthTaskHSK1Question(Base):
    __tablename__ = "hsk1_listening_fourth_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    options: Mapped[list["FourthTaskHSK1Option"]] = relationship("FourthTaskHSK1Option", back_populates="question")

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_fourth_tasks.id"))
    task: Mapped["FourthTaskHSK1"] = relationship("FourthTaskHSK1", back_populates="questions")


class FourthTaskHSK1Option(Base):
    __tablename__ = "hsk1_listening_fourth_tasks_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    question_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_fourth_tasks_questions.id"))
    question: Mapped["FourthTaskHSK1Question"] = relationship("FourthTaskHSK1Question", back_populates="options")