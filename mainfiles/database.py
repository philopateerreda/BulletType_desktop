import sqlite3
import os

class Database:
    def __init__(self, db_name="users.db"):
        # Define the path to the database file
        self.db_path = os.path.join("F:\\vs_folder\\python_V1_6", db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')

        # Create matches table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            speed REAL NOT NULL,
            accuracy REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

        self.conn.commit()

    def create_user_table(self, user_id):
        cursor = self.conn.cursor()
        
        # Create a table for user data
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS user_{user_id} (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            speed REAL NOT NULL,
            accuracy REAL NOT NULL,
            result TEXT NOT NULL
        )
        ''')
        
        # Commit
        self.conn.commit()

    def register_user(self, username, email, password):
        try:
            # Check if user exists
            if self.user_exists(username=username, email=email):
                return False
            
            # Insert user data
            query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
            self.conn.execute(query, (username, email, password))
            self.conn.commit()
            
            # Get the newly created user_id
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ? AND email = ?", (username, email))
            user_id = cursor.fetchone()[0]
            
            # Create a table for this user
            self.create_user_table(user_id)
            
            return True
        except sqlite3.IntegrityError:
            return False

    def user_exists(self, username=None, email=None):
        query = "SELECT * FROM users WHERE"
        params = []

        if username:
            query += " username = ?"
            params.append(username)
        if email:
            if params:
                query += " OR"
            query += " email = ?"
            params.append(email)

        cursor = self.conn.execute(query, params)
        return cursor.fetchone() is not None

    def validate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor = self.conn.execute(query, (username, password))
        return cursor.fetchone() is not None

    def close(self):
        self.conn.close()
