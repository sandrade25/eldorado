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
    user_service: UserService = ContextManager.get(ContextEnum.user_service)
    return {
        "user_service": user_service,
        "db": db,
        "users": db.session.execute(select(User)).all() if db else "cant connect to db",
    }


@router.post(
    "/create",
    tags=["users"],
)
async def create_user(users: UserCreate):
    db: DatabaseSession = ContextManager.get(ContextEnum.db)
    UserService.create_users(db, users, commit=True)

    return {}
