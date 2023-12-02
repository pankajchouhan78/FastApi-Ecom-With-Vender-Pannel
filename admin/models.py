from tortoise.models import Model
from tortoise import fields

class User(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(50)
    email=fields.CharField(255,unique=True)
    password=fields.CharField(100)
    city=fields.CharField(100)
    address=fields.CharField(200)
