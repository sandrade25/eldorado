from app.enums.context import ContextEnum
from app.postgres_db import DatabaseSession
from app.services.context import ContextManager
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        headers = request.headers
        token = ContextManager.get(ContextEnum.decoded_token)
        db_schema = None
        if token:
            db_schema = token.get("schema", None)

        if not db_schema:
            db_schema = headers.get("schema", None)

        if db_schema in ["null", ""]:
            db_schema = None

        # if db_schema provided, try to connect to db and add to context
        if db_schema:
            try:
                db = DatabaseSession(db_schema)

                # add db to contextvars to be accessed by route.
                ContextManager.set(ContextEnum.db, db)

                # call route
                response = await call_next(request)
                return response

            except Exception as exc:
                return Response(content=f"Exception: {exc.args[0]}", status_code=500)

        else:
            # if no db_schema provided, assume route doesnt need it.
            # let route throw exception and handle it here to return a 500.
            try:
                ContextManager.create_empty_context(ContextEnum.db)
                response = await call_next(request)
                return response
            except Exception:
                return Response(content="Unexpected error occurred", status_code=500)
