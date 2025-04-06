from apps.repository.productRepository import ProductRepository
from apps.exception.exceptions import ProductNotFoundError, CategoryNotFoundError
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def get_products(self):
        try:
            products = self.repo.get_all_products()
            if not products:
                raise ProductNotFoundError("No products found")
            return products
        except Exception as e:
            current_app.logger.error(f"Error getting products: {str(e)}")
            raise e

    def get_product_by_id(self, product_id):
        try:
            product = self.repo.get_product_by_id(product_id)
            if not product:
                raise ProductNotFoundError(f"Product with ID {product_id} not found.")
            return product
        except Exception as e:
            current_app.logger.error(f"Error getting product by ID {product_id}: {str(e)}")
            raise e

    def get_products_by_category(self, category_id):
        try:
            products = self.repo.get_products_by_category(category_id)
            if not products:
                raise CategoryNotFoundError(f"No products found in category with ID {category_id}.")
            return products
        except Exception as e:
            current_app.logger.error(f"Error getting products for category ID {category_id}: {str(e)}")
            raise e

    def add_product(self, data):
        try:
            product = self.repo.create_product(data)
            if not product:
                raise ValueError("Failed to create product.")
            return product
        except Exception as e:
            current_app.logger.error(f"Error adding product: {str(e)}")
            raise e

    def update_product(self, product_id, data):
        try:
            updated_product = self.repo.update_product(product_id, data)
            if not updated_product:
                raise ProductNotFoundError(f"Product with ID {product_id} not found or update failed.")
            return updated_product
        except Exception as e:
            current_app.logger.error(f"Error updating product with ID {product_id}: {str(e)}")
            raise e

    def delete_product(self, product_id):
        try:
            result = self.repo.delete_product(product_id)
            if not result:
                raise ProductNotFoundError(f"Product with ID {product_id} not found delete failed.")
            return {"message": f"Product with ID {product_id} deleted successfully."}
        except Exception as e:
            current_app.logger.error(f"Error deleting product with ID {product_id}: {str(e)}")
            raise e

    def get_categories(self):
        try:
            categories = self.repo.get_all_categories()
            if not categories:
                raise CategoryNotFoundError("No categories found.")
            return categories
        except Exception as e:
            current_app.logger.error(f"Error fetching categories: {str(e)}")
            raise e
