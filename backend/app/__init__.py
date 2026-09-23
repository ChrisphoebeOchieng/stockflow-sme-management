from flask import Flask

from app.config import Config
from app.extensions import db, migrate, jwt, ma
from app.models import Role  # Import your models here
from app.routes.auth import auth_bp  #Import the authentication blueprint



def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)

    app.register_blueprint(auth_bp) # Register authentication routes with the Flask application.

    return app