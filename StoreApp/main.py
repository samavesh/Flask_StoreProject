import os
import redis
from rq import Queue

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from StoreApp.models.user import UserModel

from .db import db
from .blocklist import BLOCKLIST

from .resources.item import blp as ItemBlueprint
from .resources.store import blp as StoreBlueprint
from .resources.tag import blp as TagBlueprint
from .resources.user import blp as UserBlueprint


def create_app(db_url = None):          # The create_app function is defined to create and configure a Flask application instance. It takes an optional parameter db_url, which allows you to specify the database connection URL. If db_url is not provided, it will use the DATABASE_URL environment variable or default to a SQLite database named "data.db". This function encapsulates the application setup and configuration, making it easier to create multiple instances of the app with different configurations if needed.
    app = Flask(__name__)                # The Flask app instance is created by calling the Flask constructor and passing the name of the current module (__name__) as an argument. This instance serves as the central object for the application, allowing you to define routes, configure settings, and manage the overall behavior of the web application.
    load_dotenv()          # The load_dotenv function is called to load environment variables from a .env file. This allows you to define configuration values, such as the database connection URL, in a separate file and access them within the application using the os.getenv function. It provides a convenient way to manage sensitive information and configuration settings without hardcoding them in the codebase.

    connection = redis.from_url(os.getenv("REDIS_URL"))          # The connection variable is created by calling the redis.from_url function and passing the value of the REDIS_URL environment variable. This establishes a connection to a Redis server using the specified URL, allowing the application to interact with Redis for caching, message queuing, or other purposes.
    app.queue = Queue("emails", connection=connection)          # The app.queue attribute is set to a new instance of the Queue class, which is created by passing the name "emails" and the Redis connection object. This sets up a queue for handling email-related tasks, allowing the application to enqueue and process email sending operations asynchronously using Redis as the backend.
    
    app.config["PROPAGATE_EXCEPTIONS"] = True               # The PROPAGATE_EXCEPTIONS configuration option is set to True, which means that exceptions raised during request handling will be propagated to the Flask application. This allows for better error handling and debugging, as it enables the application to catch and handle exceptions appropriately.
    app.config["API_TITLE"] = "Stores REST API"               # The API_TITLE configuration option is set to "Stores REST API", which specifies the title of the API. This title will be displayed in the generated OpenAPI documentation, providing a clear and descriptive name for the API.
    app.config["API_VERSION"] = "v1"                    # The API_VERSION configuration option is set to "v1", which specifies the version of the API. This versioning allows for better management of changes and updates to the API over time, enabling clients to specify which version of the API they want to interact with.
    app.config["OPENAPI_VERSION"] = "3.0.3"                 # The OPENAPI_VERSION configuration option is set to "3.0.3", which specifies the version of the OpenAPI specification that will be used for generating the API documentation. This ensures that the generated documentation adheres to the specified version of the OpenAPI standard, providing a consistent and standardized format for describing the API endpoints and their behavior.
    app.config["OPENAPI_URL_PREFIX"] = "/"                  # The OPENAPI_URL_PREFIX configuration option is set to "/", which specifies the URL prefix for the OpenAPI documentation. This means that the generated OpenAPI documentation will be accessible at the root URL of the application, allowing clients to easily access and explore the API documentation.
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"               # The OPENAPI_SWAGGER_UI_PATH configuration option is set to "/swagger-ui", which specifies the URL path where the Swagger UI will be served. This allows clients to access the Swagger UI interface at the specified path, providing an interactive and user-friendly way to explore and test the API endpoints.
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"                # The OPENAPI_SWAGGER_UI_URL configuration option is set to "https://cdn.jsdelivr.net/npm/swagger-ui-dist/", which specifies the URL where the Swagger UI assets will be loaded from. This allows the application to use the Swagger UI interface for API documentation and testing, providing a convenient and visually appealing way for clients to interact with the API endpoints.
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")                # The SQLALCHEMY_DATABASE_URI configuration option is set to the value of the DATABASE_URL environment variable, or "sqlite:///data.db" if the environment variable is not set. This specifies the database connection URI that SQLAlchemy will use to connect to the database. It allows for flexibility in choosing different database backends based on the deployment environment.
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL")           # The SQLALCHEMY_DATABASE_URI configuration option is set to the value of the DATABASE_URL environment variable, or db_url if it is provided. This specifies the database connection URI that SQLAlchemy will use to connect to the database. It allows for flexibility in choosing different database backends based on the deployment environment.     
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False          # The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False, which disables the tracking of modifications to objects and the emission of signals. This improves performance and reduces memory usage, as it prevents unnecessary overhead associated with tracking changes to the database models.

    db.init_app(app)          # The db.init_app method is called to initialize the SQLAlchemy database instance with the Flask app. This allows the application to interact with the specified database using SQLAlchemy's ORM capabilities.

    migrate = Migrate(app, db)          # The Migrate object is created by passing the Flask app instance and the SQLAlchemy database instance to it. This object is responsible for managing database migrations, allowing you to create and apply changes to the database schema over time. It provides a convenient way to handle database versioning and schema evolution in a controlled manner.

    api = Api(app)          # The Api object is created by passing the Flask app instance to it. This object is responsible for managing the API endpoints, handling requests, and generating OpenAPI documentation. It serves as a bridge between the Flask application and the resources defined in the blueprints.

    app.config["JWT_SECRET_KEY"] = "295893115409531720718832377074777450501"           # The JWT_SECRET_KEY configuration option is set to a secret key value, which is used for signing and verifying JSON Web Tokens (JWTs). This key should be kept secure and not exposed publicly, as it is essential for ensuring the integrity and authenticity of the tokens used for authentication and authorization in the application.
    jwt = JWTManager(app)            # The JWTManager object is created by passing the Flask app instance to it. This object is responsible for managing JSON Web Tokens (JWTs) in the application, including token creation, verification, and handling of token-related events. It provides a convenient way to implement authentication and authorization mechanisms using JWTs in the Flask application.

    # **************

    # "url": "http://127.0.0.1:5000"

    # **************

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):               # The check_if_token_in_blocklist function is defined as a callback function that will be called by the JWTManager to check if a given JWT token is in the blocklist. It takes two parameters: jwt_header and jwt_payload, which represent the header and payload of the JWT token, respectively. This function will be used to determine if a token has been invalidated or revoked, preventing it from being used for authentication in the future.
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):                # The revoked_token_callback function is defined as a callback function that will be called by the JWTManager when a revoked token is encountered. It takes two parameters: jwt_header and jwt_payload, which represent the header and payload of the JWT token, respectively. This function will be used to handle the case when a revoked token is used for authentication, returning an appropriate response to indicate that the token has been revoked.
        return (
            jsonify({"description": "The token has been revoked.", "error": "token_revoked"}),
            401,
        )

    # **************

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):               # The token_not_fresh_callback function is defined as a callback function that will be called by the JWTManager when a non-fresh token is encountered. It takes two parameters: jwt_header and jwt_payload, which represent the header and payload of the JWT token, respectively. This function will be used to handle the case when a non-fresh token is used for authentication, returning an appropriate response to indicate that a fresh token is required for certain operations.
        return (
            jsonify({"description": "The token is not fresh.", "error": "fresh_token_required"}),
            401,
        )

    # **************

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):                    # The add_claims_to_jwt function is defined as a callback function that will be called by the JWTManager to add additional claims to the JWT token. It takes one parameter: identity, which represents the identity of the user for whom the token is being generated. This function allows you to include custom claims in the JWT payload, providing additional information about the user or their permissions.
        user = UserModel.query.get(identity)
        if user:
            return {"role": user.role}
        return {"role": "user"}

    # **************

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):             # The expired_token_callback function is defined as a callback function that will be called by the JWTManager when an expired token is encountered. It takes two parameters: jwt_header and jwt_payload, which represent the header and payload of the JWT token, respectively. This function will be used to handle the case when an expired token is used for authentication, returning an appropriate response to indicate that the token has expired.
        return (
            jsonify({"message": "The token has expired.", "error": "token expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):              # The invalid_token_callback function is defined as a callback function that will be called by the JWTManager when an invalid token is encountered. It takes one parameter: error, which represents the error message associated with the invalid token. This function will be used to handle the case when an invalid token is used for authentication, returning an appropriate response to indicate that the token is invalid.
        return (
            jsonify({"message": "Signature verification failed.", "error": "invalid_token"}),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):                 # The missing_token_callback function is defined as a callback function that will be called by the JWTManager when a request is made without an access token. It takes one parameter: error, which represents the error message associated with the missing token. This function will be used to handle the case when a request is made without providing an access token, returning an appropriate response to indicate that authentication is required.
        return (
            jsonify({"description": "Request does not contain an access token.", "error": "authorization_required"}),
            401,
        )

    # **************

    # Below code commented because Flask_Migrate will be used to create database tables
    # with app.app_context():          # The with statement is used to create an application context for the Flask app. This ensures that the necessary context is available for performing operations that require access to the application, such as database operations and request handling.
    #     db.create_all()          # The db.create_all method is called to create the database tables based on the defined models. This ensures that the necessary tables are created in the database before handling any requests, allowing for proper storage and retrieval of data.

    api.register_blueprint(ItemBlueprint)              # The register_blueprint method is called on the Api object to register the ItemBlueprint. This allows the routes and views defined in the ItemBlueprint to be included in the API, making them accessible through the specified endpoints.
    api.register_blueprint(StoreBlueprint)              # The register_blueprint method is called on the Api object to register the StoreBlueprint. This allows the routes and views defined in the StoreBlueprint to be included in the API, making them accessible through the specified endpoints.
    api.register_blueprint(TagBlueprint)               # The register_blueprint method is called on the Api object to register the TagBlueprint. This allows the routes and views defined in the TagBlueprint to be included in the API, making them accessible through the specified endpoints.
    api.register_blueprint(UserBlueprint)               # The register_blueprint method is called on the Api object to register the UserBlueprint. This allows the routes and views defined in the UserBlueprint to be included in the API, making them accessible through the specified endpoints.

    return app          # The create_app function returns the configured Flask app instance, allowing it to be used for running the application or for further customization if needed.