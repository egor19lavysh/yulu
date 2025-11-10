
from datetime import datetime, timedelta, timezone, date
from enum import Enum
from typing import Optional
from database import Base
from sqlalchemy import BigInteger, Boolean, DateTime, Enum as SQLEnum, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class SubscriptionType(str, Enum):
    TRIAL = "trial"  # Пробная подписка (5 дней)
    PREMIUM = "premium"  # Платная подписка (30 дней)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    sub_type: Mapped[str] = mapped_column(default=SubscriptionType.TRIAL)
    start_date: Mapped[date]
    end_date: Mapped[date]

    @property
    def is_expired(self) -> bool:
        return date.today() > self.end_date