from app import create_app
from app.extensions import db
from app.models import Role


def seed_roles():
    app = create_app()

    with app.app_context():
        roles = [
            {
                "name": "Administrator",
                "description": "Full access to the StockFlow system.",
            },
            {
                "name": "Manager",
                "description": "Access to inventory, products, suppliers, sales, purchases, and reports.",
            },
            {
                "name": "Staff",
                "description": "Access to day-to-day operational features.",
            },
        ]

        for role_data in roles:
            # Avoid creating duplicate roles if the seed is run again.
            existing_role = Role.query.filter_by(
                name=role_data["name"]
            ).first()

            if existing_role:
                continue

            db.session.add(Role(**role_data))

        db.session.commit()
        print("Roles seeded successfully.")


if __name__ == "__main__":
    seed_roles()