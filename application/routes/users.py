from flask import Blueprint, request, jsonify
from utils import hash_password, get_sorting_parameters, get_filter_expressions
from schemas import user_schema, products_schema, user_schema_password,\
password_update_schema, orders_product_schema, ratings_order_product_schema
from models import User, Product, Order, Rating
from database import db
from oauth2 import token_required
from sqlalchemy import and_


users = Blueprint('users', __name__)


@users.route('/', methods=['POST'], strict_slashes=False)
def create_user():
    data = request.get_json()

    error = user_schema_password.validate(data)
    if error:
        return jsonify(error=error), 400

    hashed_password = hash_password(data['password'])
    data['password'] = hashed_password

    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201


@users.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


@users.route('/<int:id>/products', methods=['GET'])
def query_user_products_for_sale(id):
    params = request.args.to_dict()

    if 'seller_id' in params:
        return jsonify(error='It is not possible to change seller_id in this route'), 400

    params['seller_id'] = id
   
    sorting = get_sorting_parameters(params, Product) 
    expressions = get_filter_expressions(params, Product)
    
    results = Product.query.filter_by(**params).filter(and_(*expressions)).outerjoin(Order)\
    .where(Order.product_id == None).order_by(sorting['order'](sorting['category']))

    results = products_schema.dump(results)

    return jsonify(products=results)


@users.route('/<int:id>/orders', methods=['GET'])
def query_user_orders(id):
    params = request.args.to_dict()

    if 'buyer_id' in params:
        return jsonify(error='It is not possible to change buyer_id in this route'), 400
 
    params['buyer_id'] = id

    sorting = get_sorting_parameters(params, Order) 
    expressions = get_filter_expressions(params, Order)

    if 'unrated' in params:
        del params['unrated']
        results = Order.query.filter_by(**params).filter(and_(*expressions))\
        .outerjoin(Rating).where(Rating.id == None).order_by(sorting['order'](sorting['category']))
    else:
        results = Order.query.filter_by(**params).filter(and_(*expressions))\
        .order_by(sorting['order'](sorting['category']))
    
    results = orders_product_schema.dump(results)

    return jsonify(orders=results)
    

@users.route('/<int:id>/ratings', methods=['GET'])
def query_user_ratings(id):

    params = request.args.to_dict()
    
    sorting = get_sorting_parameters(params, Rating) 
    expressions = get_filter_expressions(params, Rating)

    results = Rating.query.filter_by(**params).filter(and_(*expressions)).join(Order)\
    .join(Product).join(User).filter_by(id=id).order_by(sorting['order'](sorting['category']))

    results = ratings_order_product_schema.dump(results)

    return jsonify(ratings=results)
    

@users.route('/', methods=['PUT'], strict_slashes=False)
@token_required
def change_user_password(current_user):
    
    new_password = request.get_json()
    error = password_update_schema.validate(new_password)
    if error:
        return jsonify(error=error), 400

    current_user.password = hash_password(new_password['password'])
    
    db.session.commit()

    return jsonify(message='Password updated'), 200
