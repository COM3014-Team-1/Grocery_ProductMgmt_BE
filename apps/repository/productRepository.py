from apps.models.product import Product
from apps.utils.db import db
from apps.models.category import Category

class ProductRepository:
    def get_all_products(self):
        return Product.query.all()

    def get_product_by_id(self, product_id):
        return Product.query.get(product_id)

    def get_products_by_category(self, category_id):
        return Product.query.filter_by(category_id=category_id).all()

    def create_product(self, data):
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        return product

    def update_product(self, product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return product

    def delete_product(self, product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
        return product

    def get_all_categories(self):
        return Category.query.all()
