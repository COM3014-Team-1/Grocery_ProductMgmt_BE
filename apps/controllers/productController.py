from flask import Blueprint, request, jsonify, current_app
from apps.services.productService import ProductService
from apps.schemas.productSchema import ProductSchema, ProductUpdateSchema
from apps.schemas.categorySchema import CategorySchema
from marshmallow import ValidationError
from apps.utils.errorHandler import handle_service_error

product_bp = Blueprint('product', __name__)

product_service = ProductService()

@product_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = product_service.get_products()
        return jsonify([ProductSchema().dump(product) for product in products]), 200
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/products/<uuid:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        product = product_service.get_product_by_id(product_id)
        return jsonify(ProductSchema().dump(product)), 200
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = product_service.get_categories()
        return jsonify([CategorySchema().dump(category) for category in categories]), 200
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/products/category/<uuid:category_id>', methods=['GET'])
def get_products_by_category(category_id):
    try:
        products = product_service.get_products_by_category(category_id)
        return jsonify([ProductSchema().dump(product) for product in products]), 200
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        schema = ProductSchema()
        validated_data = schema.load(data)
        product = product_service.add_product(validated_data)        
        return jsonify(schema.dump(product)), 201
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/products/<uuid:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()
        schema = ProductUpdateSchema()
        validated_data = schema.load(data)
        updated_product = product_service.update_product(product_id, validated_data)
        return jsonify(ProductSchema().dump(updated_product)), 200
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/products/<uuid:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        result = product_service.delete_product(product_id)
        return jsonify(result), 200
    except Exception as e:
        return handle_service_error(e)
