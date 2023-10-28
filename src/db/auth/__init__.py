from db import db

from schemas.auth import User,Signup

from auth.utils import hash_password



collection = db["accounts"]




async def add_user(user=Signup):
    if await get_user(user.username):
        return None
    if await collection.find_one({"email":user.email}):
        return None
    result = await collection.insert_one({
        "username": user.username,
        "password": hash_password(user.password),
        "email": user.email
        # **other
    })
    return result


async def get_user(username, **kwargs) -> User:
    data = await collection.find_one({"username":username, **kwargs}, )
    return User(**data) if data else None


async def get_password(username):
    return (await collection.find_one({"username":username}))["password"]

async def check_password(username, password):
    user = await get_user(username)
    if hash_password(password) == (await get_password(username)):
        return True
    return False


async def delete_user(username):
    await collection.delete_one({"username":username})
