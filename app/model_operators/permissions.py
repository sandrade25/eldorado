from app.models.permissions import Permission, Role, RolePermission, UserPermission, UserRole
from app.models.user import User
from app.permissions.enum import PermissionsEnum
from app.postgres_db import DatabaseSession
from sqlalchemy import case, func, select


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
                case([(Permission.id > 0, True)], else_=True).label("permission_allowed"),
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

        qry = (
            select(
                Permission.id.label("permission_id"),
                Permission.name.label("permission_name"),
                func.count(union_sq.c.permission_allowed)
                .filter(union_sq.c.permission_allowed.is_(False))
                .label("false_count"),
            )
            .select_from(Permission)
            .join(union_sq, union_sq.c.permission_id == Permission.id)
            .group_by(Permission.id, Permission.name)
            .where()
        ).subquery()

        return (
            select(qry.c.permission_id, qry.c.permission_name)
            .select_from(qry)
            .where(qry.c.false_count == 0)
        )

    @staticmethod
    def create_base_permissions(db: DatabaseSession):
        for data in PermissionsEnum:
            db.add(Permission(name=data.value))
        db.commit()
