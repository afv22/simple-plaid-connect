from functools import wraps
from flask import request, jsonify, session
from firebase_admin import auth
from app.services.firebase import initialize_firebase

initialize_firebase()


def verify_token(token):
    """Verify the Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None


def require_token(f):
    """Decorator to require Firebase token for API endpoints"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the auth header
        auth_header = request.headers.get("Authorization")

        # Check if the auth header exists and has the right format
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authentication token is missing or invalid"}), 401

        # Extract the token
        token = auth_header.split("Bearer ")[1]

        # Verify the token
        decoded_token = verify_token(token)
        if not decoded_token:
            return jsonify({"error": "Invalid authentication token"}), 401

        # Add the user info to the Flask session
        session["uid"] = decoded_token["uid"]

        return f(*args, **kwargs)

    return decorated_function
