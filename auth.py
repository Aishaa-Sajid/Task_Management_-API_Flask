from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
import bcrypt, jwt
from app.config import Config

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed = bcrypt.hashpw(
    data["password"].encode(),
    bcrypt.gensalt()
    ).decode("utf-8")


    user = User(
        email=data["email"],
        username=data["username"],
        password=hashed
    )

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registered"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({"id": user.id}, Config.JWT_SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

from app.utils.decorators import token_required

@auth_bp.route("/profile", methods=["GET"])
@token_required
def get_profile(user):
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username
    })


@auth_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(user):
    data = request.json

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)

    db.session.commit()

    return jsonify({"message": "Profile updated"})
