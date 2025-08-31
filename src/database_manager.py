import sqlite3
import hashlib
import json
import pickle
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

class DatabaseManager:
    """Database operations for Z-Secure authentication system"""
    
    def __init__(self, db_path='zsecure.db'):
        self.db_path = db_path
        
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                failed_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP NULL
            )
        ''')
        
        # Face data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                face_encoding BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Z-secure keys table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS zsecure_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                key_hash TEXT NOT NULL,
                key_salt BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Operations log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                operation_type TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_size INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                success BOOLEAN DEFAULT 1,
                error_message TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        # Security events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_type TEXT NOT NULL,
                description TEXT,
                ip_address TEXT,
                user_agent TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                severity TEXT DEFAULT 'INFO'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, email, password, face_encoding=None):
        """Create a new user account"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Hash password
            password_hash = generate_password_hash(password)
            
            # Insert user
            cursor.execute('''
                INSERT INTO users (email, password_hash)
                VALUES (?, ?)
            ''', (email, password_hash))
            
            user_id = cursor.lastrowid
            
            # Store face encoding if provided
            if face_encoding is not None:
                face_blob = pickle.dumps(face_encoding)
                cursor.execute('''
                    INSERT INTO face_data (user_id, face_encoding)
                    VALUES (?, ?)
                ''', (user_id, face_blob))
            
            conn.commit()
            conn.close()
            
            # Log security event
            self.log_security_event(user_id, 'USER_CREATED', f'New user account created: {email}')
            
            return user_id
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def user_exists(self, email):
        """Check if user exists"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            result = cursor.fetchone()
            
            conn.close()
            return result is not None
            
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False
    
    def verify_user_credentials(self, email, password):
        """Verify user credentials"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, email, password_hash, is_active, failed_attempts, locked_until
                FROM users WHERE email = ?
            ''', (email,))
            
            user = cursor.fetchone()
            conn.close()
            
            if not user:
                return None
            
            # Check if account is locked
            if user['locked_until'] and datetime.now() < datetime.fromisoformat(user['locked_until']):
                self.log_security_event(user['id'], 'LOGIN_ATTEMPT_LOCKED', f'Login attempt on locked account: {email}')
                return None
            
            # Check if account is active
            if not user['is_active']:
                return None
            
            # Verify password
            if check_password_hash(user['password_hash'], password):
                # Reset failed attempts on successful login
                self.reset_failed_attempts(user['id'])
                self.update_last_login(user['id'])
                return dict(user)
            else:
                # Increment failed attempts
                self.increment_failed_attempts(user['id'])
                self.log_security_event(user['id'], 'LOGIN_FAILED', f'Failed login attempt: {email}')
                return None
                
        except Exception as e:
            print(f"Error verifying credentials: {e}")
            return None
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, email, created_at, last_login, is_active
                FROM users WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            return dict(user) if user else None
            
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def store_zsecure_key(self, user_id, key):
        """Store Z-secure key for user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Generate salt and hash key for storage
            import secrets
            salt = secrets.token_bytes(32)
            key_hash = hashlib.pbkdf2_hmac('sha256', key, salt, 100000)
            
            # Store or update key
            cursor.execute('''
                INSERT OR REPLACE INTO zsecure_keys (user_id, key_hash, key_salt, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, key_hash.hex(), salt))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error storing Z-secure key: {e}")
            return False
    
    def get_zsecure_key(self, user_id):
        """Get Z-secure key for user (reconstructed from face data)"""
        try:
            # Get face encoding
            face_encoding = self.get_face_encoding(user_id)
            if face_encoding is None:
                return None
            
            # Get user email
            user = self.get_user(user_id)
            if not user:
                return None
            
            # Regenerate key from biometrics
            # Import here to avoid circular import
            import zsecure_encryption
            zsecure = zsecure_encryption.ZSecureEncryption()
            key = zsecure.generate_key_from_biometrics(face_encoding, user['email'])
            
            return key
            
        except Exception as e:
            print(f"Error getting Z-secure key: {e}")
            return None
    
    def update_zsecure_key(self, user_id, new_key):
        """Update Z-secure key"""
        return self.store_zsecure_key(user_id, new_key)
    
    def get_face_encoding(self, user_id):
        """Get face encoding for user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT face_encoding FROM face_data WHERE user_id = ?
                ORDER BY updated_at DESC LIMIT 1
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return pickle.loads(result['face_encoding'])
            return None
            
        except Exception as e:
            print(f"Error getting face encoding: {e}")
            return None
    
    def update_face_data(self, user_id, new_face_encoding):
        """Update face data for user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            face_blob = pickle.dumps(new_face_encoding)
            cursor.execute('''
                UPDATE face_data SET face_encoding = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (face_blob, user_id))
            
            conn.commit()
            conn.close()
            
            self.log_security_event(user_id, 'FACE_DATA_UPDATED', 'User updated facial biometric data')
            
            return True
            
        except Exception as e:
            print(f"Error updating face data: {e}")
            return False
    
    def get_face_data(self, user_id):
        """Get face data info (not the actual encoding)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT created_at, updated_at FROM face_data WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return dict(result) if result else None
            
        except Exception as e:
            print(f"Error getting face data info: {e}")
            return None
    
    def log_operation(self, user_id, operation_type, filename, file_size=None, success=True, error_message=None):
        """Log user operation"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO operations_log 
                (user_id, operation_type, filename, file_size, success, error_message)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, operation_type, filename, file_size, success, error_message))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error logging operation: {e}")
            return False
    
    def get_user_operations(self, user_id, limit=50):
        """Get user operations history"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT operation_type, filename, file_size, timestamp, success, error_message
                FROM operations_log 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            operations = cursor.fetchall()
            conn.close()
            
            return [dict(op) for op in operations]
            
        except Exception as e:
            print(f"Error getting operations: {e}")
            return []
    
    def log_security_event(self, user_id, event_type, description, severity='INFO'):
        """Log security event"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO security_events (user_id, event_type, description, severity)
                VALUES (?, ?, ?, ?)
            ''', (user_id, event_type, description, severity))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error logging security event: {e}")
            return False
    
    def increment_failed_attempts(self, user_id):
        """Increment failed login attempts"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET failed_attempts = failed_attempts + 1
                WHERE id = ?
            ''', (user_id,))
            
            # Lock account after 5 failed attempts
            cursor.execute('''
                UPDATE users SET locked_until = datetime('now', '+30 minutes')
                WHERE id = ? AND failed_attempts >= 5
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error incrementing failed attempts: {e}")
    
    def reset_failed_attempts(self, user_id):
        """Reset failed login attempts"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET failed_attempts = 0, locked_until = NULL
                WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error resetting failed attempts: {e}")
    
    def update_last_login(self, user_id):
        """Update last login timestamp"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating last login: {e}")
    
    def delete_user_account(self, user_id):
        """Delete user account and all associated data"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Log the account deletion
            self.log_security_event(user_id, 'ACCOUNT_DELETED', 'User account permanently deleted', 'WARNING')
            
            # Due to CASCADE constraints, deleting the user will automatically delete:
            # - face_data
            # - zsecure_keys  
            # - sessions
            # - operations_log
            # Note: security_events are kept for audit purposes
            
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            
            # Verify deletion
            rows_affected = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            return rows_affected > 0
            
        except Exception as e:
            print(f"Error deleting user account: {e}")
            return False
    
    def cleanup_user_files(self, user_id):
        """Clean up user-related files from filesystem"""
        try:
            import os
            import glob
            
            # Remove face data file if it exists
            face_file_path = f"face_data/user_{user_id}.pkl"
            if os.path.exists(face_file_path):
                os.remove(face_file_path)
                print(f"Removed face data file: {face_file_path}")
            
            # Clean up any temporary files in uploads directory
            # (Note: In a production system, you'd want to track user files more precisely)
            
            print(f"Completed file cleanup for user {user_id}")
            return True
            
        except Exception as e:
            print(f"Error cleaning up user files: {e}")
            return False
