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


class Permission(Base):
    __tablename__ = "eldorado_permission"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=False)

    role_permissions = relationship("RolePermission", back_populates="permission")
    user_permissions = relationship("UserPermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = "eldorado_role_permission"
    id = Column(BIGINT, primary_key=True, index=True)
    role_id = Column(BIGINT, ForeignKey("eldorado_role.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(
        BIGINT, ForeignKey("eldorado_permission.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="role_permission_uc"),)

    permission = relationship("Permission", back_populates="role_permissions")
    role = relationship("Role", back_populates="role_permissions")


class Role(Base):
    __tablename__ = "eldorado_role"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=False)

    user_roles = relationship("UserRole", back_populates="role")
    role_permissions = relationship("RolePermission", back_populates="role")

    __table_args__ = (UniqueConstraint("name", name="rolename_uc"),)


class UserPermission(Base):
    __tablename__ = "eldorado_user_permission"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("eldorado_user.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(
        BIGINT, ForeignKey("eldorado_permission.id", ondelete="CASCADE"), nullable=False
    )
    allowed = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="permissions")
    permission = relationship("Permission", back_populates="user_permissions")

    __table_args__ = (UniqueConstraint("user_id", "permission_id", name="user_permission_uc"),)


class UserRole(Base):
    __tablename__ = "eldorado_user_role"
    id = Column(BIGINT, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey("eldorado_user.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(BIGINT, ForeignKey("eldorado_role.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="user_roles")

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="user_role_uc"),)
