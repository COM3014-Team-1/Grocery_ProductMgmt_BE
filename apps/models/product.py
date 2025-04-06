from datetime import datetime, timezone
from apps.utils.db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.category_id'), nullable=False)
    image_url = db.Column(db.String, nullable=True)
    rating = db.Column(db.Numeric(2, 1), default=0.0) 
    is_halal = db.Column(db.Boolean, default=False)
    is_vegan = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    def __init__(self, name, description, price, quantity, category_id, image_url=None, rating=0.0, is_halal=False, is_vegan=False):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category_id = category_id
        self.image_url = image_url
        self.rating = rating
        self.is_halal = is_halal
        self.is_vegan = is_vegan

    def serialize(self):
        """Serialize product object to dictionary for response"""
        return {
            "product_id": str(self.product_id),
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "quantity": self.quantity,
            "category_id": str(self.category_id),
            "image_url": self.image_url,
            "rating": str(self.rating),
            "is_halal": self.is_halal,
            "is_vegan": self.is_vegan,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
