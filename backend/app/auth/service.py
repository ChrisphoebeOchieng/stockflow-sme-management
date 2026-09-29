from app.extensions import db
from app.models import Role, User
from app.auth.security import hash_password, verify_password


def register_user(first_name, last_name, email, password, role_name="Staff"):
    # Check whether the email is already associated with an account.
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        raise ValueError("A user with this email already exists.")

    # Find the role that will be assigned to the new account.
    role = Role.query.filter_by(name=role_name).first()

    if not role:
        raise ValueError("The specified role does not exist.")

    # Store only the hashed password, never the plain-text password.
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=hash_password(password),
        role=role,
    )

    db.session.add(user)
    db.session.commit()

    return user


def login_user(email, password):
    # Find the account using the email provided during login.
    user = User.query.filter_by(email=email).first()

    # Use the same error message for invalid email or password
    # so we do not reveal whether an email exists in the system.
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password.")

    # Prevent inactive accounts from signing into the system.
    if not user.is_active:
        raise ValueError("This account is inactive.")

    return user


# ADDED: Updates the permitted details of an existing user.
def update_user(user_id, first_name=None, last_name=None, email=None,
                role_name=None, is_active=None):
    # Find the user being updated.
    user = User.query.get(user_id)

    if not user:
        raise ValueError("User not found.")

    # Prevent another account from using the same email address.
    if email and email != user.email:
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            raise ValueError("A user with this email already exists.")

    # Update only the fields that were included in the request.
    if first_name is not None:
        user.first_name = first_name

    if last_name is not None:
        user.last_name = last_name

    if email is not None:
        user.email = email

    if role_name is not None:
        role = Role.query.filter_by(name=role_name).first()

        if not role:
            raise ValueError("The specified role does not exist.")

        user.role = role

    if is_active is not None:
        user.is_active = is_active

    db.session.commit()

    return user