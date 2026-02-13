from flask import request, jsonify
import jwt
from functools import wraps
from app.config import Config
from app.models.user import User

def token_required(func):
    @wraps(func)   # ✅ THIS LINE FIXES EVERYTHING
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data["id"])
        except:
            return jsonify({"error": "Invalid token"}), 401

        return func(current_user, *args, **kwargs)

    return wrapper
