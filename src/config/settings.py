import os
from pydantic_settings import BaseSettings



class _Config(BaseSettings):
    MONGODB_URL : str = os.environ.get("MONGODB_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"


SETTINGS = _Config()
