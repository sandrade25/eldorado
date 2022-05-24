from http.client import HTTPException

import arrow
from app.dynamo.database_connection import DatabaseConnection
from app.model_operators.user import UserOperator
from app.models.user import User
from app.postgres_db import DatabaseSession
from app.schemas.authentication import LoginCredentials, LoginSuccess
from app.schemas.user import UserCreate, UserDelete, UserUpdate
from app.services.context import ContextEnum, ContextManager
from app.services.user import UserService
from app.utils.authentication import AuthUtils
from fastapi import APIRouter, Depends
from pynamodb.exceptions import DoesNotExist
from sqlalchemy import select

router = APIRouter()


@router.get(
    "/",
    tags=["authentication"],
)
async def user_list(
    # current_user: User = Depends(get_current_active_user),
):
    db: DatabaseSession = ContextManager.get(ContextEnum.db)
    user_service: UserService = ContextManager.get(ContextEnum.user_service)

    if not user_service:
        return {"status": "not logged in"}

    else:
        return {
            "user": user_service.user,
            "db": db,
        }


@router.post("/login/", tags=["authentication"], response_model=LoginSuccess)
async def login(credentials: LoginCredentials):

    schema = credentials.schema
    email = credentials.email

    # check if schema exists
    try:
        connection: DatabaseConnection = DatabaseConnection.get(schema)
        if not connection.live or connection.maintenance:
            raise DoesNotExist
    except DoesNotExist:
        raise HTTPException(
            status_code=403, detail="schema does not exist or is otherwise unavailable."
        )

    # check if user exists
    db = DatabaseSession(schema)
    user = UserOperator.get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=403, detail="user not found")

    # check user password matches
    if not AuthUtils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=403, detail="password mismatch")

    return LoginSuccess(token=AuthUtils.generate_user_token(schema=schema, user=user))
