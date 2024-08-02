#!/usr/bin/env python3
""" encrypt_password module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Reaturns a hash password """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ To check that the provided password matches the hash password"""
    return bcrypt.checkpw(password.encode(), hashed_password)
