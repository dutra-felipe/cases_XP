from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from .config import Config
from .models import db, User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, supports_credentials=True)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'views.user_login_page'
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import api_bp
    from .auth import auth_bp
    from .views import views_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)

    with app.app_context():
        db.create_all()

    @app.route('/health')
    def health_check():
        return {'status': 'Backend API funcionando!', 'version': '1.0.0'}

    return app