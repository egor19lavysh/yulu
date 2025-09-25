from dataclasses import dataclass
from database import get_db_session
from .models import User
from sqlalchemy.orm import Session
from sqlalchemy import select, delete



@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, user_id: str) -> None:
        with self.db_session as session:
            new_user = User(user_id=user_id)
            session.add(new_user)
            session.commit()

    def get_user(self, user_id: str) -> User | None:
        with self.db_session as session:
            user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
            return user
        
    def update_user_subscription(self, user_id: str, days: int = 30) -> None:
        if user := self.get_user(user_id=user_id):
            with self.db_session as session:
                user.activate_subscription(days=days)
                session.commit()
        else:
            raise Exception("Такого пользователя не сущетсвует!")
        
    def update_user_used_full_variant(self, user_id: str) -> None:
        if user := self.get_user(user_id=user_id):
            with self.db_session as session:
                user.used_full_variant = True
                session.commit()
        else:
            raise Exception("Такого пользователя не сущетсвует!")
        
    def update_user_used_listening(self, user_id: str) -> None:
        if user := self.get_user(user_id=user_id):
            with self.db_session as session:
                user.used_listening = True
                session.commit()
        else:
            raise Exception("Такого пользователя не сущетсвует!")
        
    def update_user_used_reading(self, user_id: str) -> None:
        if user := self.get_user(user_id=user_id):
            with self.db_session as session:
                user.used_reading = True
                session.commit()
        else:
            raise Exception("Такого пользователя не сущетсвует!")
        
    def update_user_used_writing(self, user_id: str) -> None:
        if user := self.get_user(user_id=user_id):
            with self.db_session as session:
                user.used_writing = True
                session.commit()
        else:
            raise Exception("Такого пользователя не сущетсвует!")
        
    def delete_user(self, user_id: str) -> None:
        if user := self.get_user(user_id=user_id):
            with self.db_session as session:
                session.execute(delete(User).where(User.id == user_id))
                session.commit()
        else:
            raise Exception("Такого пользователя не сущетсвует!")
        
            
