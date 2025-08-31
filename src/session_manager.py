import uuid
import secrets
from datetime import datetime, timedelta
import sqlite3

class SessionManager:
    """Session management for Z-Secure authentication"""
    
    def __init__(self):
        self.sessions = {}
        self.db_path = 'zsecure.db'
        self.session_timeout = 900  # 15 minutes (900 seconds)
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_session(self, user_id, ip_address=None, user_agent=None):
        """Create a new session"""
        try:
            session_id = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(seconds=self.session_timeout)
            
            print(f"Creating session for user {user_id}, expires at {expires_at}")
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sessions (id, user_id, expires_at, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (session_id, user_id, expires_at.isoformat(), ip_address, user_agent))
            
            conn.commit()
            conn.close()
            
            print(f"Session {session_id} created successfully")
            return session_id
            
        except Exception as e:
            print(f"Error creating session: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def is_session_valid(self, session_id):
        """Check if session is valid and not expired"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id, expires_at, last_activity 
                FROM sessions 
                WHERE id = ?
            ''', (session_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                print(f"Session {session_id} not found")
                return False, None
            
            user_id, expires_at_str, last_activity = result
            expires_at = datetime.fromisoformat(expires_at_str)
            
            print(f"Session {session_id} for user {user_id}: expires at {expires_at}, current time {datetime.now()}")
            
            if datetime.now() > expires_at:
                print(f"Session {session_id} has expired")
                return False, user_id
            
            print(f"Session {session_id} is valid")
            return True, user_id
            
        except Exception as e:
            print(f"Error validating session: {e}")
            return False, None
    
    def update_session_activity(self, session_id):
        """Update session last activity and extend expiration"""
        try:
            new_expires_at = datetime.now() + timedelta(seconds=self.session_timeout)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE sessions 
                SET last_activity = CURRENT_TIMESTAMP, expires_at = ?
                WHERE id = ? AND is_active = 1
            ''', (new_expires_at.isoformat(), session_id))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error updating session activity: {e}")
            return False
    
    def invalidate_session(self, session_id):
        """Invalidate a session"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE sessions SET is_active = 0 WHERE id = ?
            ''', (session_id,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error invalidating session: {e}")
            return False
    
    def invalidate_all_user_sessions(self, user_id):
        """Invalidate all sessions for a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE sessions SET is_active = 0 WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error invalidating user sessions: {e}")
            return False
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Mark expired sessions as inactive
            cursor.execute('''
                UPDATE sessions 
                SET is_active = 0 
                WHERE expires_at < ? AND is_active = 1
            ''', (datetime.now().isoformat(),))
            
            # Delete old inactive sessions (older than 24 hours)
            old_time = datetime.now() - timedelta(hours=24)
            cursor.execute('''
                DELETE FROM sessions 
                WHERE is_active = 0 AND created_at < ?
            ''', (old_time.isoformat(),))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error cleaning up sessions: {e}")
            return False
    
    def get_session_info(self, session_id):
        """Get session information"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.*, u.email 
                FROM sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.id = ?
            ''', (session_id,))
            
            session = cursor.fetchone()
            conn.close()
            
            return dict(session) if session else None
            
        except Exception as e:
            print(f"Error getting session info: {e}")
            return None
    
    def get_active_sessions(self, user_id):
        """Get all active sessions for a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, created_at, last_activity, expires_at, ip_address, user_agent
                FROM sessions 
                WHERE user_id = ? AND is_active = 1 AND expires_at > ?
                ORDER BY last_activity DESC
            ''', (user_id, datetime.now().isoformat()))
            
            sessions = cursor.fetchall()
            conn.close()
            
            return [dict(session) for session in sessions]
            
        except Exception as e:
            print(f"Error getting active sessions: {e}")
            return []
    
    def get_session_count(self, user_id):
        """Get count of active sessions for a user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM sessions 
                WHERE user_id = ? AND is_active = 1 AND expires_at > ?
            ''', (user_id, datetime.now().isoformat()))
            
            result = cursor.fetchone()
            conn.close()
            
            return result['count'] if result else 0
            
        except Exception as e:
            print(f"Error getting session count: {e}")
            return 0
    
    def extend_session(self, session_id, additional_seconds=None):
        """Extend session by additional time"""
        try:
            if additional_seconds is None:
                additional_seconds = self.session_timeout
            
            # Get current expiration
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT expires_at FROM sessions WHERE id = ? AND is_active = 1
            ''', (session_id,))
            
            session = cursor.fetchone()
            if not session:
                conn.close()
                return False
            
            # Extend expiration
            current_expires = datetime.fromisoformat(session['expires_at'])
            new_expires = current_expires + timedelta(seconds=additional_seconds)
            
            cursor.execute('''
                UPDATE sessions SET expires_at = ? WHERE id = ?
            ''', (new_expires.isoformat(), session_id))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error extending session: {e}")
            return False
