import base64
from typing import Dict

import arrow
from app.enums.user import SessionState
from app.models.user import User, UserSession
from app.postgres_db import DatabaseSession
from app.services.user import UserService
from app.settings import HASH_CONTEXT, JWT_ALGORITHM, JWT_SIGNATURE
from jose import jwt
from sqlalchemy import select


class AuthUtils:
    @staticmethod
    def encode_token(data: Dict, base_64: bool = True):
        if base_64:
            return base64.urlsafe_b64encode(
                jwt.encode(data, JWT_SIGNATURE, algorithm=JWT_ALGORITHM).encode("utf-8")
            ).decode("ascii")
        return jwt.encode(data, JWT_SIGNATURE, algorithm=JWT_ALGORITHM).encode("utf-8")

    @staticmethod
    def decode_token(token: str, base_64: bool = True):
        if base_64:
            token = base64.urlsafe_b64decode(token)

        return jwt.decode(token, JWT_SIGNATURE, algorithms=[JWT_ALGORITHM])

    @staticmethod
    def get_user_by_hashed_token(
        db: DatabaseSession,
        token: str,
        bypass_expiration: bool = False,
        update_session: bool = True,
    ):

        data = AuthUtils.decode_token(token)

        return AuthUtils.get_user_by_unhashed_token(
            db, data, bypass_expiration=bypass_expiration, update_session=update_session
        )

    @staticmethod
    def get_user_by_unhashed_token(
        db: DatabaseSession,
        data: Dict,
        bypass_expiration: bool = False,
        update_session: bool = True,
    ):

        expiration = data.get("expiration")
        db_schema = data.get("db_schema")

        _now = arrow.utcnow()

        if db.db_schema != db_schema or (arrow.get(expiration) < _now and not bypass_expiration):
            raise Exception

        user_service = UserService(db, data.get("user_id"))
        if update_session:
            user_service.update_session()

        return user_service

    @staticmethod
    def generate_user_token(
        db_schema: str, user: User, valid_days: int = 5, data: Dict = {}, base_64: bool = True
    ):
        data.update(
            {
                "db_schema": db_schema,
                "user_id": user.id,
                "expiration": arrow.utcnow().shift(days=valid_days).isoformat(),
            }
        )
        return AuthUtils.encode_token(
            data,
            base_64,
        )

    @staticmethod
    def hash_given_string(given_str: str):
        return HASH_CONTEXT.hash(given_str)

    @staticmethod
    def verify_password(password: str, hashed_str: str) -> bool:
        if HASH_CONTEXT.verify(password, hashed_str):
            return True
        return False
