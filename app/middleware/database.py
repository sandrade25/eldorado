from contextvars import ContextVar
from typing import Any

from app.postgres_db import DatabaseSession
from app.services.context import ContextManager
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        headers = request.headers
        schema = headers.get("schema", None)

        if schema in ["null", ""]:
            schema = None

        # if schema provided, try to connect to db and add to context
        if schema:
            try:
                db = DatabaseSession(schema)

                # add db to contextvars to be accessed by route.
                ContextManager.set(db)

                # call route
                response = await call_next(request)
                return response

            except Exception as exc:
                return Response(content=f"Exception: {exc.args[0]}", status_code=500)

        else:
            # if no schema provided, assume route doesnt need it.
            # let route throw exception and handle it here to return a 500.
            try:
                response = await call_next(request)
                return response
            except Exception:
                return Response(content="Unexpected error occurred", status_code=500)