import sqlite3
import os
import importlib.util

def load_migration(file_path):
    """Load migration module dynamically"""
    spec = importlib.util.spec_from_file_location("migration", file_path)
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    return migration

def apply_migration():
    """Apply migration and clean up old data"""
    try:
        # Get migration file
        migration_file = os.path.join('migrations', 'add_retest_fields.py')
        if not os.path.exists(migration_file):
            print("Migration file not found!")
            return

        # Load and run migration
        migration = load_migration(migration_file)
        print("Running migration upgrade...")
        migration.upgrade()
        print("Migration completed successfully")

        # Clean up old data using SQLite directly
        print("Cleaning up old patterns...")
        conn = sqlite3.connect('instance/app.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pattern")
        conn.commit()
        conn.close()
        print("Old patterns deleted")

        print("Migration and cleanup completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        

if __name__ == '__main__':
    apply_migration()
