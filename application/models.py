from database import db
from sqlalchemy import text

# Database table models

class User(db.Model):
    __tablename__ = 'user'

    # Columns
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    # Relationships
    products = db.relationship('Product', backref='user')
    orders = db.relationship('Order', backref='user')
    

class Product(db.Model):
    __tablename__ = 'product'

    # Columns
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    new = db.Column(db.Boolean, nullable=False)
    posted_at = db.Column(db.TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    # Relationships
    order = db.relationship('Order', backref='product', uselist=False)
    


class Order(db.Model):
    __tablename__ = 'order'

    # Columns
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), unique=True, nullable=False)
    shipment_method = db.Column(db.String(200), nullable=False)
    ordered_at = db.Column(db.TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    # Relationships
    rating = db.relationship('Rating', backref='order', uselist=False)


class Rating(db.Model):
    __tablename__ = 'rating'

    # Columns
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500))
    rated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)