import datetime
from functools import cached_property

from app.enums.context import ContextEnum
from app.enums.user import SessionState
from app.services.context import ContextManager
from app.utils.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    and_,
    case,
    func,
    or_,
    select,
)
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import column_property, relationship


class UserSession(Base):
    __tablename__ = "eldorado_user_session"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("eldorado_user.id", ondelete="CASCADE"), nullable=False)
    start_datetime = Column(DateTime(timezone=True), default=func.now())
    last_activity = Column(DateTime(timezone=True), default=func.now())
    status = Column(String, default=SessionState.active)
    is_active = column_property(
        case(
            [
                (
                    and_(
                        status.not_in([SessionState.inactivity, SessionState.logged_out]),
                        (func.now() - datetime.timedelta(minutes=5)) < last_activity,
                    ),
                    True,
                )
            ],
            else_=False,
        )
    )

    __table_args__ = (
        UniqueConstraint("user_id", "last_activity", name="user_session_activity_uc"),
    )

    user = relationship("User", back_populates="sessions")


class User(Base):
    __tablename__ = "eldorado_user"
    id = Column(BIGINT, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    birthdate = Column(DateTime, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    join_datetime = Column(DateTime(timezone=True), default=func.now())
    most_recent_session_id: int = column_property(
        select(UserSession.id)
        .select_from(UserSession)
        .where(UserSession.user_id == id)
        .order_by(UserSession.last_activity.desc())
        .limit(1)
        .correlate_except(UserSession)
        .scalar_subquery()
    )

    sessions = relationship("UserSession", back_populates="user")
    user = relationship("UserRole", back_populates="user")
