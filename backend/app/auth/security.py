from functools import wraps

from flask_jwt_extended import (
    get_jwt,
    verify_jwt_in_request,

)
from werkzeug.security import check_password_hash , generate_password_hash

def hash_password(password):
   # converts the user's plain-text password into a secure hash
   # before it is stored in the database.
   return generate_password_hash(password)


def verify_password(password, password_hash):
   # Compares the password entered during login with the previously hashed password.
   return check_password_hash(password_hash, password)

def role_required(*allowed_roles):
    """
    Restricts access to users whose JWT contains one of the
    specified roles.
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Make sure the request contains a valid JWT first.
            verify_jwt_in_request()

            # Read the role claim stored inside the authenticated user's JWT.
            claims = get_jwt()
            user_role = claims.get("role")

            # Reject authenticated users whose role is not allowed.
            if user_role not in allowed_roles:
                return {
                    "error": "You do not have permission to access this resource."
                }, 403

            return function(*args, **kwargs)

        return wrapper

    return decorator