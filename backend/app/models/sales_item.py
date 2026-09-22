from app.extensions import db


class SaleItem(db.Model):
    __tablename__ = "sale_items"

    id = db.Column(db.Integer, primary_key=True)

    # Links this item to the sale it belongs to.
    sale_id = db.Column(
        db.Integer,
        db.ForeignKey("sales.id"),
        nullable=False,
    )

    # Identifies the product that was sold.
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
    )

    # Number of units of the product included in this sale.
    quantity = db.Column(
        db.Integer,
        nullable=False,
    )

    # Price of one unit at the time the sale was made.
    # This preserves the historical selling price.
    unit_price = db.Column(
        db.Numeric(12, 2),
        nullable=False,
    )

    # Total value for this line item.
    # Calculated as quantity × unit_price.
    subtotal = db.Column(
        db.Numeric(12, 2),
        nullable=False,
    )

    # Provides access to the related sale and product.
    sale = db.relationship(
        "Sale",
        backref="items",
    )

    product = db.relationship(
        "Product",
        backref="sale_items",
    )

    def __repr__(self):
        return (
            f"<SaleItem sale_id={self.sale_id} "
            f"product_id={self.product_id}>"
        )