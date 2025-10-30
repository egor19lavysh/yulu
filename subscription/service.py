from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from .repository import UserRepository, repository
from .models import User


class UserService:
    """Сервис для работы с пользователями"""
    
    def __init__(self, repository: UserRepository):
        self.user_repo = repository
    
    def get_or_create_user(self, user_id: str) -> User:
        """Получить пользователя или создать нового если не существует"""
        user = self.user_repo.get_user(user_id)
        if not user:
            self.user_repo.create_user(user_id)
            user = self.user_repo.get_user(user_id)
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Получить пользователя по ID"""
        return self.user_repo.get_user(user_id)
    
    def activate_subscription(self, user_id: str, days: int = 30) -> User:
        """Активировать или продлить подписку пользователю"""
        user = self.get_or_create_user(user_id)
        self.user_repo.update_user_subscription(user_id, days)
        return self.user_repo.get_user(user_id)
    
    def check_subscription(self, user_id: str) -> bool:
        """Проверить активна ли подписка у пользователя"""
        user = self.get_user(user_id)
        if not user:
            return False
        return user.is_subscription_active
    
    def get_subscription_info(self, user_id: str) -> dict:
        """Получить информацию о подписке пользователя"""
        user = self.get_or_create_user(user_id)
        
        return {
            "has_subscription": user.is_subscription_active,
            "expires_at": user.subscription_expires,
            "days_remaining": (user.subscription_expires - datetime.utcnow()).days if user.is_subscription_active else 0,
            "used_trial": user.used_trial_subscription
        }
    
    def mark_used_full_variant(self, user_id: str) -> None:
        """Пометить что пользователь использовал полный вариант"""
        user = self.get_or_create_user(user_id)
        self.user_repo.update_user_used_full_variant(user_id)
    
    def mark_used_listening(self, user_id: str) -> None:
        """Пометить что пользователь использовал аудирование"""
        user = self.get_or_create_user(user_id)
        self.user_repo.update_user_used_listening(user_id)
    
    def mark_used_reading(self, user_id: str) -> None:
        """Пометить что пользователь использовал чтение"""
        user = self.get_or_create_user(user_id)
        self.user_repo.update_user_used_reading(user_id)
    
    def mark_used_writing(self, user_id: str) -> None:
        """Пометить что пользователь использовал письмо"""
        user = self.get_or_create_user(user_id)
        self.user_repo.update_user_used_writing(user_id)
    
    def can_use_trial(self, user_id: str, section: str = None) -> bool:
        """
        Проверить может ли пользователь использовать пробный доступ
        
        Args:
            user_id: ID пользователя
            section: конкретный раздел ('listening', 'reading', 'writing') или None для полного варианта
        """
        user = self.get_or_create_user(user_id)
        
        # Если у пользователя активная подписка - доступ разрешен
        if user.is_subscription_active:
            return True
        
        # Проверка пробного доступа
        if section is None:
            # Полный вариант - проверяем не использован ли он
            return not user.used_full_variant
        else:
            # Конкретный раздел
            section_attr = f"used_{section}"
            if hasattr(user, section_attr):
                return not getattr(user, section_attr)
        
        return False
    
    def use_trial_access(self, user_id: str, section: str = None) -> bool:
        """
        Использовать пробный доступ
        
        Returns:
            bool: Успешно ли использован пробный доступ
        """
        if not self.can_use_trial(user_id, section):
            return False
        
        if section is None:
            self.mark_used_full_variant(user_id)
        elif section == 'listening':
            self.mark_used_listening(user_id)
        elif section == 'reading':
            self.mark_used_reading(user_id)
        elif section == 'writing':
            self.mark_used_writing(user_id)
        
        return True
    
    def delete_user(self, user_id: str) -> None:
        """Удалить пользователя"""
        self.user_repo.delete_user(user_id)
    
    def get_user_stats(self, user_id: str) -> dict:
        """Получить статистику пользователя"""
        user = self.get_or_create_user(user_id)
        
        return {
            "user_id": user.user_id,
            "subscription_active": user.is_subscription_active,
            "subscription_expires": user.subscription_expires,
            "used_full_variant": user.used_full_variant,
            "used_listening": user.used_listening,
            "used_reading": user.used_reading,
            "used_writing": user.used_writing,
            "used_trial_subscription": user.used_trial_subscription
        }
    
service = UserService(repository=repository)