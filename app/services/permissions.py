from typing import List

from app.utils.depends import user_has_permissions
from starlette.requests import Request


class UserPermissionChecker:
    def __init__(self, permissions_list: List[str], for_route: bool = True):
        self.for_route = for_route
        self.permissions = permissions_list

    def __call__(self, request: Request) -> bool:
        user_has_permissions(self.permissions)
