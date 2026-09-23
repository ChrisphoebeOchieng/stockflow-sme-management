from app.extensions import db 
from app.models import Role, User
from app.auth.security import hash_password


def register_user(first_name, last_name, email, password, role_name="Staff"):
    # Check whether the email is already associated with an account.
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        raise ValueError("A user with this email already exists.")
    
    #Find the role that will be assigned to the new account.
    role = Role.query.filter_by(name=role_name).first()

    if not role :
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
