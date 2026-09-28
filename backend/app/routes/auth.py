from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,  
    get_jwt_identity,
    jwt_required,
    )                 # Creates JWT access tokens

from app.auth.service import login_user, register_user


# Groups authentication-related endpoints under the /auth URL prefix.
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    # Read the JSON body sent by the client.
    data = request.get_json()

    # Reject requests that do not contain a JSON body.
    if not data:
        return jsonify({
            "error": "Request body must contain JSON data."
        }), 400

    # Extract the required registration fields.
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    # Make sure all required fields were provided before
    # passing the data to the registration service.
    if not all([first_name, last_name, email, password]):
        return jsonify({
            "error": "first_name, last_name, email, and password are required."
        }), 400

    try:
        # The service handles the database operation and password hashing.
        user = register_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        return jsonify({
            "message": "User registered successfully.",
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role.name,
            },
        }), 201

    except ValueError as error:
        # Convert expected registration errors into a client-friendly response.
        return jsonify({
            "error": str(error)
        }), 409


# Handles login requests for existing users.
@auth_bp.route("/login", methods=["POST"])
def login():
    # Read the JSON body sent by the client.
    data = request.get_json()

    # Reject requests that do not contain a JSON body.
    if not data:
        return jsonify({
            "error": "Request body must contain JSON data."
        }), 400

    # Extract the login credentials from the request.
    email = data.get("email")
    password = data.get("password")

    # Make sure both credentials were provided.
    if not email or not password:
        return jsonify({
            "error": "email and password are required."
        }), 400

    try:
        # The service verifies the credentials and returns the user.
        user = login_user(
            email=email,
            password=password,
        )

        # NEW: Create a signed JWT for the authenticated user.
        # The role is included as a claim so protected endpoints can
        # enforce role-based access later.
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role.name,
            },
        )

        return jsonify({
            "message": "Login successful.",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role.name,
            },
        }), 200

    except ValueError as error:
        # Convert authentication errors into a client-friendly response.
        return jsonify({
            "error": str(error)
        }), 401
    
# proteceted endpoint used to retrieve the currently authenticated user. 
@auth_bp.route("/me", methods=["GET"])    
@jwt_required()
def get_current_user():
    # Read the user ID stored in the JWT identity. 
    user_id = get_jwt_identity()

    # Fetch the user from the database using the ID.
    from app.models import User

    user = User.query.get(int(user_id))

    # If the user does not exist (e.g., deleted), return an error.
    if not user:
        return jsonify({
            "error": "User not found."
        }), 404
    
    return jsonify({
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role.name,
            "is_active": user.is_active,
        },
    }), 200