import os
from flask import Flask
from dotenv import load_dotenv

from app.extensions import (
    db, migrate, login_manager, bcrypt, cors
)

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_POSTGRES_URL"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv("SECRET_KEY", "dev"),
    )

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    # Blueprints
    from app.routes import main as main_blueprint
    from app.api import api as api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix="/api")

    # User loader
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
