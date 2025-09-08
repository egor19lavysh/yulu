from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ListeningHSK4(Base):
    __tablename__ = "hsk4_listening_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    audio_id: Mapped[str]

    first_type_tasks: Mapped[list["FirstTaskHSK4"]] = relationship("FirstTaskHSK4", back_populates="listening_var")
    second_type_tasks: Mapped[list["SecondTaskHSK4"]] = relationship("SecondTaskHSK4", back_populates="listening_var")
    third_type_tasks: Mapped[list["ThirdTaskHSK4"]] = relationship("ThirdTaskHSK4", back_populates="listening_var")


class FirstTaskHSK4(Base):
    __tablename__ = "hsk4_listening_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    is_correct: Mapped[bool] = mapped_column(default=False)

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK4"] = relationship("ListeningHSK4", back_populates="first_type_tasks")


class SecondTaskHSK4(Base):
    __tablename__ = "hsk4_listening_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))  # Добавить валидацию на верхний регистр

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK4"] = relationship("ListeningHSK4", back_populates="second_type_tasks")

    options: Mapped[list["SecondTaskHSK4Option"]] = relationship("SecondTaskHSK4Option", back_populates="task")


class SecondTaskHSK4Option(Base):
    __tablename__ = "hsk4_listening_second_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_second_tasks.id"))
    task: Mapped["SecondTaskHSK4"] = relationship("SecondTaskHSK4", back_populates="options")


class ThirdTaskHSK4(Base):
    __tablename__ = "hsk4_listening_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK4"] = relationship("ListeningHSK4", back_populates="third_type_tasks")

    options: Mapped[list["ThirdTaskHSK4Option"]] = relationship("ThirdTaskHSK4Option", back_populates="task")


class ThirdTaskHSK4Option(Base):
    __tablename__ = "hsk4_listening_third_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_third_tasks.id"))
    task: Mapped["ThirdTaskHSK4"] = relationship("ThirdTaskHSK4", back_populates="options")
