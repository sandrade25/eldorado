from dataclasses import dataclass

@dataclass
class MongoTest:
    __collection__ : str
    id: int
    test_field: int
    test_field2: float
