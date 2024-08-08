#!/usr/bin/env python3
""" SessionExpAuth Module """
from datetime import datetime, timedelta
from .session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    def __init__(self):
        """Initialize SessionExpAuth with session duration."""
        super().__init__()
        self.session_duration = 0
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with expiration."""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user_id for a given session_id, considering expiration."""
        if not session_id:
            return None
        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return None
        if self.session_duration <= 0:
            return session['user_id']
        created_at = session.get('created_at')
        if not created_at:
            return None
        if datetime.now() > created_at + timedelta(seconds=self.session_duration):
            del self.user_id_by_session_id[session_id]
            return None
        return session['user_id']
