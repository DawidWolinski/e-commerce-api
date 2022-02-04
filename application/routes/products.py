from flask import Blueprint, request, jsonify
from ..utils import get_sorting_parameters, get_filter_expressions
from ..schemas import product_schema, products_schema, product_update_schema
from ..models import Product, Order
from ..database import db
from ..oauth2 import token_required
from sqlalchemy import and_


products = Blueprint('products', __name__)


@products.route('/', methods=['POST'], strict_slashes=False)
@token_required
def add_product(current_user):
    data = request.get_json()
    error = product_schema.validate(data)
    if error:
        return jsonify(error=error), 400

    new_product = Product(user=current_user, **data)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201


@products.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


@products.route('/', methods=['GET'])
def query_products():
    params = request.args.to_dict()

    sorting = get_sorting_parameters(params, Product) 
    expressions = get_filter_expressions(params, Product)
    
    results = Product.query.filter_by(**params).filter(and_(*expressions)).\
    order_by(sorting['order'](sorting['category']))
    
    results = products_schema.dump(results)

    return jsonify(products=results)


@products.route('/for-sale', methods=['GET'])
def query_products_for_sale():
    params = request.args.to_dict()

    sorting = get_sorting_parameters(params, Product) 
    expressions = get_filter_expressions(params, Product)

    results = Product.query.filter_by(**params).filter(and_(*expressions)).\
    outerjoin(Order).where(Order.product_id == None).order_by(sorting['order'](sorting['category']))
    
    results = products_schema.dump(results)

    return jsonify(products=results)


@products.route('/<int:id>', methods=['PUT'], strict_slashes=False)
@token_required
def update_product(current_user, id):
    product = Product.query.get(id)

    if product == None:
        return jsonify(error='Product not found'), 404
        
    if product.seller_id != current_user.id:
        return jsonify(error='This product belongs to the user with a different ID'), 400

    if product.order != None:
        return jsonify(error='Sold products cannot be edited'), 400

    data = request.get_json()
    error = product_update_schema.validate(data)
    if error:
        return jsonify(error=error), 400

    for key in data:
        setattr(product, key, data[key])
    
    db.session.commit()
   
    return product_schema.jsonify(product)


@products.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
@token_required
def delete_product(current_user, id):
    product = Product.query.get(id)

    if product == None:
        return jsonify(error='Product not found'), 404
    
    if product.seller_id != current_user.id:
        return jsonify(error='This product belongs to the user with a different ID'), 400

    if product.order != None:
        return jsonify(error='Sold products cannot be removed'), 400
    
    db.session.delete(product)
    db.session.commit()

    return ('', 204)

