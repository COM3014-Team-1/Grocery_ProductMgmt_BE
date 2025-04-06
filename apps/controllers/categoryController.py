from flask import Blueprint, request, jsonify, current_app
from apps.services.categoryService import CategoryService
from apps.schemas.categorySchema import CategorySchema
from marshmallow import ValidationError
from apps.utils.errorHandler import handle_service_error  

category_bp = Blueprint('category', __name__)

category_service = CategoryService()

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = category_service.get_categories()
        schema = CategorySchema(many=True)
        return jsonify(schema.dump(categories)), 200
    except Exception as e:
        return handle_service_error(e) 

@category_bp.route('/categories/<uuid:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = category_service.get_category_by_id(category_id)
        schema = CategorySchema()
        return jsonify(schema.dump(category)), 200
    except Exception as e:
        return handle_service_error(e)

@category_bp.route('/categories', methods=['POST'])
def add_category():
    try:
        data = request.get_json()
        schema = CategorySchema()
        validated_data = schema.load(data) 
        category = category_service.add_category(validated_data)
        return jsonify(schema.dump(category)), 201
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    except Exception as e:
        return handle_service_error(e)  

@category_bp.route('/categories/<uuid:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        result = category_service.delete_category(category_id)
        return jsonify(result), 200
    except Exception as e:
        return handle_service_error(e) 
