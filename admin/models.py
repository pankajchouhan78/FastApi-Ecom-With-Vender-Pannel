from tortoise.models import Model
from tortoise import fields

class User(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(50)
    email=fields.CharField(255,unique=True)
    password=fields.CharField(100)
    city=fields.CharField(100)
    address=fields.CharField(200)

class Category(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(100, unique=True)
    is_active=fields.BooleanField(default=True)
    created_at=fields.DatetimeField(auto_now_add=True)
    updated_at=fields.DatetimeField(auto_now=True)
class SubCategory(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(200, unique=True)
    slug = fields.CharField(30)
    category = fields.ForeignKeyField("models.Category", related_name="subcategory", on_delete="CASCADE")
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class SubCategory(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(200, unique=True)
    category= fields.ForeignKeyField("models.Category", related_name="subcategory", on_delete="CASCADE")
    is_active = fields.BooleanField(default=True)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class Photo(Model):
    product_image = fields.TextField()
