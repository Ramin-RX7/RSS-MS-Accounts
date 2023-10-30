from typing import Annotated


from fastapi import APIRouter,Depends,Request,HTTPException,Body
from fastapi.responses import JSONResponse

from db import db,query
from db.auth import add_user,get_user,check_password,delete_user
from db.auth.errors import InvalidCredentials,UserAlreadyExists
from schemas import Signup,Login,User,Result,Profile
from auth.jwt_auth import JWTAuth


router = APIRouter(prefix='/v1')

ACCOUNTS_COLLECTION_NAME = "accounts"
collection = db[ACCOUNTS_COLLECTION_NAME]
jwt_object = JWTAuth()




@router.post("/signup/")
async def signup(user_data:Signup):
    existing_users = await db["accounts"].find_one({
        "$or":[
            {"username":user_data.username},
            {"email":user_data.email}
        ]
    })
    if not existing_users:
        await add_user(user_data)
        return JSONResponse(Result().model_dump(), status_code=201)
    return JSONResponse(Result.resolve_error(UserAlreadyExists).model_dump(), status_code=403)


@router.post('/login/', status_code=200)
async def login(data:Login):
    if not await check_password(data.username, data.password):
        return JSONResponse(Result.resolve_error(InvalidCredentials).model_dump(), status_code=403)
    return Result().model_dump()


@router.get("/profile/")
async def profile(user:User=Depends(jwt_object)):
    return user


@router.put("/profile/",)
async def profile_update(new_data:Profile, user:User=Depends(jwt_object)):
    user = user.model_copy(update=new_data.model_dump())
    await update_user(user.username, user)
    return Result()


@router.delete("/profile/")
async def profile_delete(user:User=Depends(jwt_object)):
    await delete_user(user.username)
    return {}
