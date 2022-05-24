from enum import Enum


class ContextEnum(str, Enum):
    db = "db"
    user_service = "user_service"
    decoded_token = "decoded_token"
