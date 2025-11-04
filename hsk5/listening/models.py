from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ListeningHSK5(Base):
    __tablename__ = "hsk5_listening_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    audio_id: Mapped[str]

    first_type_tasks: Mapped[list["FirstTaskHSK5"]] = relationship("FirstTaskHSK5", back_populates="listening_var")


class FirstTaskHSK5(Base):
    __tablename__ = "hsk5_listening_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))
    options: Mapped[list["FirstTaskHSK5Option"]] = relationship("FirstTaskHSK5Option", back_populates="task")

    listening_var_id: Mapped[int] = mapped_column(ForeignKey("hsk5_listening_tasks.id"))
    listening_var: Mapped["ListeningHSK5"] = relationship("ListeningHSK5", back_populates="first_type_tasks")


class FirstTaskHSK5Option(Base):
    __tablename__ = "hsk5_listening_first_tasks_option"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk5_listening_first_tasks.id"))
    task: Mapped["FirstTaskHSK5"] = relationship("FirstTaskHSK5", back_populates="options")