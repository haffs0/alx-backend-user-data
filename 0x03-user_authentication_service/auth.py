#!/usr/bin/env python3
"""Hash module"""
import bcrypt
import uuid

from sqlalchemy.orm.exc import NoResultFound
from typing import Union

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """return hash salt password"""
    salt = bcrypt.gensalt(rounds=16)
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """generate uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """check if is a valid user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                        password.encode('utf-8'),
                        user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create session ID"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """retrive a user base on session_id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """delete session_id"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """reset token"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """update user password"""
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        self._db.update_user(
                    user.id,
                    hashed_password=_hash_password(password),
                    reset_token=None
        )
        return None
