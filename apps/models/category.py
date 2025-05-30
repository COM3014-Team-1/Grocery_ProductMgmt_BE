from datetime import datetime, timezone
from apps.utils.db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_imageurl = db.Column(db.String(255))  
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        """Serialize category object to dictionary for response"""
        return {
            "category_id": str(self.category_id),
            "name": self.name,
            "description": self.description,
            "category_imageurl": self.category_imageurl,  
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
