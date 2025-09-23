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


class FirstTaskHSK1(Base):
    __tablename__ = "hsk1_listening_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    is_correct: Mapped[bool] = mapped_column(default=False)

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK1"] = relationship("ListeningHSK1", back_populates="first_type_tasks")


class SecondTaskHSK1(Base):
    __tablename__ = "hsk1_listening_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))  # Добавить валидацию на верхний регистр

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK1"] = relationship("ListeningHSK1", back_populates="second_type_tasks")

    options: Mapped[list["SecondTaskHSK1Option"]] = relationship("SecondTaskHSK1Option", back_populates="task")


class SecondTaskHSK1Option(Base):
    __tablename__ = "hsk1_listening_second_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_second_tasks.id"))
    task: Mapped["SecondTaskHSK1"] = relationship("SecondTaskHSK1", back_populates="options")


class ThirdTaskHSK1(Base):
    __tablename__ = "hsk1_listening_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK1"] = relationship("ListeningHSK1", back_populates="third_type_tasks")

    options: Mapped[list["ThirdTaskHSK1Option"]] = relationship("ThirdTaskHSK1Option", back_populates="task")


class ThirdTaskHSK1Option(Base):
    __tablename__ = "hsk1_listening_third_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_listening_third_tasks.id"))
    task: Mapped["ThirdTaskHSK1"] = relationship("ThirdTaskHSK1", back_populates="options")
