from app.settings import DYNAMO_HOST, DYNAMO_PORT


class BaseMeta:
    host = f"http://{DYNAMO_HOST}:{DYNAMO_PORT}"
    write_capacity_units = 10
    read_capacity_units = 250
