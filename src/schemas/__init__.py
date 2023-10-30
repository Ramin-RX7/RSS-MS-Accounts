from datetime import datetime

from pydantic import BaseModel, model_validator,Field

from db import db
from .base import *
from auth.validators import password_validator

collection = db["accounts"]



class Signup(BaseModel):
    username: str
    password: str
    email: str


class Login(BaseModel):
    username : str
    password : str


class Profile(BaseModel):
    first_name: str|None = None
    last_name : str|None = None
    birth_date: datetime|None = None


class ChangePassword(BaseModel):
    old_password : str
    new_password : str
    confirm_password : str

    @model_validator(mode='after')
    def check_passwords_match(self):
        pw1 = self.new_password
        pw2 = self.confirm_password
        password_validator(pw1)
        assert pw1==pw2, "Password and confirm password are not equal"
        return self
    username: str
    email: str
    # password: str   #? Commented out so it won't be retrieved from database (retrieved but not saved)
    first_name: str|None = None
    last_name : str|None = None
    birth_date: datetime|None = None
    is_admin  : bool = False
    is_active : bool = True
    is_superuser: bool = False
    permissions: list[str] = []
    groups: dict = {}   # dict[id,list[str]]

    class Config:
        extra = "ignore"
