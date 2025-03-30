import os
from app import create_app

# Xác định config dựa trên FLASK_ENV
env = os.getenv('FLASK_ENV', 'production')
if env == 'development':
    from config.development import DevelopmentConfig
    config = DevelopmentConfig
else:
    from config.production import ProductionConfig
    config = ProductionConfig

app = create_app(config)

if __name__ == '__main__':
    if env == 'development':
        app.run(debug=True)
    else:
        # Production mode sẽ sử dụng Gunicorn
        app.run(host=config.bind.split(':')[0],
                port=int(config.bind.split(':')[1]),
                debug=False)
