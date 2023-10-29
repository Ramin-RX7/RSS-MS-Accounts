from datetime import datetime

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
    # _id : ObjectId|None
    username: str
    email: str
    # password: str   #? Commented out so it won't be retrieved from database (retrieved but not saved)
    first_name: str|None = None
    last_name : str|None = None
    birth_date: datetime
    is_admin  : bool = False
    is_active : bool = True
    is_superuser: bool = False
    permissions: list[str] = []
    groups: dict = {}   # dict[id,list[str]]

    class Config:
        extra = "ignore"
