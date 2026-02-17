from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import and register routes and models
    with app.app_context():
        from app import routes, models
        
        # Register error handlers
        @app.errorhandler(404)
        def not_found_error(error):
            from flask import render_template
            return render_template('errors/404.html'), 404
        
        @app.errorhandler(500)
        def internal_error(error):
            from flask import render_template
            db.session.rollback()
            return render_template('errors/500.html'), 500
    
    return app
