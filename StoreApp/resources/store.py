import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from db import stores
from ..schemas import StoreSchema

from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError, IntegrityError          # The SQLAlchemyError and IntegrityError classes are imported from the sqlalchemy.exc module. These classes represent exceptions that can occur during database operations using SQLAlchemy. SQLAlchemyError is a general exception class for database errors, while IntegrityError specifically handles integrity constraint violations, such as unique constraint violations. These exceptions allow you to catch and handle specific database errors in your code.

from ..db import db          # The db object is imported from the db module. This object is an instance of SQLAlchemy and provides the necessary functionality to interact with the database, including creating tables, executing queries, and managing database sessions.
from ..models import StoreModel          # The StoreModel class is imported from the models module. This class represents the structure and behavior of the "stores" table in the database and is used to create, retrieve, update, and delete store records in the database.


# A Blueprint in Flask-smorest is a way to organize your routes and views into reusable components. It allows you to group related routes together, making your code more modular and easier to maintain.
# Create a Blueprint for store-related routes
blp = Blueprint("Stores", __name__, description="Operations on stores")          # The Blueprint object is created with a name ("Stores"), the current module's name (__name__), and a description of the operations it handles. This Blueprint will be used to define routes and views related to stores.


@blp.route("/store/<int:store_id>")               # This decorator defines a route for the Store class, which handles requests related to a specific store identified by its store_id. The <string:store_id> part indicates that the store_id is expected to be a string parameter in the URL.
class Store(MethodView):              # The Store class inherits from MethodView, which allows you to define HTTP methods (GET, DELETE) as class methods. Each method corresponds to a specific HTTP request type and handles the logic for that request.

    @blp.response(200, StoreSchema)             # The @blp.response decorator is used to specify the response schema for the get method. It indicates that the response will be serialized using the StoreSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.
    def get(self, store_id):                 # The get method retrieves a store based on its store_id. It attempts to return the store from the stores dictionary. If the store_id does not exist, it raises a 404 error using abort, indicating that the store was not found.

        # ************************************ 

        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found")

        # ************************************ 

        store = StoreModel.query.get_or_404(store_id)          # The query.get_or_404 method is called on the StoreModel class to retrieve a store from the database based on its store_id. If the store is not found, it automatically raises a 404 error, indicating that the store was not found. This provides a convenient way to handle store retrieval and error handling in a single line of code.
        return store


    @jwt_required()
    def delete(self, store_id):              # The delete method removes a store based on its store_id. It attempts to delete the store from the stores dictionary. If the store_id does not exist, it raises a 404 error using abort, indicating that the store was not found.

        # ************************************ 

        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted"}
        # except KeyError:
        #     abort(404, message="Store not found")

        # ************************************ 

        jwt = get_jwt()
        if jwt.get("role") != "admin":          # The get_jwt function is called to retrieve the JWT (JSON Web Token) from the request. It returns a dictionary containing the claims (payload) of the token. The code checks if the "role" claim in the JWT is not equal to "admin". If the user does not have an admin role, it raises a 401 error using abort, indicating that admin privileges are required to perform the delete operation.
            abort(401, message="Admin privilege required.")

        store = StoreModel.query.get_or_404(store_id)          # The query.get_or_404 method is called on the StoreModel class to retrieve a store from the database based on its store_id. If the store is not found, it automatically raises a 404 error, indicating that the store was not found. This provides a convenient way to handle store retrieval and error handling in a single line of code.
        # ************************************ 
        # raise NotImplementedError("Delete functionality is not implemented yet.")          # A NotImplementedError is raised to indicate that the delete functionality has not been implemented yet. This serves as a placeholder for future implementation and informs developers that the delete operation is not currently supported.
        # ************************************ 
        db.session.delete(store)          # The store object is deleted from the database session using db.session.delete. This prepares the store object to be removed from the database when the session is committed.
        db.session.commit()          # The changes made to the database session are committed using db.session.commit. This finalizes the deletion of the store from the database.
        return {"message": "Store deleted"}          # A JSON response is returned with a message indicating that the store has been successfully deleted. This provides feedback to the client about the outcome of the DELETE request.



