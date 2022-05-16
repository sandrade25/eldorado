from typing import Optional

import typer
from app.dynamo.database_connection import DatabaseConnection
from app.postgres_db import DatabaseSession
from app.settings import POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER


def main(first_revision: Optional[bool] = False):
    db_model = DatabaseConnection(
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db_name=POSTGRES_USER,
    )
    db_model.save()

    db = DatabaseSession(schema=db_model.schema, public_schema=True)
    if first_revision:
        db.create_revision(message="first_revision")

    db.add_new_schema(db_model=db_model)


if __name__ == "__main__":
    typer.run(main)
