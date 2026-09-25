from ..db import db

class UserModel(db.Model):
    __tablename__ = "users"             # The __tablename__ attribute is set to "users", which specifies the name of the table in the database that this model corresponds to. This allows SQLAlchemy to map the model to the appropriate table when performing database operations.

    id = db.Column(db.Integer, primary_key=True)                  # The id attribute is defined as a column in the database table. It is of type Integer and is marked as the primary key for the table, which means that it uniquely identifies each record in the "users" table.
    username = db.Column(db.String(80), unique=True, nullable=False)               # The username attribute is defined as a column in the database table. It is of type String with a maximum length of 80 characters, marked as unique, and not nullable. This means that each user must have a unique username and cannot be left empty when creating or updating records in the "users" table.
    password = db.Column(db.String, nullable=False)                  # The password attribute is defined as a column in the database table. It is of type String and is marked as not nullable, which means that it cannot be left empty when creating or updating records in the "users" table. This attribute represents the user's password, which is typically stored in a hashed format for security purposes.