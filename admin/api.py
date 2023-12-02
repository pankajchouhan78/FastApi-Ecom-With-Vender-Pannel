from fastapi import APIRouter
from admin.pydantic_schemas import UserCreate, UserSign, Token, UserUpdate, UserDelete
from passlib.context import CryptContext
from admin.models import User
from fastapi_login import LoginManager
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router=APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager("your-secret-key",token_url="/auth/token")
def get_password_hashed(password):
    return pwd_context.hash(password)

@router.post('/user/')
async def signup(data:UserCreate):
    if await User.exists(email=data.email):
        return {"status":False, "message": "User Already Exists"}
    else:
        await User.create(
            name=data.name,
            email=data.email,
            password=get_password_hashed(data.password),
            city=data.city,
            address=data.address
        )
        return {"status":True, "message":"User Successfully Created"}
    
@router.get('/user/')
async def get_user():
    return await User.all()

@manager.user_loader()
async def load_user(email):
    if await User.exists(email=email):
        user = await User.get(email=email)
        return user
def varify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post('/usersign/')
async def sign(data:UserSign):
    user = await load_user(data.email)
    if not user:
        return JSONResponse({"status":False, "message":"User Not Registerd"}, status_code=403)
    elif not varify_password(data.password, user.password):
        return JSONResponse({"status":False, "message":"Invalid Password"},status_code=403)
    
    access_token = manager.create_access_token(
        data={'sub':jsonable_encoder(user.email),
              'name':jsonable_encoder(user.email)
              }
        )
    new_dict = jsonable_encoder(user)
    new_dict.update({"access_token":access_token})
    return Token(access_token=access_token)

@router.put("/user/")
async def update_user(data:UserUpdate):
        if await User.exists(id =data.id):
                await User.filter(id = data.id).update(name = data.name,
                                                                  email= data.email,
                                                                  password=data.password,
                                                                  city = data.city,
                                                                  address = data.address)
                return JSONResponse({"status":True, "message":"User Successfully Updated"}, status_code=200)
        else: 
            return JSONResponse({"status":False, "message":"Invalid User ID"}, status_code=403)
        
@router.delete('/user/')
async def delete_user(data:UserDelete):
     if await User.exists(id=data.id):
            await User.filter(id=data.id).delete()
            return JSONResponse({"status":True, "message":"User Successfully Deleted"}, status_code=200)
     else:
            return JSONResponse({"status":False, "message":"Invalid User ID"}, status_code=403)
    

