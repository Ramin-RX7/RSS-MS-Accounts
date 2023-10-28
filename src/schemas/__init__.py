from pydantic import BaseModel,Field

from db import db
from .base import *

collection = db["accounts"]



class Signup(BaseModel):
    username: str
    password: str
    email: str


class Login(BaseModel):
    username : str
    password : str


class User(BaseModel):
    username: str
    email: str
    name: str|None = None
    # is_active: bool = True
    # is_staff:bool = False

    class Config:
        extra = "ignore"
