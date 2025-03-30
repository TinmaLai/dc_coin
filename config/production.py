from config import BaseConfig

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    ENV = 'production'
    
    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Production logging
    LOGGING_LEVEL = 'INFO'
    
    # Gunicorn specific
    workers = 4  # 2-4 x số CPU cores
    bind = "0.0.0.0:8000"
    worker_class = "sync"
    worker_connections = 1000
    timeout = 30
    keepalive = 2
    
    # Additional security headers
    SECURITY_HEADERS = {
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'X-Content-Type-Options': 'nosniff',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'"
    }
