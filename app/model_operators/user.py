from app.models.user import User
from app.postgres_db import DatabaseSession
from app.schemas.user import UserCreate, UserCreateBase, UserUpdateBase


class UserOperator:
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
