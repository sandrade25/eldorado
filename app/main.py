from fastapi import APIRouter, FastAPI

from app.middleware.database import DBSessionMiddleware
from app.middleware.user import UserContextMiddleware
from app.routers import users

app = FastAPI()

# middleware
app.add_middleware(DBSessionMiddleware)
app.add_middleware(UserContextMiddleware)


router = APIRouter()


# welcome endpoint
@router.get(
    "/",
    tags=["welcome", "status"],
)
async def welcome():
    return {"status": "Ok", "message": "Welcome!"}


# additional routers
app.include_router(router)
app.include_router(users.router, prefix="/users", tags=["users"])
