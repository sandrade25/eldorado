from fastapi import APIRouter, FastAPI

from app.middleware.database import DBSessionMiddleware
from app.middleware.token import TokenContextMiddleware
from app.middleware.user import UserContextMiddleware
from app.routers import authentication, users

app = FastAPI()

# middleware

app.add_middleware(UserContextMiddleware)
app.add_middleware(DBSessionMiddleware)
app.add_middleware(TokenContextMiddleware)


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
app.include_router(authentication.router, prefix="/authentication", tags=["authentication"])
