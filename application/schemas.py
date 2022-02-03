from database import app
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate


# Init ma
ma = Marshmallow(app)


# User
class UserSchema(ma.Schema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    creation_date = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        fields = ('id', 'username', 'email', 'creation_date')
        ordered = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserSchemaPassword(UserSchema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'creation_date')
        ordered = True
    
user_schema_password = UserSchemaPassword()


class PasswordUpdateSchema(ma.Schema):
    password = fields.String(required=True, validate=validate.Length(min=6))

password_update_schema = PasswordUpdateSchema()


# Product
class ProductSchema(ma.Schema):
    id = fields.Integer()
    seller_id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=1))
    category = fields.String(required=True, validate=validate.Length(min=1))
    new = fields.Boolean(required=True)
    posted_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        ordered = True

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class ProductUpdateSchema(ma.Schema):
    name = fields.String(validate=validate.Length(min=1))
    price = fields.Float(validate=validate.Range(min=1))
    category = fields.String(validate=validate.Length(min=1))
    new = fields.Boolean()
    posted_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        ordered = True

product_update_schema = ProductUpdateSchema()


# Order
class OrderSchema(ma.Schema):
    id = fields.Integer()
    buyer_id = fields.Integer()
    product_id = fields.Integer(required=True)
    shipment_method = fields.String(required=True, validate=validate.Length(min=1))
    ordered_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        ordered = True

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


class OrderProductSchema(ma.Schema):
    id = fields.Integer()
    buyer_id = fields.Integer(required=True)
    product_id = fields.Integer(required=True)
    shipment_method = fields.String(required=True)
    ordered_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    product = fields.Nested(ProductSchema)

    class Meta:
        ordered = True

order_product_schema = OrderProductSchema()
orders_product_schema = OrderProductSchema(many=True)


# Rating
class RatingSchema(ma.Schema):
    id = fields.Integer()
    order_id = fields.Integer(required=True)
    rating = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.String()
    rated_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        ordered = True

rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)


class RatingOrderProductSchema(ma.Schema):
    id = fields.Integer()
    order_id = fields.Integer(required=True)
    rating = fields.Integer(required=True, min=1, max=5)
    comment = fields.String()
    rated_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    order = fields.Nested(OrderProductSchema)

    class Meta:
        ordered = True

rating_order_product_schema = RatingOrderProductSchema()
ratings_order_product_schema = RatingOrderProductSchema(many=True)


# Login
class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

    class Meta:
        ordered = True

login_schema = LoginSchema()





