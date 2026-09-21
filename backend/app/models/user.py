from datetime import datetime, timezone

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Links each user to one of the roles defined in the roles table.
    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False,
    )

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    # Email addresses must be unique so the same account cannot be registered twice.
    email = db.Column(db.String(255), unique=True, nullable=False)

    # Store a hashed password, never the user's plain-text password.
    password_hash = db.Column(db.String(255), nullable=False)

    # Deactivating an account lets us preserve its records without deleting the user.
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Provides access to the user's role through user.role.
    role = db.relationship("Role", backref="users")

    def __repr__(self):
        return f"<User {self.email}>"