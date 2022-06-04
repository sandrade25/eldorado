#!/usr/bin/env python
import typer
from app.dynamo.database_connection import DatabaseConnection
from app.postgres_db import DatabaseUtils


def main(db_schema: str, message: str):
    db_model = DatabaseConnection.get(db_schema)
    DatabaseUtils.create_revision(db_model=db_model, message=message)


if __name__ == "__main__":
    typer.run(main)
