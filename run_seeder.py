import json
import uuid
from datetime import datetime
from app import create_app
from apps.models.product import Product
from apps.models.category import Category
from apps.utils.db import db

app = create_app()

with app.app_context():
    try:
        # Load categories
        with open('categories.json') as f:
            categories_data = json.load(f)
        category_id_map = {}

        for category in categories_data:
            new_category = Category(
                category_id=str(uuid.uuid4()),  # assuming UUID is used
                name=category['name'],
                description=category['description'],
            )
            db.session.add(new_category)
            db.session.flush()  # get ID before commit
            category_id_map[category['name']] = new_category.category_id

        # Load products
        with open('products.json') as f:
            products_data = json.load(f)

        for product in products_data:
            category_uuid = category_id_map.get(product['category_name'])  # use name, not ID
            if not category_uuid:
                print(f"Category not found for product: {product['name']}")
                continue

            new_product = Product(
                product_id=str(uuid.uuid4()),
                name=product['name'],
                description=product['description'],
                price=product['price'],
                quantity=product['quantity'],
                category_id=category_uuid,
                image_url=product.get('image_url', ''),
                rating=product.get('rating', 0),
                is_halal=product.get('is_halal', False),
                is_vegan=product.get('is_vegan', False),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_product)

        db.session.commit()
        print("Database seeding completed successfully.")
    except Exception as e:
        print("Error while seeding the database:", e)
