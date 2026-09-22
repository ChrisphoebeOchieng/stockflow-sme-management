from datetime import datetime, timezone

from app.extensions import db


class Purchase(db.Model):
    __tablename__ = "purchases"

    id = db.Column(db.Integer, primary_key=True)

    # Identifies the supplier that provided the purchased products.
    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id"),
        nullable=False,
    )

    # Identifies the user who recorded the purchase.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    # Stores the total value of the purchase.
    # The total will be calculated from the purchase items.
    total_amount = db.Column(
        db.Numeric(12, 2),
        nullable=False,
    )

    # Tracks the current state of the purchase.
    # Example values: COMPLETED, CANCELLED.
    status = db.Column(
        db.String(30),
        nullable=False,
    )

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

    # Provides access to the supplier and user associated with the purchase.
    supplier = db.relationship(
        "Supplier",
        backref="purchases",
    )

    user = db.relationship(
        "User",
        backref="purchases",
    )

    def __repr__(self):
        return f"<Purchase id={self.id} status={self.status}>"