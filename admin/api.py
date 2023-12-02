from fastapi import APIRouter, UploadFile, Depends, File
from admin.pydantic_schemas import UserCreate, UserSign, Token, UserUpdate, UserDelete
from admin.pydantic_schemas import CategorySchema, CategoryUpdateSchema, CategoryDeleteSchema
from admin.pydantic_schemas import SubCategorySchema, SubCategoryUpdateSchema, SubCategoryDeleteSchema
from admin.pydantic_schemas import ProductSchema, ProductUpdateSchema, ProductDeleteSchema
from passlib.context import CryptContext
from admin.models import User, Category, SubCategory, Photo, Product
from fastapi_login import LoginManager
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
from datetime import datetime
import secrets
from PIL import Image

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

@router.post("/Category/")
async def create_category(data: CategorySchema):
    if await Category.filter(name=data.name).exists():
        return JSONResponse({"status":False, "message": "Category Already Exists"}, status_code=403)
    else:
        await Category.create(name=data.name)
        return JSONResponse({"status":True, "message":"Category Added Successfully"}, status_code=200)

@router.get('/category/')
async def get_category():
     return await Category.all()

@router.put('/category/')
async def update_category(data:CategoryUpdateSchema):
     if await Category.exists(id=data.id):
            await Category.filter(id=data.id).update(
                 name=data.name)
            return JSONResponse({"status":True, "message":"Category Successfully Updated"}, status_code=200)
        
     else:
            return JSONResponse({"status":False, "message":"Invalid Category ID"}, status_code=403)

@router.delete('/category/')
async def delete_category(data:CategoryDeleteSchema):
     if await Category.exists(id=data.id):
          await Category.filter(id=data.id).delete()
          return JSONResponse({"status":True, "message": "Category Successfully Deleted"}, status_code=200)
     else:
          return JSONResponse({"status":False, "message":"Invalid Category ID"}, status_code=403)
     
@router.post('/subcategory/')
async def create_subcategory(data:SubCategorySchema):
     if await Category.exists(id=data.category_id):
        if await SubCategory.exists(name=data.subcategory_name):
            return JSONResponse({"status":False, "message":"Subcategory Already Exists"})
        else:
             await SubCategory.create(name=data.subcategory_name, category_id=data.category_id)
             return JSONResponse({"status":True, "message":"Subcategory Successfully Created"}, status_code=200)
     else:
            return JSONResponse({"status":False, "message":"Invalid Category ID"}, status_code=403)
 
@router.get('/subcategory/')
async def get_subcategory():
     return await SubCategory.all()

@router.put('/subcategory/')
async def update_subcategory(data:SubCategoryUpdateSchema):
     
     if SubCategory.exists(id = data.subcategory_id):
            await SubCategory.filter(id=data.subcategory_id).update(name=data.subcategory_name)
            return JSONResponse({"status":True, "message":"Subcategory Successfully Created"}, status_code=200) 
     else:
            return JSONResponse({"status":False, "message":"Invalid Subcategory ID"}, status_code=403)
     
@router.delete('/subcategory/')
async def delete_subcategory(data:SubCategoryDeleteSchema):
     if await SubCategory.exists(id=data.subcategory_id):
          await SubCategory.filter(id=data.subcategory_id).delete()
          return JSONResponse({"status":True, "message": "Subcategory Successfully Deleted"}, status_code=200)
     else:
          return JSONResponse({"status":False, "message":"Invalid Subcategory ID"}, status_code=403)

@router.post('/product_images/')
async def upload_product_image(file:UploadFile):
     FILEPATH = "static/product/"
     file_name = file.filename
     extention = file_name.split('.')[1]

     if extention not in ['png', 'jpg']:
          return JSONResponse({"status":False, "message":"Invalid Filetype"}, status_code=403)
     else:
          if not os.path.exists(FILEPATH):
                os.makedirs(FILEPATH)
        
          token_name = secrets.token_hex(10) + "." + extention
          generated_name = FILEPATH + token_name
          file_content = await file.read()

          with open(generated_name , 'wb') as file:
               file.write(file_content)

          img = Image.open(generated_name)
          img = img.resize(size = (500,500))
               
          await Photo.create(product_image=generated_name)
          return JSONResponse({"status":True, "message":"Photo Added Successfully"}, status_code=200)


async def upload_image(img):
    FILEPATH = "static/product/"
    if not os.path.isdir(FILEPATH):
        os.mkdir(FILEPATH)

    filename = img.filename
    image_name = filename.split('.')[0]
    extention = filename.split('.')[1]
    if extention not in ['jpg','png', "jpeg"]:
        return {"status":False, "message":"Image Extension Not Allowed"}
                
    dt = datetime.now()
    dt_timestamp = round(datetime.timestamp(dt))

    modified_image_name = image_name + "_" + str(dt_timestamp) + "." + extention
    generated_name = FILEPATH + modified_image_name
    file_content = await img.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)
        file.close()
    return generated_name
@router.post('/product/')
async def create_product(data:ProductSchema=Depends(),
                        file:UploadFile = File(...)):
     if await Category.exists(id=data.category_id):
            category_obj = await Category.get(id=data.category_id)
     else:
            return JSONResponse({"status":False, "message":"Invalid Category ID"}, status_code=403)
     
     if await SubCategory.exists(id=data.subcategory_id):
            subcategory_obj = await SubCategory.get(id=data.subcategory_id)
     else:
            return JSONResponse({"status":False, "message":"Invalid Sub-Category ID"}, status_code=403)

     if await Product.exists(name=data.name):
            return JSONResponse({"status":False, "message":"This product already exists!"}, status_code=403)
     else:
            image_url = await upload_image(file)

            await Product.create(
                 name=data.name,
                 description=data.description,
                 price=data.price,
                 discount_price=data.discount_price,
                 category=category_obj,
                 subcategory=subcategory_obj,
                 product_iamge=image_url
            )
            return JSONResponse({"status":True, "message":"Product Added Successfully"}, status_code=200)

@router.get('/product/')
async def get_product():
     return await Product.all()

@router.put('/product/')
async def update_product(data:ProductUpdateSchema=Depends(),
                         productfile:UploadFile = File(...)):
     if await Product.exists(id=data.product_id):
            image_url = await upload_image(productfile)

            await Product.filter(id=data.product_id).update(
                 name=data.name,
                 description=data.description,
                 price=data.price,
                 discount_price=data.discount_price,
                 product_iamge=image_url
            )
            return JSONResponse({"status":True, "message":"Product Update Successfully"}, status_code=200)
     else:
          return JSONResponse({"status":False, "message":"Invalid Product ID"}, status_code=403)
@router.delete('/product/')
async def delete_product(data:ProductDeleteSchema):
     if await Product.exists(id=data.product_id):
          await Product.filter(id=data.product_id).delete()
          return JSONResponse({"status":True, "message": "Product Successfully Deleted"}, status_code=200)
     else:
          return JSONResponse({"status":False, "message":"Invalid Product ID"}, status_code=403)