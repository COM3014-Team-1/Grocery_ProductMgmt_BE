from flask import Blueprint, request, jsonify, current_app
from apps.services.categoryService import CategoryService
from apps.schemas.categorySchema import CategorySchema
from marshmallow import ValidationError
from apps.utils.errorHandler import handle_service_error 
from flask_jwt_extended import jwt_required 
from apps.utils.authenticator import roles_allowed

category_bp = Blueprint('category', __name__)

category_service = CategoryService()

@category_bp.route('/categories', methods=['GET'])
@jwt_required()
@roles_allowed(['user'])
def get_categories():
    try:
        categories = category_service.get_categories()
        schema = CategorySchema(many=True)
        # The 'category_imageurl' will now be part of the response due to the updated schema
        return jsonify(schema.dump(categories)), 200
    except Exception as e:
        return handle_service_error(e)

@category_bp.route('/categories/<uuid:category_id>', methods=['GET'])
@jwt_required()
@roles_allowed(['user'])
def get_category(category_id):
    try:
        category = category_service.get_category_by_id(category_id)
        schema = CategorySchema()
        # The 'category_imageurl' will now be part of the response due to the updated schema
        return jsonify(schema.dump(category)), 200
    except Exception as e:
        return handle_service_error(e)

@category_bp.route('/categories', methods=['POST'])
@jwt_required()
@roles_allowed(['user'])
def add_category():
    try:
        data = request.get_json()
        schema = CategorySchema()
        validated_data = schema.load(data)
        
        # Ensure 'category_imageurl' is included in the request body and passed to the service
        category = category_service.add_category(validated_data)
        return jsonify(schema.dump(category)), 201
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    except Exception as e:
        return handle_service_error(e)

@category_bp.route('/categories/<uuid:category_id>', methods=['DELETE'])
@jwt_required()
@roles_allowed(['user'])
def delete_category(category_id):
    try:
        result = category_service.delete_category(category_id)
        return jsonify(result), 200
    except Exception as e:
        return handle_service_error(e)
