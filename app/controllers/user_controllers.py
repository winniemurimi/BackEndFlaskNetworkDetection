from flask import request, jsonify
from app.model.user_models import User
import os
import hashlib

SECRET_KEY = os.urandom(24).hex()

def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.create_user(username, password):
        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"error": "Username already exists"}), 400


def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.verify_password(username, password):
        session_token = hashlib.sha256(os.urandom(24)).hexdigest()
        User.set_session_token(username, session_token)

        user = User.get_user_by_username(username)
        user_id = user[0]

        return jsonify({"message": "Login successful", "user_id": user_id, "session_token": session_token}), 200
    return jsonify({"error": "Invalid username or password"}), 401


def logout():
    session_token = request.headers.get('X-Auth')
    if session_token:
        user = User.get_user_by_session_token(session_token)
        if user:
            User.remove_session_token(session_token)
            return jsonify({"message": "Logout successful"}), 200
        else:
            return jsonify({"error": "Invalid session token"}), 401
    return jsonify({"error": "Not logged in"}), 400

def current_user():
    session_token = request.headers.get('X-Auth')
    user = User.get_user_by_session_token(session_token)
    if user:
        return jsonify({"user_id": user[0], "username": user[1]}), 200
    return jsonify({"error": "Not logged in"}), 400
