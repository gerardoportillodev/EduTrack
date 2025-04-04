from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder="static")
    
    app.config.from_object('config.Config')
    
    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'main.login'  # Especifica la vista de login

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(id):
        from app.models import User
        return User.query.get(int(id))
    
    return app