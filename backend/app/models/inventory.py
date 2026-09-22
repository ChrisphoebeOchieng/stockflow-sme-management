from datetime import datetime, timezone

from app.extensions import db


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)

    # Links the inventory record to the product it belongs to.
    # Each product should have only one inventory record.
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        unique=True,
        nullable=False,
    )

    # Stores the current quantity available for the product.
    # Stock changes will be handled through sales, purchases,
    # and stock adjustment operations.
    quantity = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    # Tracks when the current inventory quantity was last updated.
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Provides access to the related Product object through inventory.product.
    # uselist=False reflects the one-to-one product/inventory relationship.
    product = db.relationship(
        "Product",
        backref="inventory",
        uselist=False,
    )

    def __repr__(self):
        return (
            f"<Inventory product_id={self.product_id} "
            f"quantity={self.quantity}>"
        )