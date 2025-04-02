from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig

db = SQLAlchemy()

def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    with app.app_context():
        # Import routes
        from app.routes import init_routes
        
        # Initialize routes
        init_routes(app)
        
        # Create database tables
        # db.create_all()  # Disabled - Using migrations instead
        
        # Register blueprints if any
        # app.register_blueprint(...)
        
        return app
