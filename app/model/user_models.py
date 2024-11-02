import sqlite3
import hashlib
import os

DATABASE = 'db.sqlite'

class User:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DATABASE)
    
    @staticmethod
    def create_user(username, password):
        salt = os.urandom(16).hex()
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

        conn = User.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', (username, hashed_password, salt))
            conn.commit()
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
        return True
    
    @staticmethod
    def get_user_by_username(username):
        conn = User.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def verify_password(username, password):
        user = User.get_user_by_username(username)
        if user:
            user_id, username, stored_password, salt, session_token = user
            hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            return hashed_password == stored_password
        return False
    
    @staticmethod
    def set_session_token(username, session_token):
        conn = User.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET session_token = ? WHERE username = ?', (session_token, username))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_by_session_token(session_token):
        conn = User.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE session_token = ?', (session_token,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def remove_session_token(session_token):
        conn = User.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET session_token = NULL WHERE session_token = ?', (session_token,))
        conn.commit()
        conn.close()