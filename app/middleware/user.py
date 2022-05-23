import traceback
from contextvars import ContextVar
from typing import Any

from app.middleware.database import db_context
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

        headers = request.headers
        db = ContextManager.get(ContextEnum.db, None)
        token = headers.get("token", None)

        if db and token:
            # get user by token
            user_service = AuthUtils.get_user_by_token(db=db, token=headers.get("token", None))
            # add user to context
            ContextManager.set(ContextEnum.user_service, user_service)

        # call route
        return await call_next(request)
