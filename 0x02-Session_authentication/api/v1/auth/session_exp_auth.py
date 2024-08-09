#!/usr/bin/env python3
"""Defines session_exp_auth module"""

from .session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """Implement SessionExpAuth class"""
    def __init__(self) -> None:
        super().__init__()
        self.session_duration = int(os.environ.get('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """Creates a session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets user_id of a specific session"""
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
        expirationTime = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expirationTime:
            del self.user_id_by_session_id[session_id]
            return None
        return session['user_id']
