import datetime as dt
from typing import List, Optional

import arrow
from app.enums.user import SessionState
from pydantic import BaseModel, validator


class RolesBase:
    role_id: int
    role_allowed: bool


class PermissionsBase:
    permission_id: int
    permission_allowed: bool
