from enum import Enum


class SessionState(str, Enum):
    active = "active"
    inactivity = "inactive"
    logout = "logged_out"
