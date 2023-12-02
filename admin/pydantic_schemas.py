from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name:str
    email:str
    password:str
    city:str
    address:str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserSign(BaseModel):
    email:str
    password:str

class UserUpdate(UserCreate):
    id:int
class UserDelete(BaseModel):
    id:int