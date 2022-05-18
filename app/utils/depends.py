from typing import Tuple

from app.middleware.database import db_context
from app.models.user import User, UserSession
from app.postgres_db import DatabaseSession
from app.settings import (DEVELOPMENT_MODE, JWT_ALGORITHM, JWT_SIGNATURE,
                          PASSWORD_CONTEXT)
from fastapi import Depends, Security
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_user_by_token(
    token: str = Depends(oauth_scheme),
) -> User:
    # decode token
    # get user and most recent session, that is still active (last activity < 5min ago) from database
    # return (None, None) if not found.
    # return (user, session) or (user, None)
    pass


async def get_current_active_user(
    user_data: Tuple[User, UserSession] = Depends(get_user_by_token)
):
    current_user: User, user_session: UserSession = user_data
    if current_user:
        # update user session.last_activity or create new session if None returned
        # update user data as needed.
        user_session.last_activity = arrow.utcnow().datetime
        
        return current_user
    else:
        raise HTTPException(status_code=401, detail="Login Required")
