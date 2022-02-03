from passlib.context import CryptContext
from sqlalchemy import asc, desc


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Returns sorting parameters based on HTTP query parameters
# Sorting parameter value format in the HTTP request: category-order
# Category represents a column in the table by which the results will be sorted
# Examples: sorting=price-asc, sorting=date-desc, sorting=rating-asc
def get_sorting_parameters(params: dict, Table):

    # Each table has different name for date, hence date will be replaced with one of the following
    date_keywords = {'user': 'creation_date', 
                    'product': 'posted_at', 
                    'order': 'ordered_at', 
                    'rating': 'rated_at'}

    # By default sorting is set to descending by date
    sorting = {'category': getattr(Table, date_keywords[Table.__tablename__]), 'order': desc}

    # If 'sorting' keyword is present, the category and order are separated and put into two variables
    if 'sorting' in params:
        sorting_argument = params['sorting']
        delimiter = sorting_argument.rfind('-')
        order = sorting_argument[(delimiter+1):len(sorting_argument)]
        category = sorting_argument[0:(delimiter)]
        
        if category == 'date':
            category = date_keywords[Table.__tablename__]
        
        if order == 'asc':
            sorting['order'] = asc
        
        # User can provide any category as long as it matches the name of the column 
        # in the table to be sorted
        sorting['category'] = getattr(Table, category)

        del params['sorting']
    
    return sorting


# Returns range filter expressions based on HTTP query parameters
# Range parameters keyword formats in the HTTP request: category-from (minimum value) or/and 
# category-to=maximum value
# Examples: rating-from=2, price-from=40&price-to=200 
def get_filter_expressions(params: dict, Table):
  
    expressions = []
    params_to_delete = []

    for param in params:
        if '-from' in param:
            delimiter = param.find('-from')
            category = param[0:(delimiter)]
            expressions.append(getattr(Table, category) >= params[param])
            params_to_delete.append(param)
        elif 'to' in param:
            delimiter = param.find('-to')
            category = param[0:(delimiter)]
            expressions.append(getattr(Table, category) <= params[param])
            params_to_delete.append(param)

    for param in params_to_delete:
        del params[param]

    return expressions