import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOOTSTRAP_SERVERS: str = os.environ.get("BOOTSTRAP_SERVERS", "localhost:29092")
    ORDER_TOPIC: str = os.environ.get("ORDER_TOPIC", "orders")


settings = Settings()
