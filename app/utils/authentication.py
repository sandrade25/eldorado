import base64
from typing import Dict

import arrow
from app.enums.user import SessionState
from app.models.user import User, UserSession
from app.postgres_db import DatabaseSession
from app.services.user import UserService
from app.settings import JWT_ALGORITHM, JWT_SIGNATURE
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
    def decode_token(token: str):
        return jwt.decode(token, JWT_SIGNATURE, algorithms=[JWT_ALGORITHM])

    @staticmethod
    def get_user_by_token(
        db: DatabaseSession,
        token: str,
        bypass_expiration: bool = False,
        update_session: bool = True,
    ):

        data = AuthUtils.decode_token(token)

        expiration = data.get("expiration")
        schema = data.get("schema")

        _now = arrow.utcnow()

        if db.schema != schema or (arrow.get(expiration) < _now and not bypass_expiration):
            raise Exception

        user_service = UserService(db, data.get("user_id"))
        if update_session:
            user_service.update_session()

        return user_service

    @staticmethod
    def generate_user_token(
        schema: str, user: User, valid_days: int = 5, data: Dict = {}, base_64: bool = True
    ):
        return AuthUtils.encode_token(
            {
                "schema": schema,
                "user_id": user.id,
                "expiration": arrow.utcnow().shift(days=valid_days).datetime,
            },
            base_64,
        )
