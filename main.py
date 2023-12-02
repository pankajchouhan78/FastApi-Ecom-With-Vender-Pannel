from  fastapi import FastAPI
from admin import api as Apirouter
from tortoise.contrib.fastapi import register_tortoise

app=FastAPI()
app.include_router(Apirouter.router)

register_tortoise(
    app,
    db_url="postgres://postgres:8821@127.0.0.1/ecomdata",
    modules={'models':['admin.models',]},
    generate_schemas=True,
    add_exception_handlers=True
)