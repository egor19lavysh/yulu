from datetime import datetime, timedelta

from database import Base
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import mapped_column, Mapped


class User(Base):
    __tablename__ = "yulu_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    subscription_expires = Column(DateTime, nullable=True)
    used_full_variant: Mapped[bool] = mapped_column(default=False)
    used_listening: Mapped[bool] = mapped_column(default=False)
    used_reading: Mapped[bool] = mapped_column(default=False)
    used_writing: Mapped[bool] = mapped_column(default=False)

    @property
    def is_subscription_active(self):
        if self.subscription_expires is None:
            return False
        return self.subscription_expires > datetime.utcnow()

    @property
    def used_trial_subscription(self):
        if self.used_full_variant or all([self.used_listening, self.used_reading, self.used_writing]):
            return True
        return False

    def activate_subscription(self, days=30):
        if self.subscription_expires and self.subscription_expires > datetime.utcnow():
            # Продлить существующую подписку
            self.subscription_expires += timedelta(days=days)
        else:
            # Новая подписка
            self.subscription_expires = datetime.utcnow() + timedelta(days=days)
