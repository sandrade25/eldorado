"""
TODO: Delete this file!!!
"""

from app.dynamo.base_classes import BaseMeta
from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model


class TestModel(Model):
    class Meta(BaseMeta):
        table_name = "TestTable"

    field_1 = UnicodeAttribute(hash_key=True)
    field_2 = NumberAttribute()


if not TestModel.exists():
    TestModel.create_table(wait=True)
