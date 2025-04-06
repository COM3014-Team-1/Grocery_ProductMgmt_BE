from apps.repository.categoryRepository import CategoryRepository
from apps.exception.exceptions import CategoryNotFoundError, DatabaseError
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def get_categories(self):
        try:
            categories = self.repo.get_all_categories()
            if not categories:
                raise CategoryNotFoundError("No categories found.")
            return categories
        except Exception as e:
            current_app.logger.error(f"Error in get_categories: {str(e)}")
            raise e

    def get_category_by_id(self, category_id):
        try:
            category = self.repo.get_category_by_id(category_id)
            if not category:
                raise CategoryNotFoundError(f"Category with ID {category_id} not found.")
            return category
        except Exception as e:
            current_app.logger.error(f"Error in get_category_by_id: {str(e)}")
            raise e

    def add_category(self, data):
        try:
            category = self.repo.create_category(data)
            if not category:
                raise ValueError("Failed to create category.")
            return category
        except Exception as e:
            current_app.logger.error(f"Error in add_category: {str(e)}")
            raise e

    def delete_category(self, category_id):
        try:
            success = self.repo.delete_category(category_id)
            if not success:
                raise CategoryNotFoundError(f"Category with ID {category_id} not found for deletion.")
            return {"message": f"Category with ID {category_id} deleted successfully."}
        except Exception as e:
            current_app.logger.error(f"Error in delete_category: {str(e)}")
            raise e
