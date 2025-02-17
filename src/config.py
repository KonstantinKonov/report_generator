from typing import Literal

from pydantic_settings import BaseSettigs, SettingsConfigDict


class Settings(BaseSettigs):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    APP_HOST: str
    APP_PORT: int

    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
