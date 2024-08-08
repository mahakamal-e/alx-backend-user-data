#!/usr/bin/env python3
""" SessionExpAuth Module """
from datetime import datetime, timedelta
from .session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    def __init__(self) -> None:
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
        """Gets user_id of a specific session"""
        if not session_id or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        session_created_at = session_dict.get('created_at')

        if not session_created_at:
            return None

        if not self.is_session_expired(session_created_at):
            return None

        return session_dict.get('user_id')

    def is_session_expired(self, created_at):
        """Checks if a session is expired"""
        if self.session_duration <= 0:
            return True

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        return expiration_time >= datetime.now()
