from app.settings import DYNAMO_HOST, DYNAMO_PORT


class BaseMeta:
    """
    Base meta class for dynamo models.
    to avoid having to specify common meta data.
    """

    host = f"http://{DYNAMO_HOST}:{DYNAMO_PORT}"
    write_capacity_units = 10
    read_capacity_units = 250
