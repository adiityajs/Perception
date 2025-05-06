import sqlite3
import datetime
import hashlib

# Establish a global connection; using check_same_thread=False for Streamlit multi-threading
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

def init_tables():
    """Initializes the required tables."""
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY, 
                    password TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    activity TEXT,
                    timestamp TEXT
                 )''')
    conn.commit()

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Registers a new user with hashed password."""
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    """Logs in a user by checking provided credentials."""
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    return c.fetchone()

def log_activity(username, activity):
    """Logs user activity with a timestamp."""
    timestamp = datetime.datetime.now().isoformat()
    c.execute("INSERT INTO activity_logs (username, activity, timestamp) VALUES (?, ?, ?)",
              (username, activity, timestamp))
    conn.commit()

def get_activity_logs(username):
    """Fetches activity logs for a specific user."""
    c.execute("SELECT * FROM activity_logs WHERE username = ?", (username,))
    return c.fetchall()

# Initialize tables upon module import
init_tables()