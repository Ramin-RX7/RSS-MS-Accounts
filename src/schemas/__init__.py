from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, field_serializer, field_validator, model_validator,Field

from db import db
from auth.validators import password_validator


from .base import *
from .jwt import *

collection = db["accounts"]



class Scheme(BaseModel):
    # created_at: datetime
    # updated_at: datetime
    async def save(self, _id=None):
        collection = db[self._db_collection]
        id = _id #or self.id
        doc_data = self.model_dump(exclude_defaults=True)
        if _id:
            await collection.insert_one(doc_data)
        else:
            await collection.update_one(filter={"_id":id}, update=doc_data)


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

class Email(BaseModel):
    email : str


class User(Profile):
    id : ObjectId|None = Field(alias="_id")
    username: str
    email: str
    # password: str|None = Field(default=None, exclude=True)
    is_admin  : bool = False
    is_active : bool = True
    is_superuser: bool = False
    permissions: list[str] = []
    groups: dict = {}   # dict[id,list[str]]

    class Config:
        extra = "ignore"
        arbitrary_types_allowed=True

    @field_validator("id",mode="before")
    def id_validator(cls, value):
        if type(value)==str:
            return ObjectId(value)
        return value

    @field_serializer('id')
    def id_serializer(self, id, _info):
        return str(id)
