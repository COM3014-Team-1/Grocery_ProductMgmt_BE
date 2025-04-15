from apps.models.product import Product
from apps.models.category import Category
from apps.utils.db import db
import json

def seed_database():
    try:
        # Open and load the categories data
        with open("data/categories.json") as categories_file:
            categories_data = json.load(categories_file)
        
        # Open and load the products data
        with open("data/products.json") as products_file:
            products_data = json.load(products_file)
        
        # Add categories to the database
        for category_data in categories_data:
            category = Category(
                name=category_data['name'],
                description=category_data.get('description', '')
            )
            db.session.add(category)
        
        # Add products to the database
        for product_data in products_data:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity'],
                category_id=product_data['category_id'],
                image_url=product_data.get('image_url', None),
                rating=product_data.get('rating', 0.0),
                is_halal=product_data.get('is_halal', False),
                is_vegan=product_data.get('is_vegan', False)
            )
            db.session.add(product)
        
        # Commit the session to persist data
        db.session.commit()

        print("Database seeding completed successfully.")
    
    except Exception as e:
        db.session.rollback()
        print(f"Error while seeding the database: {e}")
