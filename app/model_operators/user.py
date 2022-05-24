from app.models.user import User
from app.postgres_db import DatabaseSession
from app.schemas.user import UserCreate, UserCreateBase
from sqlalchemy import select


class UserOperator:
    @staticmethod
    def get_user_by_id(db: DatabaseSession, user_id: int, non_deleted: bool = True):
        stmt = select(User).where(User.id == user_id)
        if non_deleted:
            stmt = stmt.where(User.is_deleted.is_(False))

        user = db.session.execute(stmt).scalar_one_or_none()
        return user

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
                first_name=UserCreateBase.first_name,
                last_name=UserCreateBase.last_name,
                birthdate=UserCreateBase.birthdate,
                email=UserCreateBase.email,
                password=UserCreateBase.password,
            )
        )

        if commit:
            db.commit()

    @staticmethod
    def batch_create(db: DatabaseSession, users: UserCreate, commit: bool = False):
        for user in users.users:
            UserOperator.create(db=db, user=user, commit=False)

        if commit:
            db.commit()
