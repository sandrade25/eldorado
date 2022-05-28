from typing import List

from app.models.permissions import (Permission, Role, RolePermission,
                                    UserPermission, UserRole)
from app.models.user import User, UserSession
from app.postgres_db import DatabaseSession
from app.schemas.user import UserCreate, UserCreateBase
from app.settings import HASH_CONTEXT
from sqlalchemy import and_, func, null, select


class PermissionsOperator:
    @staticmethod
    def get_query_for_user_permissions_by_id(
        db: DatabaseSession,
        user_ids: List[int] = None,
    ):

        # role permissions
        role_permissions = (
            select(
                User.id.label("user_id"),
                Role.id.label("role_id"),
                Role.name.label("role_name"),
                Permission.id.label("permission_id"),
                Permission.name.label("permission_name"),
                (True).label("permission_allowed"),
            )
            .select_from(User)
            .outerjoin(UserRole, UserRole.user_id == User.id)
            .outerjoin(Role, Role.id == UserRole.role_id)
            .outerjoin(RolePermission, RolePermission.role_id == Role.id)
            .outerjoin(Permission, Permission.id == RolePermission.permission_id)
            .where(User.id.in_(user_ids))
        ).subquery()

        # direct permissions
        direct_permissions = (
            select(
                User.id.label("user_id"),
                null().label("role_id"),
                null().label("role_name"),
                Permission.id.label("permission_id"),
                Permission.name.label("permission_name"),
                UserPermission.allowed.label("permission_allowed"),
            )
            .select_from(User)
            .outerjoin(UserPermission, UserPermission.user_id == User.id)
            .outerjoin(Permission, Permission.id == UserPermission.permission_id)
            .where(User.id.in_(user_ids))
        ).subquery()


        (
            select()
            # TODO: write query that joins both role permissions and direct permissions. 
            """
            - role permissions allow a user with a role to have all the permissions associated with that role. 
                - if you want to assign a set of permissions to a user, you can use a role to do so.
            - if a user has a role that allows a permission, but then has that specific permission set to not allowed directly, 
                - the user permission takes final say. So you can assign a role of permissions, but then disallow one or two permissions within that role,
                on a specific user.


                SEE TRELLO FOR DETAILS
            
            """
        )
