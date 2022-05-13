#!/usr/bin/env python
import typer
from app.alembic.migrations import upgrade_db
from app.dynamo.database_connection import DatabaseConnection
from app.postgres_db import DatabaseUtils


def main(schema: str, revision: str = "head"):
    # db_model = DatabaseConnection.get(schema)
    # DatabaseUtils.upgrade_db(db_model=db_model, revision=revision)
    upgrade_db(schema)


if __name__ == "__main__":
    typer.run(main)
