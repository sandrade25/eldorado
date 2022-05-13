from app.postgres_db import DatabaseSession

from alembic import command, config, script
from alembic.runtime import migration


def upgrade_db(schema: str, revision: str = "head") -> None:
    db = DatabaseSession(schema)
    print(db.db_url)
    db.db_data.maintenance_mode = True
    db.db_data.save()
    _config = config.Config("/var/www/eldorado/app/alembic.ini")
    _config.set_main_option("sqlalchemy.url", db.db_url)
    with db.engine.begin() as cnxn:
        _config.attributes["connection"] = cnxn
        _config.attributes["schema"] = schema.lower()
        command.upgrade(_config, revision)
        db.db_data.maintenance_mode = False
        db.db_data.save()


def downgrade_db(schema: str, revision: str) -> None:
    db = DatabaseSession(schema)
    db.db_data.maintenance_mode = True
    db.db_data.save()
    _config = config.Config("/var/www/eldorado/app/alembic.ini")

    with db.engine.begin() as cnxn:
        _config.attributes["connection"] = cnxn
        _config.attributes["schema"] = schema.lower()

        command.downgrade(_config, revision)
        db.db_data.maintenance_mode = False
        db.db_data.save()


def create_revision(schema: str, message: str) -> None:
    db = DatabaseSession(schema)
    _config = config.Config("/var/www/eldorado/app/alembic.ini")

    with db.engine.begin() as cnxn:
        _config.attributes["connection"] = cnxn
        _config.attributes["schema"] = schema.lower()

        command.revision(_config, message=message, autogenerate=True)


def check_is_migrated(schema: str) -> None:
    db = DatabaseSession(schema)
    _config = config.Config("/var/www/eldorado/app/alembic.ini")
    _script = script.ScriptDirectory.from_config(_config)

    with db.engine.begin() as cnxn:
        context = migration.MigrationContext.configure(cnxn)
        return context.get_current_revision() == _script.get_current_head()


def get_current_revision(schema: str) -> None:
    db = DatabaseSession(schema)

    with db.engine.begin() as cnxn:
        context = migration.MigrationContext.configure(cnxn)
        return context.get_current_revision()
