import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOOTSTRAP_SERVERS: str = os.environ.get("BOOTSTRAP_SERVERS", "localhost:29092")
    ORDER_TOPIC: str = os.environ.get("ORDER_TOPIC", "orders")
    API_KEYS: List = os.environ.get("API_KEYS", "changeme").split(",")


settings = Settings()
