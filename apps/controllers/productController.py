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

# apps/controllers/productController.py

@product_bp.route('/products/search', methods=['GET'])
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
    
@product_bp.route('/products/update-quantity', methods=['PUT'])
def update_product_quantities():
    try:
        data = request.get_json()
        products=data.get('product_ids',[])
        current_app.logger.info("update the products"+str(data))
        if not isinstance(products, list):
            return jsonify({"message": "Expected a list of products with quantity changes."}), 400
        result = product_service.update_product_quantities(products)
        return jsonify(result), 400 if result.get("errors") else 200
    except Exception as e:
        return handle_service_error(e)