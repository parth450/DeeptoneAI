from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime
import numpy as np

from app.classifier import classify_audio
from app.audio_classification import extract_features
from app.database import predictions_collection, users_collection

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return "🎧 Welcome to Deeptone AI API — Deepfake Voice Detection"


#  AUDIO PREDICTION ROUTE
@main.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    username = request.form.get('username')

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        result = classify_audio(file)

        # Convert NumPy floats to native Python floats
        clean_result = {
            k: float(v) if isinstance(v, (np.float32, np.float64)) else v
            for k, v in result.items()
        }

        # Add metadata
        clean_result.update({
            "filename": file.filename,
            "timestamp": datetime.utcnow(),
            "username": username,
        })

        #   Check collection properly
        if predictions_collection is not None:
            inserted = predictions_collection.insert_one(clean_result)
            clean_result["_id"] = str(inserted.inserted_id)

        return jsonify(clean_result), 200

    except Exception as e:
        print("Prediction error:", str(e))
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


#  USER REGISTRATION
@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })

    return jsonify({"message": "User registered successfully"}), 201


#  USER LOGIN
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "Invalid username"}), 401

    if not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid password"}), 401

    return jsonify({"message": "Login successful", "username": username}), 200


#  HISTORY ROUTE
@main.route('/history/<username>', methods=['GET'])
def get_history(username):
    try:
        if not username:
            return jsonify({"error": "Username required"}), 400

        #  Check collection explicitly
        if predictions_collection is None:
            return jsonify([]), 200

        history_cursor = predictions_collection.find(
            {"username": username}
        ).sort("timestamp", -1)

        history = []
        for item in history_cursor:
            history.append({
                "_id": str(item["_id"]),
                "prediction": item.get("prediction"),
                "accuracy": float(item.get("accuracy", 0)),
                "recall": float(item.get("recall", 0)),
                "precision": float(item.get("precision", 0)),
                "f1_score": float(item.get("f1_score", 0)),
                "filename": item.get("filename", "unknown"),
                "timestamp": item.get("timestamp").isoformat() if item.get("timestamp") else ""
            })

        return jsonify(history), 200

    except Exception as e:
        print("History error:", str(e))
        return jsonify({"error": "Failed to fetch history", "details": str(e)}), 500
