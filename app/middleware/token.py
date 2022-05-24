from app.services.context import ContextEnum, ContextManager
from app.utils.authentication import AuthUtils
from starlette.middleware.base import BaseHTTPMiddleware


class TokenContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        headers = request.headers
        token = headers.get("token", None)

        if token:
            decoded_token = AuthUtils.decode_token(token=token)
            ContextManager.set(ContextEnum.decoded_token, decoded_token)
        else:
            ContextManager.create_empty_context(ContextEnum.decoded_token)

        # call route
        return await call_next(request)
