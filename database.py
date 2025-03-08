import sqlite3
import hashlib
from typing import Optional, Dict, Any
import os

class Database:
    def __init__(self):
        self.db_path = "users.db"
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_user(self, email: str, password_hash: str, first_name: str, last_name: str) -> bool:
        """Add a new user to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (email, password_hash, first_name, last_name) VALUES (?, ?, ?, ?)",
                    (email, password_hash, first_name, last_name)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # Email already exists
            return False
        except Exception as e:
            print(f"Error adding user: {str(e)}")
            return False

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user data by email"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT email, password_hash, first_name, last_name FROM users WHERE email = ?",
                    (email,)
                )
                result = cursor.fetchone()
                if result:
                    return {
                        'email': result[0],
                        'password_hash': result[1],
                        'first_name': result[2],
                        'last_name': result[3]
                    }
                return None
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

    def user_exists(self, email: str) -> bool:
        """Check if a user exists"""
        user = self.get_user(email)
        return user is not None

    def verify_password(self, email: str, password_hash: str) -> bool:
        """Verify user's password"""
        user = self.get_user(email)
        if user:
            return user['password_hash'] == password_hash
        return False

    def delete_user(self, email: str) -> bool:
        """Delete a user from the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE email = ?", (email,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return False 