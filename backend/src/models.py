from pymongo import IndexModel, ASCENDING
from .database import db

# User collection model
users_collection = db["users"]

# Create an index on the firstname field for faster lookups
users_collection.create_indexes([IndexModel([("firstname", ASCENDING)])])
