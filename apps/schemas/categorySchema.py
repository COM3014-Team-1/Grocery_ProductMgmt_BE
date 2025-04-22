from marshmallow import Schema, fields, post_load
from apps.models.category import Category
import uuid

class CategorySchema(Schema):
    category_id = fields.UUID()
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    category_imageurl = fields.Str(allow_none=True)