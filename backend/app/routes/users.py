from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.auth.security import role_required
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