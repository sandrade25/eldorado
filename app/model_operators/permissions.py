from typing import List

from app.models.permissions import Permission, Role, RolePermission, UserPermission, UserRole
from app.models.user import User, UserSession
from app.postgres_db import DatabaseSession
from app.schemas.user import UserCreate, UserCreateBase
from app.settings import HASH_CONTEXT
from sqlalchemy import and_, case, func, null, select


class PermissionsOperator:
    @staticmethod
    def get_query_for_user_permissions_by_id(
        db: DatabaseSession,
        user_id: int,
    ):

        # role permissions
        role_permissions = (
            select(
                Permission.id.label("permission_id"),
                (True).label("permission_allowed"),
            )
            .select_from(User)
            .outerjoin(UserRole, UserRole.user_id == User.id)
            .outerjoin(Role, Role.id == UserRole.role_id)
            .outerjoin(RolePermission, RolePermission.role_id == Role.id)
            .outerjoin(Permission, Permission.id == RolePermission.permission_id)
            .where(User.id == user_id)
        )

        # direct permissions
        direct_permissions = (
            select(
                Permission.id.label("permission_id"),
                UserPermission.allowed.label("permission_allowed"),
            )
            .select_from(User)
            .outerjoin(UserPermission, UserPermission.user_id == User.id)
            .outerjoin(Permission, Permission.id == UserPermission.permission_id)
            .where(User.id == user_id)
        )

        union_sq = role_permissions.union(direct_permissions).subquery()

        return (
            select(
                Permission.id,
                Permission.name,
                case(
                    [
                        (
                            func.count(union_sq.permission_allowed).filter(
                                and_(
                                    union_sq.c.permission_allowed.is_(False),
                                    union_sq.c.permission_id == Permission.id,
                                )
                            )
                            > 0,
                            False,
                        )
                    ],
                    else_=union_sq.c.permission_allowed,
                ).label("allowed"),
            )
            .select_from(Permission)
            .join(union_sq, union_sq.c.permission_id == Permission.id)
        )
