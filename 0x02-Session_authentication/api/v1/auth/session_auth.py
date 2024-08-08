#!/usr/bin/env python3
""" Authentication Module"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ Implement SessionAuth Class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Method that creates session """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
