from app.dynamo.database_connection import DatabaseConnection
from app.postgres_db import DatabaseSession, DatabaseUtils
from app.settings import POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER


def main():
    db_model = DatabaseConnection(
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db_name=POSTGRES_USER,
    )

    db = DatabaseSession(schema=db_model.schema, public_schema=True)
    db.add_new_schema(db_model=db_model)


if __name__ == "__main__":
    main()
