#!/usr/bin/env python3
"""
The auth.py module defines a base class for handling authentication,
in a Flask application.
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Implement class Auth """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths """
        return False

    def authorization_header(self, request=None) -> str:
        """returns None - request"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request"""
        return None

