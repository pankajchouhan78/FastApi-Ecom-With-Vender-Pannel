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
class CategorySchema(BaseModel):
    name:str
class CategoryUpdateSchema(CategorySchema):
    id:int
class CategoryDeleteSchema(BaseModel):
    id:int
class SubCategorySchema(BaseModel):
    category_id:int
    subcategory_name:str
class SubCategoryUpdateSchema(BaseModel):
    subcategory_id: int
    subcategory_name:str
class SubCategoryDeleteSchema(BaseModel):
    subcategory_id:int
