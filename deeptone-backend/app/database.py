from pymongo import MongoClient

MONGO_URI = "mongodb+srv://Parth:Parth2004@cluster0.1z6jsl4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

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
