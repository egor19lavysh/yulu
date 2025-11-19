from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession

from subscription.models import Subscription
from subscription.sub_repository import get_sub_repo


class SubscriptionMiddleware(BaseMiddleware):
    ALLOWED_COMMANDS = ['/start', '/subscribe', '/help', '/status', '/feedback']
    ALLOWED_CONTENT_TYPES = ['successful_payment']

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        
        if isinstance(event, Message) and hasattr(event, 'successful_payment') and event.successful_payment:
            return await handler(event, data)
        
        if isinstance(event, Message) and event.text in self.ALLOWED_COMMANDS:
            return await handler(event, data)
        
        if isinstance(event, Message) and handler.__name__ == "get_feedback":
            return await handler(event, data)
        
        # Получаем сессию из данных
        repo = await get_sub_repo()
        user_id = event.from_user.id
        
        # Проверяем подписку пользователя
        subscription = await repo.get_by_user_id(user_id=user_id)
        
        if subscription and subscription.is_expired:
            # Если подписка просрочена
            if isinstance(event, Message):
                await event.answer(
                    "❌ Ваша подписка истекла. Пожалуйста, продлите подписку для доступа к функциям бота. Для этого нажмите /subscribe")
                return  # Прерываем выполнение хендлера
            elif isinstance(event, CallbackQuery):
                await event.message.answer(
                    "❌ Ваша подписка истекла. Пожалуйста, продлите подписку для доступа к функциям бота. Для этого нажмите /subscribe",
                    show_alert=True
                )
                return
        
        # Если подписка активна или пользователя нет в базе, пропускаем
        return await handler(event, data)
