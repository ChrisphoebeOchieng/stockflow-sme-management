from datetime import datetime, timezone

from app.extensions import db


class Sale(db.Model):
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)

    # Identifies the user who recorded the sale.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    # Stores the total value of the completed sale.
    # The total will be calculated from the sale items.
    total_amount = db.Column(
        db.Numeric(12, 2),
        nullable=False,
    )

    # Tracks the current state of the sale.
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

    # Provides access to the user who recorded the sale.
    user = db.relationship("User", backref="sales")

    def __repr__(self):
        return f"<Sale id={self.id} status={self.status}>"