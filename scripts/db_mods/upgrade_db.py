#!/usr/bin/env python
import typer
from app.postgres_db import DatabaseUtils


def main(schema: str, revision: str = "head"):
    DatabaseUtils.upgrade_db(schema=schema, revision=revision)


if __name__ == "__main__":
    typer.run(main)
