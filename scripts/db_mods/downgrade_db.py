#!/usr/bin/env python
import typer
from app.alembic.migrations import downgrade_db


def main(db_schema: str, revision: str = "head"):
    # db_model = DatabaseConnection.get(db_schema)
    # DatabaseUtils.upgrade_db(db_model=db_model, revision=revision)
    downgrade_db(db_schema, revision)


if __name__ == "__main__":
    typer.run(main)
