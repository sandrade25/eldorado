from app.enums.user import SessionState
from app.postgres_db import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import relationship


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

    sessions = relationship("UserSession", back_populates="user")


class UserSession(Base):
    __tablename__ = "eldorado_user_session"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("eldorado_user.id", ondelete="CASCADE"), nullable=False)
    start_datetime = Column(DateTime(timezone=True), default=func.now())
    last_activity = Column(DateTime(timezone=True), default=func.now())
    stale_reason = Column(String, default=SessionState.active)

    user = relationship("User", back_populates="sessions")
