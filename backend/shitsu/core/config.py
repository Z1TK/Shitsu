import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: str

    SECRET_KEY: str
    ALGORITHM: str
    SHEMA_CRYPT: str
    ACCESS_TIME: int
    REFRESH_TIME: int
    VERIFY_TIME: int

    MAIL: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int

    model_config = SettingsConfigDict(
        env_file=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../", ".env")
        )
    )

    def get_db_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    def get_redis_url(self, db: int = 0):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}"


settings = Settings()
