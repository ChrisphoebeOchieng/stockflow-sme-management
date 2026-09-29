from flask import Blueprint, jsonify, request  
from flask_jwt_extended import jwt_required

from app.auth.security import role_required
from app.auth.service import register_user
from app.models import User


# Groups user management endpoints under the /users URL prefix.
users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("", methods=["GET"])
@jwt_required()
@role_required("Administrator")
def get_users():
    # Retrieve users from the database in a consistent order.
    users = User.query.order_by(User.id.asc()).all()

    return jsonify({
        "users": [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role.name,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
            }
            for user in users
        ]
    }), 200


# ADDED: Retrieves a single user by their ID.
@users_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@role_required("Administrator")
def get_user(user_id):
    # Find the requested user by primary key.
    user = User.query.get(user_id)

    # Return a clear response when the requested user does not exist.
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
            "created_at": user.created_at.isoformat(),
        }
    }), 200


# ADDED: Allows an Administrator to create a new user account.
@users_bp.route("", methods=["POST"])  
@jwt_required() 
@role_required("Administrator")  
def create_user():  
    # Read the JSON body sent by the client.
    data = request.get_json()  

    # Reject requests that do not contain a JSON body.
    if not data:  
        return jsonify({  
            "error": "Request body must contain JSON data."  
        }), 400  

    # Extract the required user information.
    first_name = data.get("first_name")  
    last_name = data.get("last_name")  
    email = data.get("email")  
    password = data.get("password")  
    role_name = data.get("role", "Staff")  

    # Make sure all required fields were provided.
    if not all([first_name, last_name, email, password]):  
        return jsonify({  
            "error": (
                "first_name, last_name, email, and password "
                "are required."
            ) 
        }), 400  

    try:
        # Reuse the registration service so password hashing,
        # duplicate email checks, and role lookup stay in one place.
        user = register_user(  
            first_name=first_name,  
            last_name=last_name,  
            email=email,  
            password=password,  
            role_name=role_name,  
        )

        return jsonify({  
            "message": "User created successfully.",  
            "user": {  
                "id": user.id,  
                "first_name": user.first_name,  
                "last_name": user.last_name,  
                "email": user.email,  
                "role": user.role.name,  
                "is_active": user.is_active,  
            },  
        }), 201  

    except ValueError as error:  
        # Convert expected user creation errors into a client-friendly response.
        return jsonify({  
            "error": str(error)  
        }), 409  