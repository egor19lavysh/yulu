from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: str = "5432"
    PRIVATE_GROUP_ID: int

    @property
    def DB_URL(self):
        # # Если есть готовая DATABASE_URL (например, от Railway), используем её
        # database_url = os.getenv('DATABASE_URL')
        # if database_url:
        #     # Railway использует postgres://, а SQLAlchemy требует postgresql://
        #     return database_url.replace('postgres://', 'postgresql+psycopg2://', 1)

        # Иначе собираем из отдельных параметров
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )


settings = Settings()