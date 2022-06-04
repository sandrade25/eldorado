from typing import List

from app.model_operators.user import UserOperator
from app.permissions.user_crud import can_create_user, can_view_other_user_data
from app.postgres_db import DatabaseSession
from app.schemas.user import UserCreate, UserExtendedData, UserSession
from app.services.context import ContextEnum, ContextManager
from app.services.user import UserService
from app.utils.depends import get_user_service_from_context
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get(
    "/",
    tags=["users"],
    response_model=List[UserExtendedData],
    dependencies=[Depends(can_view_other_user_data)],
)
async def user_list(
    # current_user: User = Depends(get_current_active_user),
):
    db: DatabaseSession = ContextManager.get(ContextEnum.db, None)
    stmt = UserOperator.get_all_users(with_sessions=True, non_deleted=True)
    db_users = db.execute(stmt).all()

    users = []
    for user, session in db_users:
        session_data = (
            UserSession(
                id=session.id,
                start_datetime=session.start_datetime,
                last_activity=session.last_activity,
                status=session.status,
                is_active=session.is_active,
            )
            if session
            else None
        )

        users.append(
            UserExtendedData(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                birthdate=user.birthdate,
                email=user.email,
                join_datetime=user.join_datetime,
                is_deleted=user.is_deleted,
                most_recent_session=session_data,
            )
        )

    return users


@router.get(
    "/{user_id}/",
    tags=["users"],
    response_model=UserExtendedData,
)
async def get_user_by_id(
    user_id: int,
    current_user: UserService = Depends(get_user_service_from_context),
):
    if not current_user.allowed_to_view_user_info(user_id):
        raise HTTPException(status_code=403, detail="you do not have permission to view this")

    db: DatabaseSession = ContextManager.get(ContextEnum.db, None)
    results = UserOperator.get_user_by_id(
        db=db,
        user_id=user_id,
        non_deleted=False,
        include_most_recent_session=True,
        include_permissions=False,
    )

    if not results:
        raise HTTPException(status_code=404, detail="user not found")

    user, session = results

    session_data = (
        UserSession(
            id=session.id,
            start_datetime=session.start_datetime,
            last_activity=session.last_activity,
            status=session.status,
            is_active=session.is_active,
        )
        if session
        else None
    )

    return UserExtendedData(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        birthdate=user.birthdate,
        email=user.email,
        join_datetime=user.join_datetime,
        is_deleted=user.is_deleted,
        most_recent_session=session_data,
    )


@router.post("/create/", tags=["users"], dependencies=[Depends(can_create_user)])
async def create_user(
    users: UserCreate,
):
    db: DatabaseSession = ContextManager.get(ContextEnum.db)
    UserService.create_users(db, users, commit=True)

    return {}
