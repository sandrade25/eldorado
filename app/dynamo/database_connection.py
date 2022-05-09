import arrow
from app.dynamo.base_classes import BaseMeta
from pynamodb.attributes import (
    BooleanAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.models import Model


class DatabaseConnection(Model):
    class Meta(BaseMeta):
        table_name = "database_connection"

    db_identifier = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute()
    password = UnicodeAttribute()
    host = UnicodeAttribute()
    port = UnicodeAttribute()

    live = BooleanAttribute(default=True)
    maintainence = BooleanAttribute(default=False)

    date_created = UTCDateTimeAttribute(default=arrow.utcnow().datetime)


if not DatabaseConnection.exists():
    DatabaseConnection.create_table(wait=True)
