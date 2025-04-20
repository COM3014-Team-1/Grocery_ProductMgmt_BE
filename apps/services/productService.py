from apps.repository.productRepository import ProductRepository
from apps.exception.exceptions import ProductNotFoundError, CategoryNotFoundError
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError



class ProductService:
    def __init__(self):
        self.repo = ProductRepository()  # Use 'repo' here to match your init method

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

    def search_products(self, filters):
        try:
            products = self.repo.get_products_by_search_criteria(
                name=filters.get('name'),
                min_price=filters.get('min_price'),
                max_price=filters.get('max_price'),
                category_id=filters.get('category_id'),
                is_halal=filters.get('is_halal'),
                is_vegan=filters.get('is_vegan'),
                min_rating=filters.get('min_rating')
            )
            return products
        except Exception as e:
            current_app.logger.error(f"Error searching products: {str(e)}")
            raise e
        
    def check_product_avalibility(self, products_list):
        try:
            product_ids = [str(item['product_id']) for item in products_list]
            products = self.repo.get_all_poducts(product_ids)
            requested_quantities = {
                str(item['product_id']): item['quantity'] for item in products_list
            }
            result = []
            for product in products:
                requested_qty = requested_quantities.get(str(product.product_id), 0)
                result.append( {
                    "product_id":product.product_id,
                    "in_stock": product.quantity >= requested_qty,
                    "available_quantity": product.quantity,
                    "requested_quantity": requested_qty
                })
            current_app.logger.info("Result of products from order service: " + str(result))
            return result
        except Exception as e:
            current_app.logger.error(f"Error checking product availability: {str(e)}")
            raise e