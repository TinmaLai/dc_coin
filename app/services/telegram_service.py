import asyncio
from telegram import Bot
from telegram.error import TelegramError
from telegram.request import HTTPXRequest
from config import BaseConfig
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        try:
            logger.info(f"BaseConfig bot tokennnn: {BaseConfig.TELEGRAM_BOT_TOKEN}")
            # Configure connection pool
            request = HTTPXRequest(
                connection_pool_size=8,
                connect_timeout=20.0,
                read_timeout=20.0,
                pool_timeout=3.0
            )
            self.bot = Bot(token=BaseConfig.TELEGRAM_BOT_TOKEN, request=request)
            self.chat_id = BaseConfig.TELEGRAM_CHAT_ID
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

    def send_batch_notification(self, notifications):
        """Send batch notification with multiple patterns"""
        try:
            if not notifications:
                logger.warning("Empty notifications list, skipping batch")
                return False
                
            # Sort by confidence and get top 5
            notifications.sort(key=lambda x: x[1]['confidence'], reverse=True)
            notifications = notifications[:5]
                
            logger.info("Sending batch notification for top 5 patterns")
            summary = "🏆 TOP 5 PATTERN PHÁT HIỆN:\n\n"
            for symbol, pattern in notifications:
                emoji = self.get_pattern_emoji(pattern['pattern_type'])
                is_bullish = pattern['take_profit'] > pattern['entry_price'] if pattern.get('take_profit') else None
                
                summary += (
                    f"{emoji} <b>{symbol}</b>\n"
                    f"Mẫu hình: {pattern['pattern_type'].replace('_', ' ').title()}\n"
                    f"Độ tin cậy: {pattern['confidence']*100:.1f}%\n"
                )
                
                if pattern.get('entry_price'):
                    tp_percent = abs((pattern['take_profit'] - pattern['entry_price']) / pattern['entry_price'] * 100)
                    sl_percent = abs((pattern['stop_loss'] - pattern['entry_price']) / pattern['entry_price'] * 100)
                    
                    summary += (
                        f"{"🟢" if is_bullish else "🔴"} Tín hiệu: {'LONG' if is_bullish else 'SHORT'}\n"
                        f"📍 Entry: {pattern['entry_price']:.2f}\n"
                        f"🎯 TP: {pattern['take_profit']:.2f} ({tp_percent:.1f}%)\n"
                        f"🛑 SL: {pattern['stop_loss']:.2f} ({sl_percent:.1f}%)\n"
                        f"📊 R/R: {pattern['risk_reward_ratio']}\n"
                    )
                
                summary += "\n"
            
            return asyncio.run(self.send_message(summary))
        except Exception as e:
            logger.error(f"Error in batch notification: {e}")
            return False

    def get_pattern_emoji(self, pattern_type):
        """Get emoji for pattern type"""
        emoji_map = {
            'head_and_shoulders': '👥',
            'double_top': '🔝',
            'double_bottom': '⬇️',
            'symmetric_triangle': '◀️▶️',
            'ascending_triangle': '📈',
            'descending_triangle': '📉',
            'triple_top': '⚠️',
            'triple_bottom': '✅',
            'rising_wedge': '📐',
            'falling_wedge': '📏',
            'bull_flag': '🚩',
            'bear_flag': '⛳'
        }
        return emoji_map.get(pattern_type, '📊')

    def format_pattern_message(self, symbol, pattern, current_price):
        """Format pattern detection message"""
        try:
            emoji = self.get_pattern_emoji(pattern['pattern_type'])
            message = f"{emoji} <b>{symbol}</b> - {pattern['pattern_type'].replace('_', ' ').title()} - {pattern['confidence']*100:.1f}%"
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
