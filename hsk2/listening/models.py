from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ListeningHSK2(Base):
    __tablename__ = "hsk2_listening_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    audio_id: Mapped[str]

    first_type_tasks: Mapped[list["FirstTaskHSK2"]] = relationship("FirstTaskHSK2", back_populates="listening_var")
    second_type_tasks: Mapped[list["SecondTaskHSK2"]] = relationship("SecondTaskHSK2", back_populates="listening_var")
    third_type_tasks: Mapped[list["ThirdTaskHSK2"]] = relationship("ThirdTaskHSK2", back_populates="listening_var")


class FirstTaskHSK2(Base):
    __tablename__ = "hsk1_listening_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    questions: Mapped[list["FirstTaskHSK2Question"]] = relationship("FirstTaskHSK2Question", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk2_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK2"] = relationship("ListeningHSK2", back_populates="first_type_tasks")


class FirstTaskHSK2Question(Base):
    __tablename__ = "hsk2_listening_first_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_correct: Mapped[bool]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk2_listening_first_tasks.id"))
    task = relationship("FirstTaskHSK2", back_populates="questions")


class SecondTaskHSK2(Base):
    __tablename__ = "hsk2_listening_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    questions: Mapped[list["SecondTaskHSK2Question"]] = relationship("SecondTaskHSK2Question", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk2_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK2"] = relationship("ListeningHSK2", back_populates="second_type_tasks")


class SecondTaskHSK2Question(Base):
    __tablename__ = "hsk2_listening_second_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk2_listening_second_tasks.id"))
    task = relationship("SecondTaskHSK2", back_populates="questions")


class ThirdTaskHSK2(Base):
    __tablename__ = "hsk2_listening_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    questions: Mapped[list["ThirdTaskHSK2Option"]] = relationship("ThirdTaskHSK2Option", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk2_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK2"] = relationship("ListeningHSK2", back_populates="third_type_tasks")


class ThirdTaskHSK2Question(Base):
    __tablename__ = "hsk2_listening_third_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    options: Mapped[list["ThirdTaskHSK2Option"]] = relationship("ThirdTaskHSK2Option", back_populates="question")

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk2_listening_third_tasks.id"))
    task: Mapped["ThirdTaskHSK2"] = relationship("ThirdTaskHSK2", back_populates="questions")


class ThirdTaskHSK2Option(Base):
    __tablename__ = "hsk2_listening_third_tasks_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    question_id: Mapped[int] = mapped_column(ForeignKey("hsk2_listening_third_tasks_questions.id"))
    question: Mapped["ThirdTaskHSK2Question"] = relationship("ThirdTaskHSK2Question", back_populates="options")
