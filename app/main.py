from fastapi import FastAPI

from app.middleware.database import DBSessionMiddleware
from app.routers import users

app = FastAPI()

app.middleware(DBSessionMiddleware)

app.include_router(users.router, prefix="/users", tags=["users"])
