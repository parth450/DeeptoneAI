from flask import Blueprint, request, jsonify
from app.database import users_collection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 409

    users_collection.insert_one({"username": username, "password": password})
    return jsonify({"message": "User registered successfully"})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username, "password": password})

    if user:
        return jsonify({"message": "Login successful", "username": username})
    return jsonify({"error": "Invalid credentials"}), 401

