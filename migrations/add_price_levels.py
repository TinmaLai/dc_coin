"""Add price levels columns

Revision ID: add_price_levels
Create Date: 2025-03-31 23:51

"""
import sqlite3

def upgrade():
    # Connect to database
    conn = sqlite3.connect('instance/app.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS pattern (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol VARCHAR(20) NOT NULL,
        pattern_type VARCHAR(50) NOT NULL,
        price REAL NOT NULL,
        confidence REAL NOT NULL,
        timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT,
        entry_price REAL,
        take_profit REAL,
        stop_loss REAL,
        risk_reward_ratio REAL
    )''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

def downgrade():
    # SQLite does not support dropping columns
    pass
