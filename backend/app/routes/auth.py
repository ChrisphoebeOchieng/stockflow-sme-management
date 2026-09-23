from flask import Blueprint, jsonify, request

from app.auth.service import register_user


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