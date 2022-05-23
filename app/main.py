from fastapi import FastAPI

from app.middleware.database import DBSessionMiddleware
from app.middleware.user import UserContextMiddleware
from app.routers import users

app = FastAPI()

app.add_middleware(DBSessionMiddleware)
app.add_middleware(UserContextMiddleware)

app.include_router(users.router, prefix="/users", tags=["users"])
