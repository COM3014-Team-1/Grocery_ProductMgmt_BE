from flask import jsonify, current_app
from apps.exception.exceptions import ProductNotFoundError, CategoryNotFoundError
from sqlalchemy.exc import SQLAlchemyError

def handle_service_error(error):
    """Centralized error handler that handles known service errors and returns appropriate responses with logging."""
    if isinstance(error, ValueError):
        current_app.logger.error(f"ValueError: {error}")
        return jsonify({"message": str(error)}), 404
    elif isinstance(error, ProductNotFoundError):
        current_app.logger.error(f"ProductNotFoundError: {error}")
        return jsonify({"message": str(error)}), 404
    elif isinstance(error, CategoryNotFoundError):
        current_app.logger.error(f"CategoryNotFoundError: {error}")
        return jsonify({"message": str(error)}), 404
    elif isinstance(error, SQLAlchemyError):
        current_app.logger.error(f"Database error: {error}")
        return jsonify({"message": "Database error occurred."}), 500
    else:
        current_app.logger.error(f"Unexpected error: {error}")
        return jsonify({"message": "Unexpected error occurred", "error": str(error)}), 500