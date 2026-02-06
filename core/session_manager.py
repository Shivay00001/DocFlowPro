"""
Session Manager - Handle user session timeout and activity tracking
"""

import time
from datetime import datetime, timedelta
from config.session_config import (
    SESSION_TIMEOUT_MINUTES,
    WARNING_TIME_MINUTES,
    SESSION_TIMEOUT_ENABLED
)
from core.logger import get_logger

logger = get_logger('app')


class SessionManager:
    """Manages user session with automatic timeout"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.timeout_minutes = SESSION_TIMEOUT_MINUTES
        self.warning_minutes = WARNING_TIME_MINUTES
        self.enabled = SESSION_TIMEOUT_ENABLED
        
        self.is_active = False
        self.user_id = None
        self.username = None
        self.last_activity = None
        self.login_time = None
    
    def start_session(self, user_id, username):
        """Start a user session"""
        self.user_id = user_id
        self.username = username
        self.is_active = True
        self.login_time = datetime.now()
        self.refresh_activity()
        
        logger.info(f"Session started for user: {username} (ID: {user_id})")
    
    def refresh_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def check_timeout(self):
        """
        Check if session has timed out
        Returns: tuple (timed_out: bool, warning: bool, remaining_seconds: int)
        """
        if not self.enabled or not self.is_active:
            return False, False, 0
        
        elapsed = datetime.now() - self.last_activity
        elapsed_seconds = elapsed.total_seconds()
        timeout_seconds = self.timeout_minutes * 60
        warning_seconds = self.warning_minutes * 60
        
        remaining_seconds = max(0, timeout_seconds - elapsed_seconds)
        
        # Check if timed out
        if elapsed_seconds >= timeout_seconds:
            logger.warning(f"Session timed out for user: {self.username}")
            return True, False, 0
        
        # Check if warning threshold reached
        if remaining_seconds <= warning_seconds:
            return False, True, int(remaining_seconds)
        
        return False, False, int(remaining_seconds)
    
    def end_session(self):
        """End the current session"""
        if self.is_active:
            logger.info(f"Session ended for user: {self.username}")
        
        self.is_active = False
        self.user_id = None
        self.username = None
        self.last_activity = None
        self.login_time = None
    
    def get_session_duration(self):
        """Get total session duration"""
        if not self.is_active or not self.login_time:
            return 0
        
        duration = datetime.now() - self.login_time
        return int(duration.total_seconds())
    
    def get_idle_time(self):
        """Get idle time in seconds"""
        if not self.is_active or not self.last_activity:
            return 0
        
        idle = datetime.now() - self.last_activity
        return int(idle.total_seconds())
    
    def get_remaining_time(self):
        """Get remaining time before timeout in seconds"""
        if not self.enabled or not self.is_active:
            return 0
        
        elapsed = datetime.now() - self.last_activity
        timeout_seconds = self.timeout_minutes * 60
        remaining = timeout_seconds - elapsed.total_seconds()
        
        return max(0, int(remaining))
    
    def extend_session(self, minutes=30):
        """Extend session by refreshing activity"""
        self.refresh_activity()
        logger.info(f"Session extended for user: {self.username}")
    
    def is_session_active(self):
        """Check if session is currently active"""
        return self.is_active
    
    def get_session_info(self):
        """Get current session information"""
        if not self.is_active:
            return None
        
        return {
            'user_id': self.user_id,
            'username': self.username,
            'login_time': self.login_time,
            'last_activity': self.last_activity,
            'duration_seconds': self.get_session_duration(),
            'idle_seconds': self.get_idle_time(),
            'remaining_seconds': self.get_remaining_time()
        }


# Global session instance
session_manager = SessionManager()

def get_session_manager():
    """Get global session manager instance"""
    return session_manager
