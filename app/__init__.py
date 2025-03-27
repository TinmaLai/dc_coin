from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    with app.app_context():
        # Import routes
        from app.routes import init_routes
        
        # Initialize routes
        init_routes(app)
        
        # Create database tables
        db.create_all()
        
        # Register blueprints if any
        # app.register_blueprint(...)
        
        return app
