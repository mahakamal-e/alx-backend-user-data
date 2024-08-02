#!/usr/bin/env python3
""" encrypt_password module"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Reaturns a hash password """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password
