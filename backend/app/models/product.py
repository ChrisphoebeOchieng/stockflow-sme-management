from datetime import datetime, timezone

from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # Every product belongs to a category.
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False,
    )

    # A supplier can be assigned later, so this relationship is optional.
    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id"),
        nullable=True,
    )

    name = db.Column(db.String(150), nullable=False)

    # SKU is the unique identifier used to track a product.
    sku = db.Column(db.String(100), unique=True, nullable=False)

    description = db.Column(db.Text, nullable=True)

    cost_price = db.Column(db.Numeric(12, 2), nullable=False)
    selling_price = db.Column(db.Numeric(12, 2), nullable=False)

    # Used to determine when a product should appear as low stock.
    minimum_stock_level = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    # Products are deactivated rather than deleted when historical
    # transactions still depend on them.
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

    category = db.relationship("Category", backref="products")
    supplier = db.relationship("Supplier", backref="products")

    def __repr__(self):
        return f"<Product {self.name}>"