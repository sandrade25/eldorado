from app.services.context import ContextEnum, ContextManager

from app.utils.authentication import AuthUtils

from starlette.middleware.base import BaseHTTPMiddleware


class UserContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        db = ContextManager.get(ContextEnum.db, None)
        data = ContextManager.get(ContextEnum.decoded_token)

        if db and data:
            # get user by token
            user_service = AuthUtils.get_user_by_unhashed_token(db=db, data=data)
            # add user to context
            ContextManager.set(ContextEnum.user_service, user_service)

        else:
            ContextManager.create_empty_context(ContextEnum.user_service)

        # call route
        return await call_next(request)
