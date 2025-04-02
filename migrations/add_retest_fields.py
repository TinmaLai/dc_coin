"""Add retest fields to Pattern model"""
import sqlite3

def upgrade():
    """Add new columns for retest functionality"""
    conn = sqlite3.connect('instance/app.db')
    cursor = conn.cursor()
    
    # Add new columns
    cursor.execute('ALTER TABLE pattern ADD COLUMN retest_status TEXT NOT NULL DEFAULT "none"')
    cursor.execute('ALTER TABLE pattern ADD COLUMN retest_price REAL')
    cursor.execute('ALTER TABLE pattern ADD COLUMN retest_timestamp TIMESTAMP')
    cursor.execute('ALTER TABLE pattern ADD COLUMN retest_description TEXT')
    
    conn.commit()
    conn.close()

def downgrade():
    """Remove retest columns"""
    conn = sqlite3.connect('instance/app.db')
    cursor = conn.cursor()
    
    # Since SQLite doesn't support DROP COLUMN, we need to recreate the table
    cursor.execute('''
        CREATE TABLE pattern_new (
            id INTEGER PRIMARY KEY,
            symbol TEXT NOT NULL,
            pattern_type TEXT NOT NULL,
            price REAL NOT NULL,
            confidence REAL NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            description TEXT,
            entry_price REAL,
            take_profit REAL,
            stop_loss REAL,
            risk_reward_ratio REAL
        )
    ''')
    
    cursor.execute('''
        INSERT INTO pattern_new 
        SELECT id, symbol, pattern_type, price, confidence, timestamp, description, 
               entry_price, take_profit, stop_loss, risk_reward_ratio
        FROM pattern
    ''')
    
    cursor.execute('DROP TABLE pattern')
    cursor.execute('ALTER TABLE pattern_new RENAME TO pattern')
    
    conn.commit()
    conn.close()
