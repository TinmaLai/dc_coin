import os
from dotenv import load_dotenv

load_dotenv('D:\\Code\\resume\\.env.local')

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'Tsecret')
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crypto_scanner.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Binance
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    # os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    # Scanner Settings
    SCAN_INTERVAL = 3600  # 1 hour in seconds
    TOP_COINS_LIMIT = 100  # Number of top coins to scan
