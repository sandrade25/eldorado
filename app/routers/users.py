from app.middleware.database import get_db_context
from app.middleware.user import get_user_context
from app.models.user import User
from app.postgres_db import DatabaseSession
from app.services.user import UserService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/",
    tags=["Users"],
)
async def user_list(
    # current_user: User = Depends(get_current_active_user),
):
    db: DatabaseSession = get_db_context()
    user_service: UserService = get_user_context()
    return {"user_service": user_service, "db": db}
