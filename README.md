About
===

eCommerce API is organised around RESTful principles. It resembles online shopping platforms, such as Amazon, eBay or Allegro, where users can sell and buy their products.

The API was created using Flask web framework. All the data is stored in PostgreSQL database, using SQLAlchemy as an ORM system. The API and database are deployed to Heroku, a cloud platform which allows the API to be accessed at anytime. It is hosted at the following domain: https://api-online-shopping.herokuapp.com/


## Documentation

Link to the Postman documentation: https://documenter.getpostman.com/view/19248285/UVeGr62D


## Authorization

eCommerce API uses an OAuth 2.0 authorization standard. In order to send POST, PUT or DEL requests (except account creation and log in), the user has to first create an account and log in using valid credentials. After logging in, the user will receive an access token which will have to be provided alongside aforementioned requests.

The token has to be passed as the request header "Authorization" together with a "Bearer" keyword: "Bearer <access token<blabla>>" (replace "<access token<blabla>>").


## Querying

All GET requests, except those which return a specific item, can include query parameters which take form of filters and sorting arguments.

**Filters**

Results can be filtered based on any attribute of a specific item, except its ID. For example when querying products, the following attributes can be used as filters: "name", "price", "seller_id", "category", "new" and "posted_at".
 
For example, to find products named "Wardrobe", the request would be: https://api-online-shopping.herokuapp.com/products?name=Wardrobe

Additionally, the API supports range filters for numeric attributes which work by adding range type to the name of attribute. The are two range types: "from" (equal or greater than) and "to" (equal or smaller than).
 
For example, to find products in the price range from 200 to 500, the request would be: https://api-online-shopping.herokuapp.com/products?price-from=200&price-to=500

**Sorting**

The query results can also be sorted by providing a "sorting" parameter with a value indicating the attribute to sort by and the sorting order.
  
For example, to list products from newest to oldest, the request would be: https://api-online-shopping.herokuapp.com/products?sorting=date-desc
