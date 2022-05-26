import arrow
from app.models.user import User
from app.postgres_db import DatabaseSession
from app.schemas.user import UserCreate, UserDelete, UserUpdate
from app.services.context import ContextEnum, ContextManager
from app.services.user import UserService
from fastapi import APIRouter, Depends
from sqlalchemy import select

router = APIRouter()


@router.get(
    "/",
    tags=["users"],
)
async def user_list(
    # current_user: User = Depends(get_current_active_user),
):
    db: DatabaseSession = ContextManager.get(ContextEnum.db)
    user_service: UserService = ContextManager.get(ContextEnum.user_service, None)
    # most_recent_session = user_service.user.most_recent_session
    return {
        "user_service": user_service.user.id,
        "db": db.db_schema,
        "users": "cant connect to db",
    }


@router.post(
    "/create",
    tags=["users"],
)
async def create_user(users: UserCreate):
    db: DatabaseSession = ContextManager.get(ContextEnum.db)
    UserService.create_users(db, users, commit=True)

    return {}
