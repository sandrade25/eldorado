#!/usr/bin/env python
import typer
from app.postgres_db import DatabaseUtils


def main(schema: str, message: str):
    DatabaseUtils.create_revision(schema=schema, message=message)


if __name__ == "__main__":
    typer.run(main)
