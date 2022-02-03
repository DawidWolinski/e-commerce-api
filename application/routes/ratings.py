from flask import Blueprint, request, jsonify
from schemas import rating_schema, ratings_order_product_schema
from models import Rating, Order
from database import db
from utils import get_sorting_parameters, get_filter_expressions
from oauth2 import token_required
from sqlalchemy import and_


ratings = Blueprint('ratings', __name__)


@ratings.route('/', methods=['POST'], strict_slashes=False)
@token_required
def add_rating(current_user):
    data = request.get_json()
    error = rating_schema.validate(data)
    if error:
        return jsonify(error=error), 400

    order = Order.query.get(data['order_id'])

    if order.rating != None:
        return jsonify(error='This order has already been rated'), 400
    elif order.buyer_id != current_user.id:
        return jsonify(error='IDs of this user and buyer are different'), 400
    
    new_rating = Rating(order=order, **data)
    db.session.add(new_rating)
    db.session.commit()

    return rating_schema.jsonify(new_rating)


@ratings.route('/<int:id>', methods=['GET'])
def get_rating(id):
    rating = Rating.query.get(id)
    return rating_schema.jsonify(rating)


@ratings.route('/', methods=['GET'])
def query_ratings():
    params = request.args.to_dict()
    
    sorting = get_sorting_parameters(params, Rating) 
    expressions = get_filter_expressions(params, Rating)

    results = Rating.query.filter_by(**params).filter(and_(*expressions))\
    .order_by(sorting['order'](sorting['category']))

    results = ratings_order_product_schema.dump(results)

    return jsonify(ratings=results)