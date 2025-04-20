from flask import Blueprint, request, jsonify, current_app
from apps.services.productService import ProductService
from apps.schemas.productSchema import ProductSchema, ProductUpdateSchema
from apps.schemas.categorySchema import CategorySchema
from marshmallow import ValidationError
from apps.utils.errorHandler import handle_service_error
from flask_jwt_extended import jwt_required
from apps.utils.authenticator import roles_allowed

product_bp = Blueprint('product', __name__)

product_service = ProductService()

@product_bp.route('/products', methods=['GET'])
@jwt_required()
@roles_allowed(['user'])
def get_products():
    try:
        products = product_service.get_products()
        return jsonify([ProductSchema().dump(product) for product in products]), 200
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/products/<uuid:product_id>', methods=['GET'])
@jwt_required()
@roles_allowed(['user'])
def get_product_by_id(product_id):
    try:
        product = product_service.get_product_by_id(product_id)
        return jsonify(ProductSchema().dump(product)), 200
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/categories', methods=['GET'])
@jwt_required()
@roles_allowed(['user'])
def get_categories():
    try:
        categories = product_service.get_categories()
        return jsonify([CategorySchema().dump(category) for category in categories]), 200
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/products/category/<uuid:category_id>', methods=['GET'])
@jwt_required()
@roles_allowed(['user'])
def get_products_by_category(category_id):
    try:
        products = product_service.get_products_by_category(category_id)
        return jsonify([ProductSchema().dump(product) for product in products]), 200
    except Exception as e:
        return handle_service_error(e)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
@roles_allowed(['user'])
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
@jwt_required()
@roles_allowed(['user'])
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
@jwt_required()
@roles_allowed(['user'])
def delete_product(product_id):
    try:
        result = product_service.delete_product(product_id)
        return jsonify(result), 200
    except Exception as e:
        return handle_service_error(e)

# apps/controllers/productController.py

@product_bp.route('/products/search', methods=['GET'])
@jwt_required()
@roles_allowed(['user'])
def search_products():
    try:
        filters = {
            'name': request.args.get('name'),
            'min_price': float(request.args.get('min_price')) if request.args.get('min_price') else None,
            'max_price': float(request.args.get('max_price')) if request.args.get('max_price') else None,
            'category_id': request.args.get('category_id'),
            'is_halal': request.args.get('is_halal') == 'true' if request.args.get('is_halal') else None,
            'is_vegan': request.args.get('is_vegan') == 'true' if request.args.get('is_vegan') else None,
            'min_rating': float(request.args.get('min_rating')) if request.args.get('min_rating') else None,
        }

        products = product_service.search_products(filters)  # Calling the search_products method here
        return jsonify([ProductSchema().dump(product) for product in products]), 200
    except Exception as e:
        return handle_service_error(e)


@product_bp.route('/products/check_availability', methods=['POST'])
@jwt_required()
@roles_allowed(['user'])
def check_product_avaliability():
    try:
        data=request.get_json()
        current_app.logger.info("check the product avalibility"+str(data))
        product_ids=data.get('product_ids',[])
        result = product_service.check_product_avalibility(product_ids)
        return jsonify(result), 200
    except Exception as e:
        return handle_service_error(e)
