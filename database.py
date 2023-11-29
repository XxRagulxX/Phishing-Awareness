import sqlite3
from flask import g

DATABASE = 'phishing_challenge.db'

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Create the table if it doesn't exist
def init_db(app):
    with app.app_context():
        cursor = get_db().cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            score INTEGER NOT NULL,
            total_score INTEGER NOT NULL
        )
    ''')
        get_db().commit()

# Close the database connection
def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()