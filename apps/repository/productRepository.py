from apps.models.product import Product
from apps.utils.db import db
from apps.models.category import Category
from sqlalchemy import or_


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

    def get_products_by_search_criteria(self, name=None, min_price=None, max_price=None,
                        category_id=None, is_halal=None, is_vegan=None, min_rating=None):
        query = Product.query

        if name:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{name}%"),
                    Product.description.ilike(f"%{name}%")
                )
            )

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        if category_id:
            query = query.filter(Product.category_id == category_id)

        if is_halal is not None:
            query = query.filter(Product.is_halal == is_halal)

        if is_vegan is not None:
            query = query.filter(Product.is_vegan == is_vegan)

        if min_rating is not None:
            query = query.filter(Product.rating >= min_rating)

        return query.all()
