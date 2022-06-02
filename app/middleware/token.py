from app.services.context import ContextEnum, ContextManager
from app.utils.authentication import AuthUtils
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security.utils import get_authorization_scheme_param
from jose.exceptions import JWTError


class TokenContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        headers = request.headers
        token = headers.get("Authorization", None)

        if token:
            scheme, token = get_authorization_scheme_param(token)
            if scheme.lower() == "bearer" and token:
                try:
                    decoded_token = AuthUtils.decode_token(token=token)
                    ContextManager.set(ContextEnum.decoded_token, decoded_token)
                except JWTError:
                    ContextManager.create_empty_context(ContextEnum.decoded_token)

        else:
            ContextManager.create_empty_context(ContextEnum.decoded_token)

        # call route
        return await call_next(request)
