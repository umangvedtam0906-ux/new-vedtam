import sqlite3
import os

db_path = 'subscribers.db'
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    organisation TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL,
    token TEXT,
    subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP
)''')

c.execute('''CREATE TABLE otps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    otp_hash TEXT NOT NULL,
    expires_at INTEGER NOT NULL,
    attempts INTEGER DEFAULT 0
)''')

c.execute('''CREATE TABLE rate_limits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT,
    email TEXT,
    last_request_time INTEGER NOT NULL,
    request_count INTEGER DEFAULT 1
)''')

c.execute('''INSERT INTO subscribers (name, phone, organisation, email, status, token) 
             VALUES ('Umang Chauhan', '9999999999', 'Vedtam', 'umang@vedtam.com', 'confirmed', 'test_token_123')''')
conn.commit()
conn.close()

print(f"Test database created at {db_path} with 1 confirmed subscriber.")
