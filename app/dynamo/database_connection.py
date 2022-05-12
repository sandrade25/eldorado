import arrow
from app.dynamo.base_classes import BaseMeta
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class DatabaseConnection(Model):
    class Meta(BaseMeta):
        table_name = "database_connection"

    schema = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute()
    password = UnicodeAttribute()
    host = UnicodeAttribute()
    port = UnicodeAttribute()
    db_name = UnicodeAttribute()

    live = BooleanAttribute(default=True)
    maintenance = BooleanAttribute(default=False)

    date_created = UTCDateTimeAttribute(default=arrow.utcnow().datetime)


if not DatabaseConnection.exists():
    DatabaseConnection.create_table(wait=True)
