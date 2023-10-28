from pydantic import BaseModel,Field

from db import db


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




class Error(BaseModel):
    type : str
    message : str

    class Config:
        extra = "allow"

    def __bool__(self):
        return False


class Result(BaseModel):
    status: bool = Field(True, alias="__status")   #? Should this be True|Error
    data: dict = {}
    error: Error|None

    def __init__(self, __status, **data):
        self.status = __status
        return super().__init__(**data)

    def __bool__(self):
        return self.status

    def model_dump(self, **kwargs):
        excludes = ["error"] if self.error is not None else ["data"]
        return super().model_dump(exclude=excludes, **kwargs)

    class Config:
        extra = "allow"
