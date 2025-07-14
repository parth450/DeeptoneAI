from pymongo import MongoClient
import os

# Use environment variable for security
MONGO_URI = os.environ.get("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    db = client["deeptoneDB"]

    predictions_collection = db.get_collection("predictions")
    users_collection = db.get_collection("users")

    print("✅ MongoDB connected successfully")

except Exception as e:
    print("❌ MongoDB connection failed:", e)
    predictions_collection = None
    users_collection = None
