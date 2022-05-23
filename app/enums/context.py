from enum import Enum


class ContextEnum(Enum, str):
    db = "db"
    user_service = "user_service"
