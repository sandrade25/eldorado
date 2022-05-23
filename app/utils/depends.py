from typing import Tuple

from app.middleware.database import db_context
from app.models.user import User, UserSession
from app.postgres_db import DatabaseSession
from app.settings import DEVELOPMENT_MODE, JWT_ALGORITHM, JWT_SIGNATURE, PASSWORD_CONTEXT
from app.utils.authentication import AuthUtils
from fastapi import Depends, Security
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

# NOT IN USE.
# async def get_user_by_token(
#     token: str = Depends(oauth_scheme),
# ) -> User:
#     db = db_context.get()
#     return AuthUtils.get_user_by_token(db, token)
