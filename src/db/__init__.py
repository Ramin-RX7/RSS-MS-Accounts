import motor.motor_asyncio

from config import SETTINGS


client = motor.motor_asyncio.AsyncIOMotorClient(SETTINGS.MONGODB_URL)
db = client["fastapi"]


def get_db():
    return db


async def query(collection_name:str, query:dict, **kwargs):
    collection = get_db()[collection_name]
    return collection.find(query, **kwargs)
