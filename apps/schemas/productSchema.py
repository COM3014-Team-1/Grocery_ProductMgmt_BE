from marshmallow import Schema, fields

from marshmallow import Schema, fields, post_load
from apps.models.product import Product
import uuid

class ProductSchema(Schema):
    product_id = fields.UUID()
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    price = fields.Decimal(required=True, as_string=True)
    quantity = fields.Int(required=True)
    category_id = fields.UUID(required=True)
    image_url = fields.Str(allow_none=True)
    rating = fields.Decimal(as_string=True, default=0.0)
    is_halal = fields.Boolean(default=False)
    is_vegan = fields.Boolean(default=False)
    created_at = fields.DateTime(dump_only=True)

class ProductUpdateSchema(Schema):
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    price = fields.Decimal(allow_none=True, as_string=True)
    quantity = fields.Int(allow_none=True)
    category_id = fields.UUID(allow_none=True)
    image_url = fields.Str(allow_none=True)
    rating = fields.Decimal(allow_none=True, as_string=True)
    is_halal = fields.Boolean(allow_none=True)
    is_vegan = fields.Boolean(allow_none=True)
