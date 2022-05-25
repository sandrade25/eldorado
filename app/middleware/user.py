import traceback
from contextvars import ContextVar
from typing import Any

from app.models.user import User
from app.postgres_db import DatabaseSession
from app.services.context import ContextEnum, ContextManager
from app.services.user import UserService
from app.settings import ENVIRONMENT
from app.utils.authentication import AuthUtils
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware


class UserContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        db = ContextManager.get(ContextEnum.db, None)
        token = ContextManager.get(ContextEnum.decoded_token)

        if db and token:
            # get user by token
            user_service = AuthUtils.get_user_by_unhashed_token(db=db, token=token)
            # add user to context
            ContextManager.set(ContextEnum.user_service, user_service)

        else:
            ContextManager.create_empty_context(ContextEnum.user_service)

        # call route
        return await call_next(request)
