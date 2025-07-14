from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from config import settings

engine = create_engine(
    url=settings.DB_URL,
    echo=True
)

session_factory = sessionmaker(engine)


def get_db_session() -> Session:
    with session_factory() as session:
        yield session


class Base(DeclarativeBase):
    pass
