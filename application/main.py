from flask import jsonify
from .database import app
from application.routes.users import users
from application.routes.products import products
from application.routes.orders import orders
from application.routes.ratings import ratings
from application.routes.authorisation import login


app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(products, url_prefix='/products')
app.register_blueprint(orders, url_prefix='/orders')
app.register_blueprint(ratings, url_prefix='/ratings')


# Main page message
@app.route('/')
def index():
    return jsonify(message='Hello')


if __name__ == '__main__':
    app.run()