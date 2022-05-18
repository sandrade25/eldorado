from enum import Enum


class SessionState(str, Enum):
    active = "active"
    inactivity = "inactive"
    logged_out = "logged_out"
