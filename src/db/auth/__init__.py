from db import db

from schemas import User,Signup

from db.auth.utils import hash_password



collection = db["accounts"]




async def add_user(user=Signup):
    if await get_user(username=user.username):
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


async def get_user(**kwargs) -> User:
    assert kwargs != {}, "filter need to be set to query over collection"
    data = await collection.find_one({**kwargs})
    if data:
        return User(**data)


async def get_password(username):
    user = (await collection.find_one({"username":username}, {"password":1, "_id":0}))
    return user["password"] if user else None

async def check_password(username, password):
    if hash_password(password) == (await get_password(username)):
        return True
    return False


async def delete_user(username):
    await collection.delete_one({"username":username})


async def update_user(username, new_data:User):
    assert username == new_data.username
    res = await collection.find_one_and_update(
        {"username":username},
        {"$set":new_data.model_dump(exclude_unset=True)}
    )


async def update_password(username:str, new_password:str):
    res = await collection.find_one_and_update(
        {"username":username},
        {"$set":{"password": hash_password(new_password)}}
    )
