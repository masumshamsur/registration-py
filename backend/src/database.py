import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="./config/.env")

#MONGO_URI = f"mongodb://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@mongodb-service:27017/{os.getenv('MONGO_DATABASE')}?authSource=admin"
MONGO_URI = f"mongodb://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_HOST')}:27017/{os.getenv('MONGO_DATABASE')}?authSource=admin"


# Establish MongoDB connection
try:
    client = MongoClient(MONGO_URI)
    db = client[os.getenv('MONGO_DATABASE')]
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")

def get_db():
    return db
