from mongokit import Collection 
import datetime


class MongoTest(Document):
    __collection__ = 'test_col'
    __database__ = 'test_db'
    structure = {
        'title': str,
        'body': str,
        'author': str,
        'date_creation': datetime.datetime,
        'rank': int,
        'tags': [str],
    }
    required_fields = ['title', 'author', 'date_creation']
    default_values = {
        'rank': 0,
        'date_creation': datetime.datetime.utcnow
    }
