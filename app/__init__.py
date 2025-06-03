from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = (
    "auth.login"  # Assuming 'auth' will be the blueprint name for auth routes
)
login_manager.login_message_category = "info"
jwt = JWTManager()


@login_manager.user_loader
def load_user(user_id):
    from .models import User

    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    from . import models  # Ensure models are registered # noqa: F401

    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)

    from . import routes

    app.register_blueprint(routes.bp)

    from . import auth_routes

    app.register_blueprint(auth_routes.auth_bp)

    from . import registration_routes

    app.register_blueprint(registration_routes.reg_bp)

    return app
