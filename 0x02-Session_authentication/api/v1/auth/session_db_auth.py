#!/usr/bin/env python3
""" SessionDBAuth Module """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class that manages session storage in the database """

    def create_session(self, user_id=None):
        """Create and store a new session instance"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user_id by requesting UserSession in the database"""
        if not session_id or not isinstance(session_id, str):
            return None
        try:
            # Retrieve the UserSession based on session_id
            sessions = UserSession.search({'session_id': session_id})
            if not sessions:
                return None
            user_session = sessions[0]
        except Exception:
            return None

        # Handle expiration
        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        expirationTime = created_at + timedelta(seconds=self.session_duration)
        if created_at and datetime.now() > expirationTime:
            user_session.remove()
            return None
         return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy the UserSession based on the session ID,
        from the request cookie"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        users = UserSession.search({'session_id': session_id})
        if not users:
            return False

        user = users[0]
        user.remove()
        UserSession.save_to_file()

        return True
