from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse

from db import db
from db.auth import add_user,check_password,delete_user,update_password,update_user
from db.auth.errors import InvalidCredentials,UserAlreadyExists
from db.auth.utils import hash_password
from schemas import ChangePassword, Email, Signup,Login,User,Result,Profile
from auth.jwt_auth import JWTHandler


router = APIRouter(prefix='/v1')

ACCOUNTS_COLLECTION_NAME = "accounts"
collection = db[ACCOUNTS_COLLECTION_NAME]
jwt_object = JWTHandler()




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
        return JSONResponse(Result(msg="ok").model_dump(), status_code=201)
    return JSONResponse(
        Result.resolve_error(UserAlreadyExists).model_dump(),
        status_code=403
    )


@router.post('/login/', status_code=200)
async def login(data:Login):
    user = await collection.find_one({
        "username":data.username,
        "password":hash_password(data.password)
    })
    if not user:
        return JSONResponse(
            Result.resolve_error(InvalidCredentials).model_dump(),
            status_code=403
        )
    return Result(user=User(**user)).model_dump()



@router.get("/profile/")
async def profile(user:User=Depends(jwt_object.get_user)):
    return user


@router.put("/profile/",)
async def profile_update(new_data:Profile, user:User=Depends(jwt_object.get_user)):
    user = user.model_copy(update=new_data.model_dump())
    await update_user(user.id, user)
    return Result().model_dump()


@router.delete("/profile/")
async def profile_delete(user:User=Depends(jwt_object.get_user)):
    await delete_user(user.id)
    # logout from all user sessions
    return Result(message="ok").model_dump()

