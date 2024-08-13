#!/usr/bin/env python3
""" Authentication Module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Saved the user to the database after hashing password."""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
            return user

    def valid_login(self, email, password) -> bool:
        """returrs true if password match with email"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False


def _hash_password(password: str) -> bytes:
    """ Returned hashed pawssword"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password_bytes, salt)
    return hashed_pass
