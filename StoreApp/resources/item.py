from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..schemas import ItemSchema, ItemUpdateSchema

from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError             # The SQLAlchemyError class is imported from the sqlalchemy.exc module. This class represents a general exception that can occur during database operations using SQLAlchemy. It serves as a base class for various specific exceptions related to database errors, allowing you to catch and handle these exceptions in your code.

from ..db import db          # The db object is imported from the db module. This object is an instance of SQLAlchemy and provides the necessary functionality to interact with the database, including creating tables, executing queries, and managing database sessions.
from ..models import ItemModel          # The ItemModel class is imported from the models module. This class represents the structure and behavior of the "items" table in the database and is used to create, retrieve, update, and delete item records in the database.



blp = Blueprint("Items", __name__, description="Operations on items")       # blp is a Blueprint object that is used to define routes and views related to items. It allows you to group related routes together, making your code more modular and easier to maintain.

@blp.route("/item/<int:item_id>")         # This decorator defines a route for the Item class, which handles requests related to a specific item identified by its item_id. The <string:item_id> part indicates that the item_id is expected to be a string parameter in the URL.
class Item(MethodView):              # The Item class inherits from MethodView, which allows you to define HTTP methods (GET, DELETE, PUT) as class methods. Each method corresponds to a specific HTTP request type and handles the logic for that request.

    @jwt_required()
    @blp.response(200, ItemSchema)             # The @blp.response decorator is used to specify the response schema for the get method. It indicates that the response will be serialized using the ItemSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.
    def get(self, item_id):               # The get method retrieves an item based on its item_id. It attempts to return the item from the items dictionary. If the item_id does not exist, it raises a 404 error using abort, indicating that the item was not found.

        # ************************************ 

        # try:
        #     return items[item_id]
        # except KeyError:
        #     abort(404, message="Item not found")

        # ************************************ 

        item = ItemModel.query.get_or_404(item_id)          # The query.get_or_404 method is called on the ItemModel class to retrieve an item from the database based on its item_id. If the item is not found, it automatically raises a 404 error, indicating that the item was not found. This provides a convenient way to handle item retrieval and error handling in a single line of code.
        return item          # The retrieved item is returned as the response to the GET request. It will be serialized using the ItemSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.

    @jwt_required()
    def delete(self, item_id):           # The delete method removes an item based on its item_id. It attempts to delete the item from the items dictionary. If the item_id does not exist, it raises a 404 error using abort, indicating that the item was not found.

        # ************************************ 

        # try:
        #     del items[item_id]
        #     return {"message": "Item deleted"}
        # except KeyError:
        #     abort(404, message="Item not found")

        # ************************************ 

        jwt = get_jwt()
        if jwt.get("role") != "admin":          # The get_jwt function is called to retrieve the JWT (JSON Web Token) from the request. It returns a dictionary containing the claims (payload) of the token. The code checks if the "role" claim in the JWT is not equal to "admin". If the user does not have an admin role, it raises a 401 error using abort, indicating that admin privileges are required to perform the delete operation.
            abort(401, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)          # The query.get_or_404 method is called on the ItemModel class to retrieve an item from the database based on its item_id. If the item is not found, it automatically raises a 404 error, indicating that the item was not found. This provides a convenient way to handle item retrieval and error handling in a single line of code.
        # ************************************ 
        # raise NotImplementedError("Delete functionality is not implemented yet.")          # A NotImplementedError is raised to indicate that the delete functionality has not been implemented yet. This serves as a placeholder for future implementation and informs developers that the delete operation is not currently supported.
        # ************************************ 
        db.session.delete(item)          # The delete method of the db.session object is called to mark the retrieved item for deletion from the database. This prepares the item for removal from the database.
        db.session.commit()          # The commit method of the db.session object is called to save the changes to the database, effectively deleting the item.
        return {"message": "Item deleted"}          # A JSON response is returned with a message indicating that the item has been successfully deleted. This provides feedback to the client about the outcome of the DELETE request.


    @jwt_required()
    @blp.arguments(ItemUpdateSchema)             # The @blp.arguments decorator is used to validate and deserialize the incoming request data based on the ItemUpdateSchema defined in schemas.py. It ensures that the request payload adheres to the specified schema, allowing for automatic validation and conversion of the data into a Python dictionary.
    @blp.response(200, ItemSchema)             # The @blp.response decorator is used to specify the response schema for the put method. It indicates that the response will be serialized using the ItemSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.
    def put(self, item_data, item_id):             # The put method updates an existing item based on its item_id. It retrieves the JSON payload from the request and attempts to update the corresponding item in the items dictionary. If the item_id does not exist, it raises a 404 error using abort, indicating that the item was not found. The method uses the merge operator (|=) to update the existing item with the new data from item_data.

        # The commented-out code below shows an alternative way to retrieve the JSON payload from the request
        
        # item_data = request.get_json()
        # if ("price" not in item_data or "name" not in item_data):
        #         abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
        # try:
        #     item = items[item_id]
        #     item |= item_data         # |= is the merge operator in Python 3.9 and later, which updates the dictionary in place with the new data from item_data.
        #     return item
        # except KeyError:
        #     abort(404, message="Item not found")

        # ************************************ 

        # item = ItemModel.query.get_or_404(item_id)          # The query.get_or_404 method is called on the ItemModel class to retrieve an item from the database based on its item_id. If the item is not found, it automatically raises a 404 error, indicating that the item was not found. This provides a convenient way to handle item retrieval and error handling in a single line of code.
        # raise NotImplementedError("Update functionality is not implemented yet.")          # A NotImplementedError is raised to indicate that the update functionality has not been implemented yet. This serves as a placeholder for future implementation and informs developers that the update operation is not currently supported.
        # item.price = item_data["price"]          # The price attribute of the retrieved item is updated with the new value from item_data. This modifies the existing item object in memory, preparing it for the update operation in the database.
        # item.name = item_data["name"]          # The name attribute of the retrieved item is updated with the new value from item_data. This modifies the existing item object in memory, preparing it for the update operation in the database.
        # try:
        #     db.session.add(item)          # The add method of the db.session object is called to mark the updated item for insertion into the database. This prepares the item for updating in the database.
        #     db.session.commit()          # The commit method of the db.session object is called to save the changes to the database, effectively updating the item with the new values.
        # except SQLAlchemyError:          # If any SQLAlchemyError occurs during the commit operation, it indicates a general database error. In this case, a 500 error is raised using abort, indicating that an error occurred while updating the item in the database.
        #     abort(500, message="An error occurred while updating the item in the database.")

        # ************************************ 

        item = ItemModel.query.get(item_id)          # The query.get method is called on the ItemModel class to retrieve an item from the database based on its item_id. If the item is not found, it returns None instead of raising an error. This allows for conditional handling of the item retrieval.
        if item:          # If the item exists in the database, it proceeds to update its attributes with the new values from item_data. The price and name attributes are updated, and the changes are committed to the database.
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:          # If the item does not exist in the database, it creates a new item instance using the provided item_data and assigns the specified item_id. The new item is then added to the database session and committed, effectively creating a new record in the database.
            item = ItemModel(id=item_id, **item_data)

        try:
            db.session.add(item)          # The add method of the db.session object is called to mark the item (either updated or newly created) for insertion into the database. This prepares the item for updating or creating in the database.
            db.session.commit()          # The commit method of the db.session object is called to save the changes to the database, effectively updating or creating the item record.
        except SQLAlchemyError:          # If any SQLAlchemyError occurs during the commit operation, it indicates a general database error. In this case, a 500 error is raised using abort, indicating that an error occurred while updating or creating the item in the database.
            abort(500, message="An error occurred while updating or creating the item in the database.")
        return item          # The updated or newly created item is returned as the response to the PUT request. It will be serialized using the ItemSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.

        

