from apps.models.category import Category
from apps.utils.db import db

class CategoryRepository:
    def get_all_categories(self):
        return Category.query.all()

    def get_category_by_id(self, category_id):
        return Category.query.get(category_id)

    def create_category(self, data):
        category = Category(**data)
        db.session.add(category)
        db.session.commit()
        return category

    def delete_category(self, category_id):
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
        return category
