from enum import Enum


class SessionStaleReason(str, Enum):
    active = "active"
    inactivity = "inactivity"
    logout = "logout"
