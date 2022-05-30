from typing import List

from app.services.context import ContextEnum, ContextManager
from app.services.user import UserService
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_user_service_from_context():
    return ContextManager.get(ContextEnum.user_service, None)


def user_has_permissions(
    permission_names_list: List[str],
    user_service: UserService = Depends(get_user_service_from_context),
):
    if not user_service:
        raise HTTPException(status_code=403, detail="User not logged in")

    permission_names = user_service.permission_names

    res = any(item in permission_names_list for item in permission_names)

    if not res:
        raise HTTPException(status_code=403, detail="User does not have the required permissions")

    else:
        return True
