from app.settings import DYNAMO_HOST, DYNAMO_PORT

class BaseMeta:
    host = f"{DYNAMO_HOST}:{DYNAMO_PORT}"