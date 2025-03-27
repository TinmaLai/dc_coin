import asyncio
from telegram import Bot
from telegram.error import TelegramError
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        try:
            logger.info(f"Config bot tokennnn: {Config.TELEGRAM_BOT_TOKEN}")
            self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
            self.chat_id = Config.TELEGRAM_CHAT_ID
            logger.info(f"Telegram bot initialized with chat_id: {self.chat_id}")
        except Exception as e:
            logger.error(f"Error initializing Telegram bot: {e}")
            raise

    async def send_message(self, message):
        """Send message to Telegram channel"""
        try:
            if not self.bot or not self.chat_id:
                logger.error("Bot or chat_id not properly initialized")
                return False
                
            logger.info(f"Attempting to send message to chat {self.chat_id}")
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            logger.info("Message sent successfully")
            return True
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending message: {e}")
            return False

    def send_batch_notification(self, message):
        """Send batch notification with multiple patterns"""
        try:
            if not message.strip():
                logger.warning("Empty message, skipping notification")
                return False
                
            logger.info("Sending batch notification")
            return asyncio.run(self.send_message(message))
        except Exception as e:
            logger.error(f"Error in batch notification: {e}")
            return False

    def format_pattern_message(self, symbol, pattern, current_price):
        """Format pattern detection message"""
        try:
            emoji_map = {
                'head_and_shoulders': '👥',
                'double_top': '🔝',
                'double_bottom': '⬇️',
                'symmetric_triangle': '◀️▶️',
                'ascending_triangle': '📈',
                'descending_triangle': '📉'
            }
            
            emoji = emoji_map.get(pattern['pattern_type'], '📊')
            
            message = (
                f"{emoji} <b>Phát hiện mô hình!</b>\n\n"
                f"<b>Mã:</b> {symbol}\n"
                f"<b>Mô hình:</b> {pattern['pattern_type'].replace('_', ' ').title()}\n"
                f"<b>Giá hiện tại:</b> {current_price:,.2f} USDT\n"
                f"<b>Độ tin cậy:</b> {pattern['confidence']*100:.1f}%\n"
                f"<b>Chi tiết:</b> {pattern['description']}\n\n"
                f"<i>⚠️ Lưu ý: Đây chỉ là phân tích kỹ thuật tự động, "
                f"không phải là khuyến nghị đầu tư.</i>"
            )
            
            return message
        except Exception as e:
            logger.error(f"Error formatting message: {e}")
            return None

    def test_connection(self):
        """Test Telegram connection and permissions"""
        try:
            logger.info("Testing Telegram connection...")
            test_message = "🔄 Kiểm tra kết nối Telegram Bot"
            result = asyncio.run(self.send_message(test_message))
            
            if result:
                logger.info("Telegram connection test successful")
                return True
            else:
                logger.error("Telegram connection test failed")
                return False
        except Exception as e:
            logger.error(f"Error testing Telegram connection: {e}")
            return False

    def notify_pattern(self, symbol, pattern, current_price):
        """Send single pattern notification"""
        try:
            message = self.format_pattern_message(symbol, pattern, current_price)
            if message:
                logger.info(f"Sending notification for {symbol} pattern: {pattern['pattern_type']}")
                return asyncio.run(self.send_message(message))
            return False
        except Exception as e:
            logger.error(f"Error in pattern notification: {e}")
            return False
