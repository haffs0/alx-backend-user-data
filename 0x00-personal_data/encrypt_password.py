#!/usr/bin/env python3
"""A module for encrypting passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Password hashing using random salt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))


def is_valid(hashed_password: bytes, password: str) -> bool:
    """check if is a valid password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
