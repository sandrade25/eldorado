from typing import List

from app.services.context import ContextEnum, ContextManager
from app.services.user import UserService
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_user_service_from_context():
    return ContextManager.get(ContextEnum.user_service, None)


def is_logged_in():
    user = ContextManager.get(ContextEnum.user_service, None)
    if not user:
        raise HTTPException(status_code=403, detail="User must be logged in")


def user_has_permissions(
    permission_names_list: List[str],
    user_service: UserService,
):
    if not user_service:
        raise HTTPException(status_code=403, detail="User not logged in")

    permission_names = user_service.permission_names

    res = any(item in permission_names_list for item in permission_names)

    if not res:
        raise HTTPException(status_code=403, detail="User does not have the required permissions")

    else:
        return True


class Permissions:
    def __init__(self, permission_names_list: List[str]):
        self.permission_names_list = permission_names_list

    def __call__(self, user_service: UserService = Depends(get_user_service_from_context)):
        return user_has_permissions(self.permission_names_list, user_service)
