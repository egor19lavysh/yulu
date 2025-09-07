from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Listening(Base):
    __tablename__ = "hsk4_listening_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    audio_id: Mapped[str]

    first_type_tasks: Mapped[list["FirstTask"]] = relationship("FirstTask", back_populates="listening_var")
    second_type_tasks: Mapped[list["SecondTask"]] = relationship("SecondTask", back_populates="listening_var")
    third_type_tasks: Mapped[list["ThirdTask"]] = relationship("ThirdTask", back_populates="listening_var")


class FirstTask(Base):
    __tablename__ = "hsk4_listening_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    is_correct: Mapped[bool] = mapped_column(default=False)

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_tasks.id"))
    listening_var = relationship("Listening", back_populates="first_type_tasks")


class SecondTask(Base):
    __tablename__ = "hsk4_listening_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))
    options: Mapped[list["SecondTaskOption"]] = relationship("SecondTaskOption", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_tasks.id"))
    listening_var = relationship("Listening", back_populates="second_type_tasks")


class SecondTaskOption(Base):
    __tablename__ = "hsk4_listening_second_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_second_tasks.id"))
    task = relationship("SecondTask", back_populates="options")


class ThirdTask(Base):
    __tablename__ = "hsk4_listening_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))
    options: Mapped[list["ThirdTaskOption"]] = relationship("ThirdTaskOption", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_tasks.id"))
    listening_var = relationship("Listening", back_populates="third_type_tasks")


class ThirdTaskOption(Base):
    __tablename__ = "hsk4_listening_third_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk4_listening_third_tasks.id"))
    task = relationship("ThirdTask", back_populates="options")