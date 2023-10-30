import os
from pydantic_settings import BaseSettings



class _Config:#(BaseSettings):
    MONGODB_URL : str = "mongodb://mongo:27017"

    REDIS_URL : str = "redis://redis:6379"
    REDIS_KEY_TTL : int = 60*60

    class Config:
        env_file = ".env"
        extra = "ignore"


SETTINGS = _Config()
