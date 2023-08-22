import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BOOTSTRAP_SERVERS: str = os.environ.get("BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC: str = os.environ.get("ORDER_TOPIC", "orders")
    API_KEYS: List = os.environ.get("API_KEYS", "changeme").split(",")


settings = Settings()
