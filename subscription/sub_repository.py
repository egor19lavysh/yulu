from typing import Optional, List
from datetime import datetime, timedelta, timezone, date

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_session_async
from .models import Subscription, SubscriptionType


class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, subscription: Subscription) -> Subscription:
        """Создать новую подписку"""
        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription)
        return subscription
    
    async def get_all_subs(self) -> list[Subscription]:
        stmt = select(Subscription)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_user_id(self, user_id: int) -> Optional[Subscription]:
        """Получить подписку по ID пользователя"""
        stmt = select(Subscription).where(Subscription.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """Получить подписку по ID"""
        stmt = select(Subscription).where(Subscription.id == subscription_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def extend_sub(self, user_id: int,
                         start_date: date,
                          days: int = 30,
                          ):
        stmt = (update(Subscription)
        .where(Subscription.user_id == user_id)
        .values(sub_type=SubscriptionType.PREMIUM, start_date=start_date, end_date=start_date + timedelta(days=days))
        )
        await self.session.execute(stmt)
        await self.session.commit()

    

async def get_sub_repo():
    async for session in get_db_session_async():
        return SubscriptionRepository(session=session)