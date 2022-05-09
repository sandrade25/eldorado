#!/usr/bin/env python
import typer
from app.postgres_db import DatabaseUtils


def main(db_code: str, revision: str = "head"):
    DatabaseUtils.upgrade_db(db_code=db_code, revision=revision)


if __name__ == "__main__":
    typer.run(main)
