import arrow
from app.models.user import User
from app.postgres_db import DatabaseSession
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
        "users": db.session.execute(select(User)).all(),
    }


@router.post(
    "/create",
    tags=["users"],
)
async def create_user():
    db: DatabaseSession = ContextManager.get(ContextEnum.db)
    new_user = User(
        first_name="new_user_first_name",
        last_name="new_user_last_name",
        birthdate=arrow.utcnow().datetime,
        email="test@example.com",
        password="password",
        is_deleted=False,
        join_datetime=arrow.utcnow().datetime,
    )

    db.session.add(new_user)
    db.session.commit()

    return {}
