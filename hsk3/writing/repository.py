from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from database import get_db_session
from .models import *


@dataclass
class WritingRepository:
    db_session: Session

    def get_variants(self) -> list[Writing]:
        with self.db_session as session:
            variants = list(session.execute(select(Writing)).scalars().all())
            return variants

    def get_variant_by_id(self, variant_id: int) -> Writing | None:
        with self.db_session as session:
            stmt = select(Writing).where(Writing.id == variant_id).options(
                selectinload(Writing.first_tasks),
                selectinload(Writing.second_tasks)
            )

            variant = session.execute(stmt).scalar_one_or_none()
            return variant


session = next(get_db_session())
repo = WritingRepository(session)
