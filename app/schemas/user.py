import datetime as dt
from typing import List, Optional

import arrow
from app.enums.user import SessionState
from app.schemas.permissions import PermissionsBase, RolesBase
from pydantic import BaseModel, validator


class UserSession(BaseModel):
    id: int
    start_datetime: dt.datetime
    last_activity: dt.datetime
    status: SessionState
    is_active: bool


class UserId(BaseModel):
    id: int


class UserLessData(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    birthdate: Optional[dt.date]
    email: str


class UserBaseData(UserLessData):
    is_deleted: bool
    join_datetime: dt.datetime


class UserFullData(UserBaseData, UserId):
    pass


class UserExtendedData(UserFullData):
    most_recent_session: Optional[UserSession]


class UserCreateBase(UserLessData):
    password: str
    roles: List[RolesBase]
    permissions: List[PermissionsBase]


class UserCreate(BaseModel):
    users: List[UserCreateBase]


class UserUpdateBase(UserId, UserLessData):
    pass


class UserUpdate(BaseModel):
    users: List[UserUpdateBase]


class UserDeleteBase(UserId):
    hard_delete: bool = False


class UserDelete(BaseModel):
    users: List[UserDeleteBase]
