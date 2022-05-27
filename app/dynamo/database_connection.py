from uuid import uuid4

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

    def _ensure_unique_values(
        self,
        schema: str = None,
        username: str = None,
        password: str = None,
        db_name: str = None,
    ):
        self.schema = schema if schema else "{}".format(uuid4().hex[:5])
        self.username = username if username else "eldorado-{}".format(uuid4().hex[:12])
        self.password = password if password else "eldorado-{}".format(uuid4().hex)
        self.db_name = db_name if db_name else "eldorado-{}".format(uuid4().hex[:12])

    def save(self, *args, **kwargs):
        self._ensure_unique_values(
            schema=self.schema,
            username=self.username,
            password=self.password,
            db_name=self.db_name,
        )
        super().save(*args, **kwargs)

    @property
    def url(self):
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


if not DatabaseConnection.exists():
    DatabaseConnection.create_table(wait=True)
