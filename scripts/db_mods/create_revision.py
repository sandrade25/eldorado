#!/usr/bin/env python
import typer
from app.postgres_db import DatabaseUtils


def main(db_code: str, message: str):
    DatabaseUtils.create_revision(db_id=db_code, message=message)


if __name__ == "__main__":
    typer.run(main)
