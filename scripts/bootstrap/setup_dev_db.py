from app.dynamo.database_connection import DatabaseConnection
from app.postgres_db import DatabaseConnection, DatabaseUtils
from app.settings import POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, POSTRGES_HOST


def main():
    db_model = DatabaseConnection(
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTRGES_HOST,
        port=POSTGRES_PORT,
        db_name=POSTGRES_USER,
    )
    db_model.save()

    DatabaseUtils.upgrade_db(schema=db_model.schema)


if __name__ == "__main__":
    main()
