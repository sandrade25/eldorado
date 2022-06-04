import typer
from app.model_operators.permissions import PermissionsOperator
from app.model_operators.user import UserOperator
from app.postgres_db import DatabaseSession
from app.schemas.user import UserCreate, UserCreateBase
from faker import Faker


def main(db_schema: str = "0123a", user_count: int = 5):
    faker = Faker()

    db = DatabaseSession(db_schema=db_schema)
    PermissionsOperator.create_base_permissions(db)

    # create users
    users_to_create = UserCreate(users=[])
    for i in range(user_count):
        first_name = faker.first_name()
        last_name = faker.last_name()

        users_to_create.users.append(
            UserCreateBase(
                first_name=first_name,
                last_name=last_name,
                birthdate=faker.date_of_birth(minimum_age=13),
                email=f"{first_name}.{last_name}@example.com",
                password="password",
            )
        )

    UserOperator.batch_create(db, users_to_create, commit=True)

    # randomly assign them permissions


if __name__ == "__main__":
    typer.run(main)
