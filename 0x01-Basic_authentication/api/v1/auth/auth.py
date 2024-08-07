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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')
            if excluded_path.endswith('*'):
            # Remove the '*' for prefix matching
            excluded_prefix = excluded_path[:-1]
            if path.startswith(excluded_prefix):
                return False
            else:
                if (path == excluded_path or 
                    path.startswith(excluded_path + '/')):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None - request"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if not header:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request"""
        return None
