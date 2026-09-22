from datetime import datetime, timezone

from app.extensions import db


class StockTransaction(db.Model):
    __tablename__ = "stock_transactions"

    id = db.Column(db.Integer, primary_key=True)

    # Identifies the product whose stock changed.
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
    )

    # Identifies the user responsible for recording the stock movement.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    # Describes why the inventory changed.
    # Examples: STOCK_IN, STOCK_OUT, ADJUSTMENT.
    transaction_type = db.Column(
        db.String(30),
        nullable=False,
    )

    # Stores the number of units added, removed, or adjusted.
    quantity = db.Column(
        db.Integer,
        nullable=False,
    )

    # Can store a related sale or purchase reference.
    reference = db.Column(
        db.String(100),
        nullable=True,
    )

    # Optional explanation for manual adjustments or other stock changes.
    notes = db.Column(
        db.Text,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Provides access to the related Product and User objects.
    product = db.relationship("Product", backref="stock_transactions")
    user = db.relationship("User", backref="stock_transactions")

    def __repr__(self):
        return (
            f"<StockTransaction product_id={self.product_id} "
            f"type={self.transaction_type} quantity={self.quantity}>"
        )