@blp.route("/store")                  # This decorator defines a route for the StoreList class, which handles requests related to the collection of stores. It does not require a store_id parameter in the URL.
class StoreList(MethodView):                     # The StoreList class also inherits from MethodView and defines methods for handling GET and POST requests related to the collection of stores. The get method returns a list of all stores, while the post method allows for the creation of a new store. It checks for the presence of "name" in the request payload, raises a 400 error if it is missing, and checks for duplicates before creating a new store with a unique ID.

    @blp.response(200, StoreSchema(many=True))             # The @blp.response decorator is used to specify the response schema for the get method. It indicates that the response will be serialized using the StoreSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.
    def get(self):                  # The get method retrieves a list of all stores by returning a dictionary containing the stores stored in the stores dictionary. It converts the values of the stores dictionary into a list and returns it in a JSON response format.

        # ************************************ 

        # return stores.values()

        # ************************************ 

        return StoreModel.query.all()          # The query.all method is called on the StoreModel class to retrieve all stores from the database. It returns a list of all store records in the "stores" table, which will be serialized using the StoreSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.


    @blp.arguments(StoreSchema)                 # The @blp.arguments decorator is used to validate and deserialize the incoming request data based on the StoreSchema defined in schemas.py. It ensures that the request payload adheres to the specified schema, allowing for automatic validation and conversion of the data into a Python dictionary.
    @blp.response(201, StoreSchema)             # The @blp.response decorator is used to specify the response schema for the post method. It indicates that the response will be serialized using the StoreSchema defined in schemas.py, ensuring that the output adheres to the specified schema and provides a consistent format for the API response.
    def post(self, store_data):                 # The post method allows for the creation of a new store. It retrieves the JSON payload from the request and checks if "name" is included. If it is missing, it raises a 400 error using abort, indicating a bad request. It also checks for duplicates by iterating through the existing stores and comparing the name. If a duplicate is found, it raises a 400 error. If all checks pass, it generates a unique store_id using uuid, creates a new store dictionary with the provided data, adds it to the stores dictionary, and returns the newly created store.

        # ************************************ 

        # store_data = request.get_json()

        # if "name" not in store_data:
        #     abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")

        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message=f"Store with name '{store_data['name']}' already exists.")

        # store_id = uuid.uuid4().hex
        # store = { **store_data, "id": store_id }
        # stores[store_id] = store

        # ************************************ 

        store = StoreModel(**store_data)          # A new instance of the StoreModel class is created using the provided store_data. The **store_data syntax unpacks the dictionary and passes its key-value pairs as keyword arguments to the StoreModel constructor, allowing for the creation of a new store object with the specified attributes.
        try:
            db.session.add(store)          # The new store object is added to the database session using db.session.add. This prepares the store object to be inserted into the database when the session is committed.
            db.session.commit()          # The changes made to the database session are committed using db.session.commit. This finalizes the insertion of the new store into the database, making it persistent and available for future queries.
        except IntegrityError:          # If an IntegrityError occurs during the commit (e.g., due to a unique constraint violation), it is caught in the except block. This allows for graceful error handling and provides feedback to the client about the issue.
            abort(400, message="A store with that name already exists.")          # If an IntegrityError is caught, a 400 error is raised using abort, indicating that a store with the same name already exists. This informs the client that the request could not be completed due to a conflict with existing data.
        except SQLAlchemyError:          # If any other SQLAlchemyError occurs during the commit, it is caught in the except block. This allows for handling unexpected database errors and provides feedback to the client about the issue.
            abort(500, message="An error occurred while creating the store.")          # If a SQLAlchemyError is caught, a 500 error is raised using abort, indicating that an internal server error occurred while attempting to create the store. This informs the client that the request could not be completed due to a server-side issue.

        return store