#!/usr/bin/env python3
""" Authentication Module """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Returned hashed pawssword"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password_bytes, salt)
    return hashed_pass
