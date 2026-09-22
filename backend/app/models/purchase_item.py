from app.extensions import db


class PurchaseItem(db.Model):
    __tablename__ = "purchase_items"

    id = db.Column(db.Integer, primary_key=True)

    # Links this item to the purchase it belongs to.
    purchase_id = db.Column(
        db.Integer,
        db.ForeignKey("purchases.id"),
        nullable=False,
    )

    # Identifies the product included in the purchase.
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
    )

    # Number of units purchased.
    quantity = db.Column(
        db.Integer,
        nullable=False,
    )

    # Cost of one unit at the time of purchase.
    # This preserves the historical purchase cost.
    unit_cost = db.Column(
        db.Numeric(12, 2),
        nullable=False,
    )

    # Total value for this purchase line.
    # Calculated as quantity × unit_cost.
    subtotal = db.Column(
        db.Numeric(12, 2),
        nullable=False,
    )

    # Provides access to the related purchase and product.
    purchase = db.relationship(
        "Purchase",
        backref="items",
    )

    product = db.relationship(
        "Product",
        backref="purchase_items",
    )

    def __repr__(self):
        return (
            f"<PurchaseItem purchase_id={self.purchase_id} "
            f"product_id={self.product_id}>"
        )