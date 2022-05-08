from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from app.dynamo.base_classes import BaseMeta

class TestModel(Model):
    class Meta(BaseMeta)