@blp.route("/item")              # This decorator defines a route for the ItemList class, which handles requests related to the collection of items. It does not require an item_id parameter in the URL.
class ItemList(MethodView):           # The ItemList class also inherits from MethodView and defines methods for handling GET and POST requests related to the collection of items. The get method returns a list of all items, while the post method allows for the creation of a new item. It checks for the presence of "price", "name", and "store_id" in the request payload, raises a 400 error if any are missing, and checks for duplicates before creating a new item with a unique ID.

    @blp.response(200, ItemSchema(many=True))             # The @blp.response decorator is used to specify the response schema for the get method. It indicates that the response will be serialized using the ItemSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.
    def get(self):              # The get method retrieves a list of all items by returning a dictionary containing the items stored in the items dictionary. It converts the values of the items dictionary into a list and returns it in a JSON response format.

        # ************************************

        # return items.values()

        # ************************************

        return ItemModel.query.all()          # The query.all method is called on the ItemModel class to retrieve all items from the database. It returns a list of all item records in the "items" table, which will be serialized using the ItemSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.


    @jwt_required(fresh=True)              # The @jwt_required decorator is used to enforce authentication for the post method. It requires a valid JWT (JSON Web Token) to be present in the request, and the fresh=True argument indicates that a fresh token is required, meaning that the token must have been recently issued and not refreshed. This adds an extra layer of security to ensure that only authenticated users can create new items.
    @blp.arguments(ItemSchema)             # The @blp.arguments decorator is used to validate and deserialize the incoming request data based on the ItemSchema defined in schemas.py. It ensures that the request payload adheres to the specified schema, allowing for automatic validation and conversion of the data into a Python dictionary.
    @blp.response(201, ItemSchema)             # The @blp.response decorator is used to specify the response schema for the post method. It indicates that the response will be serialized using the ItemSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.
    def post(self, item_data):             # The post method allows for the creation of a new item. It retrieves the JSON payload from the request and checks if "price", "name", and "store_id" are included. If any of these fields are missing, it raises a 400 error using abort, indicating a bad request. It also checks for duplicates by iterating through the existing items and comparing the name and store_id. If a duplicate is found, it raises a 400 error. If all checks pass, it generates a unique item_id using uuid, creates a new item dictionary with the provided data, adds it to the items dictionary, and returns the newly created item.

        # ************************************ 

        # The commented-out code below shows an alternative way to retrieve the JSON payload from the request
        
        # item_data = request.get_json()
        # if ("price" not in item_data or "name" not in item_data or "store_id" not in item_data):
        #         abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload.")
        # for item in items.values():
        #     if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
        #         abort(400, message=f"Item already exists in store {item_data['store_id']}.")
    
        # item_id = uuid.uuid4().hex
        # item = { **item_data, "id": item_id }
        # items[item_id] = item

        # ************************************ 

        item = ItemModel(**item_data)          # An instance of the ItemModel class is created using the provided item_data. The ** operator is used to unpack the dictionary and pass its key-value pairs as keyword arguments to the constructor of the ItemModel class. This allows for the creation of a new item object with the specified attributes.
        try:
            db.session.add(item)          # The item object is added to the database session using the add method of the db.session object. This prepares the item for insertion into the database.
            db.session.commit()          # The commit method of the db.session object is called to persist the changes to the database. This executes the necessary SQL statements to insert the new item record into the "items" table.
        except SQLAlchemyError:          # If any other SQLAlchemyError occurs during the commit operation, it indicates a general database error. In this case, a 500 error is raised using abort, indicating that an error occurred while inserting the item into the database.
            abort(500, message="An error occurred while inserting the item into the database.")
    
        return item