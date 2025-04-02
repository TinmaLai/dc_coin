from datetime import datetime, timedelta
from app import db
import logging

logger = logging.getLogger(__name__)

class Pattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False)
    pattern_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)
    
    # Retest information
    retest_status = db.Column(db.String(20), nullable=False, default='none')  # none, pending, confirmed, failed
    retest_price = db.Column(db.Float)
    retest_timestamp = db.Column(db.DateTime)
    retest_description = db.Column(db.Text)
    
    # Price levels
    entry_price = db.Column(db.Float)
    take_profit = db.Column(db.Float)
    stop_loss = db.Column(db.Float)
    risk_reward_ratio = db.Column(db.Float)
    
    # Unique constraint to prevent duplicates within time window
    __table_args__ = (
        db.UniqueConstraint('symbol', 'pattern_type', 'timestamp', 
                           name='_symbol_pattern_timestamp_uc'),
    )

    def __repr__(self):
        return f'<Pattern {self.symbol} {self.pattern_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'pattern_type': self.pattern_type,
            'price': self.price,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat(),
            'description': self.description,
            'entry_price': self.entry_price,
            'take_profit': self.take_profit,
            'stop_loss': self.stop_loss,
            'risk_reward_ratio': self.risk_reward_ratio,
            'retest_status': self.retest_status,
            'retest_price': self.retest_price,
            'retest_timestamp': self.retest_timestamp.isoformat() if self.retest_timestamp else None,
            'retest_description': self.retest_description
        }

    @staticmethod
    def cleanup_old_patterns(hours=24):
        """Delete patterns older than specified hours"""
        try:
            cutoff = datetime.utcnow() - timedelta(hours=hours)
            num_deleted = Pattern.query.filter(Pattern.timestamp < cutoff).delete()
            db.session.commit()
            logger.info(f"Deleted {num_deleted} old patterns")
            return num_deleted
        except Exception as e:
            logger.error(f"Error cleaning up patterns: {e}")
            db.session.rollback()
            raise
