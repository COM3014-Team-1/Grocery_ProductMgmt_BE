class ProductNotFoundError(Exception):
    """Exception raised when a product is not found."""
    pass

class CategoryNotFoundError(Exception):
    """Exception raised when a category is not found."""
    pass

class DatabaseError(Exception):
    """Exception raised for general database-related issues."""
    pass