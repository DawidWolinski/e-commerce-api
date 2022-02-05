from operator import and_
from flask import Blueprint, request, jsonify
from ..oauth2 import token_required
from ..schemas import order_schema, order_product_schema, orders_product_schema
from ..models import Order, Product
from ..database import db
from ..utils import get_filter_expressions, get_sorting_parameters, lower_case_args
from sqlalchemy import and_


orders = Blueprint('orders', __name__)


@orders.route('/', methods=['POST'], strict_slashes=False)
@token_required
def order_product(current_user):
    data = request.get_json()
    error = order_schema.validate(data)
    if error:
        return jsonify(error=error), 400

    product = Product.query.get(data['product_id'])
    if product == None:
        return jsonify(error='Product with a given ID was not found'), 404

    if current_user.id == product.user.id:
        return jsonify(error='The IDs of buyer and seller are the same'), 400
    
    data = lower_case_args(data)

    new_order = Order(user=current_user, **data)
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)


@orders.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get(id)
    return order_product_schema.jsonify(order)


@orders.route('/', methods=['GET'])
def query_orders():
    params = request.args.to_dict()

    sorting = get_sorting_parameters(params, Order) 
    expressions = get_filter_expressions(params, Order)

    results = Order.query.filter_by(**params).filter(and_(*expressions))\
    .order_by(sorting['order'](sorting['category']))

    results = orders_product_schema.dump(results)

    return jsonify(orders=results)