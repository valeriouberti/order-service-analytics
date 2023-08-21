import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PINOT_HOST: str = os.environ.get("PINOT_HOST", "localhost")
    PINOT_PORT: int = os.environ.get("PINOT_PORT", 8099)


settings = Settings()