from flask import render_template, jsonify
from app import db
from app.models.pattern import Pattern
from app.services.binance_service import BinanceService
from app.services.pattern_analyzer import PatternAnalyzer
from app.services.telegram_service import TelegramService
from datetime import datetime, timedelta
import threading
import time
import atexit
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

binance_service = BinanceService()
pattern_analyzer = PatternAnalyzer()
telegram_service = TelegramService()
background_thread = None

def scan_patterns(app):
    """Background task to scan for patterns"""
    with app.app_context():
        while True:
            try:
                # Cleanup old patterns
                Pattern.cleanup_old_patterns(hours=24)
                logger.info("Cleaned up old patterns")
                
                # Get top symbols
                symbols = binance_service.get_top_symbols()
                logger.info(f"Analyzing {len(symbols)} symbols")
                
                # Initialize notifications list
                notifications = []
                
                for symbol in symbols:
                    try:
                        # Get historical data
                        df = binance_service.get_klines(symbol)
                        if df is None:
                            continue
                            
                        # Add technical indicators
                        df = binance_service.add_technical_indicators(df)
                        
                        # Analyze patterns
                        patterns = pattern_analyzer.analyze_all_patterns(df)
                        current_price = binance_service.get_current_price(symbol)
                        
                        if patterns and current_price:
                            for pattern in patterns:
                                # Check for existing pattern
                                cutoff = datetime.utcnow() - timedelta(hours=1)
                                existing = Pattern.query.filter(
                                    Pattern.symbol == symbol,
                                    Pattern.pattern_type == pattern['pattern_type'],
                                    Pattern.timestamp > cutoff
                                ).first()
                                
                                if existing is None:
                                    # Save to database
                                    db_pattern = Pattern(
                                        symbol=symbol,
                                        pattern_type=pattern['pattern_type'],
                                        price=current_price,
                                        confidence=pattern['confidence'],
                                        description=pattern['description']
                                    )
                                    db.session.add(db_pattern)
                                    logger.info(f"New pattern detected: {symbol} - {pattern['pattern_type']}")
                                    
                                    # Add to notifications list
                                    notifications.append((symbol, pattern))
                                    
                    except Exception as e:
                        logger.error(f"Error processing symbol {symbol}: {e}")
                        continue
                
                try:
                    # Commit all changes
                    db.session.commit()
                    logger.info(f"Found {len(notifications)} new patterns")
                    
                    # Send batch notification for top 5 patterns if any found
                    if notifications:
                        logger.info(f"Sending top 5 patterns out of {len(notifications)} detected patterns")
                        telegram_service.send_batch_notification(notifications)
                except Exception as e:
                    logger.error(f"Error committing changes: {e}")
                    db.session.rollback()
                
            except Exception as e:
                logger.error(f"Error in pattern scanning: {e}")
                
            # Sleep for 5 minutes
            logger.info("Sleeping for 5 minutes before next scan")
            time.sleep(300)

def cleanup_background_thread():
    """Cleanup function to stop background thread when app stops"""
    global background_thread
    if background_thread:
        logger.info("Cleaning up background thread")
        background_thread.join(timeout=1)

def init_routes(app):
    @app.route('/')
    def index():
        """Render main dashboard"""
        global background_thread
        # Start background task if not already running
        if not background_thread or not background_thread.is_alive():
            logger.info("Starting background scanning thread")
            background_thread = threading.Thread(target=scan_patterns, args=(app,), daemon=True)
            background_thread.start()
            # Register cleanup function
            atexit.register(cleanup_background_thread)
        return render_template('index.html')

    @app.route('/api/patterns')
    def get_patterns():
        """Get recent patterns"""
        try:
            # Get patterns from last 24 hours
            cutoff = datetime.utcnow() - timedelta(hours=24)
            patterns = Pattern.query.filter(Pattern.timestamp >= cutoff).order_by(Pattern.timestamp.desc()).all()
            
            # Get statistics
            total_patterns = Pattern.query.count()
            stats = {
                'total_patterns': total_patterns,
                'recent_patterns': len(patterns),
                'active_coins': len(set(p.symbol for p in patterns)),
                'accuracy_rate': sum(1 for p in patterns if p.confidence >= 0.8) / len(patterns) if patterns else 0
            }
            
            logger.info(f"Retrieved {len(patterns)} patterns. Total in DB: {total_patterns}")
            return jsonify({
                'patterns': [pattern.to_dict() for pattern in patterns],
                'stats': stats
            })
        except Exception as e:
            logger.error(f"Error getting patterns: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/cleanup')
    def cleanup_patterns():
        """Manual cleanup endpoint for testing"""
        try:
            before_count = Pattern.query.count()
            Pattern.cleanup_old_patterns()
            after_count = Pattern.query.count()
            logger.info(f"Cleaned up patterns: {before_count - after_count} removed")
            return jsonify({
                'status': 'success',
                'message': f'Cleaned up {before_count - after_count} patterns'
            })
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return app
