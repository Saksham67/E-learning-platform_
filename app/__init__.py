from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from .models import db, User
import os



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['UPLOAD_FOLDER'] = os.path.join('app/static/uploads')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes.auth import auth
    app.register_blueprint(auth)

    from .routes.main import main
    app.register_blueprint(main)

    from .routes.user import user_bp
    app.register_blueprint(user_bp)

    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp)


    return app
