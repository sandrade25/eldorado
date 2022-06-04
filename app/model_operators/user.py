from typing import List

from app.model_operators.permissions import PermissionsOperator
from app.models.user import User, UserSession
from app.postgres_db import DatabaseSession
from app.schemas.user import UserCreate, UserCreateBase
from app.settings import HASH_CONTEXT
from sqlalchemy import func, select


class UserOperator:
    @staticmethod
    def get_user_by_id(
        db: DatabaseSession,
        user_id: int,
        non_deleted: bool = True,
        include_most_recent_session: bool = True,
        include_permissions: bool = True,
    ):
        if include_most_recent_session:
            stmt = (
                select(User, UserSession)
                .select_from(User)
                .outerjoin(UserSession, UserSession.id == User.most_recent_session_id)
            )
        else:
            stmt = select(User)

        stmt = stmt.where(User.id == user_id)

        if non_deleted:
            stmt = stmt.where(User.is_deleted.is_(False))

        if include_permissions:
            permissions_sq = PermissionsOperator.get_query_for_user_permissions_by_id(
                db, user_id=user_id
            ).subquery()
            stmt = stmt.add_columns(
                func.array(select(permissions_sq.c.permission_id).subquery()).label(
                    "permission_ids"
                ),
                func.array(select(permissions_sq.c.permission_name).subquery()).label(
                    "permission_name"
                ),
            )

        if include_most_recent_session or include_permissions:
            return db.session.execute(stmt).one()
        return db.session.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_user_by_email(db: DatabaseSession, email: str, non_deleted: bool = True):
        stmt = select(User).where(User.email == email)
        if non_deleted:
            stmt = stmt.where(User.is_deleted.is_(False))

        user = db.session.execute(stmt).scalar_one_or_none()
        return user

    @staticmethod
    def create(db: DatabaseSession, user: UserCreateBase, commit: bool = False):
        db.add(
            User(
                first_name=user.first_name.lower(),
                last_name=user.last_name.lower(),
                birthdate=user.birthdate,
                email=user.email.lower(),
                password=HASH_CONTEXT.hash(user.password),
            )
        )

        if commit:
            db.commit()

    @staticmethod
    def batch_create(
        db: DatabaseSession, users: UserCreate, skip_emails: List[str] = [], commit: bool = False
    ):
        for user in users.users:
            if user.email.lower() not in skip_emails:
                UserOperator.create(db=db, user=user, commit=False)

        if commit:
            db.commit()

    @staticmethod
    def get_all_users(with_sessions: bool = False, non_deleted: bool = True):
        stmt = select(User)

        if with_sessions:
            stmt = stmt.add_columns(UserSession).outerjoin(
                UserSession, UserSession.id == User.most_recent_session_id
            )

        if non_deleted:
            stmt = stmt.where(User.is_deleted.is_(False))

        return stmt
