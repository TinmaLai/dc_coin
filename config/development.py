from config import BaseConfig

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV = 'development'
    
    # Development specific settings
    TEMPLATES_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = True
    
    # Development database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    
    # Verbose logging
    LOGGING_LEVEL = 'DEBUG'
