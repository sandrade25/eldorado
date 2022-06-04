from app.dynamo.database_connection import DatabaseConnection
from app.model_operators.user import UserOperator
from app.postgres_db import DatabaseSession
from app.schemas.authentication import LoginCredentials, LoginSuccess
from app.utils.authentication import AuthUtils
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pynamodb.exceptions import DoesNotExist

router = APIRouter()


@router.post("/login/", tags=["authentication"], response_model=LoginSuccess)
async def login(credentials: LoginCredentials):

    db_schema = credentials.db_schema
    email = credentials.email

    # check if db_schema exists
    try:
        connection: DatabaseConnection = DatabaseConnection.get(db_schema)
        if not connection.live or connection.maintenance:
            raise DoesNotExist
    except DoesNotExist:
        raise HTTPException(
            status_code=403, detail="db_schema does not exist or is otherwise unavailable."
        )

    # check if user exists
    db = DatabaseSession(db_schema)
    user = UserOperator.get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=403, detail="user not found")

    # check user password matches
    if not AuthUtils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=403, detail="password mismatch")

    return LoginSuccess(token=AuthUtils.generate_user_token(db_schema=db_schema, user=user))
