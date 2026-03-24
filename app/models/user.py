from datetime import datetime
from typing import Optional, List
from sqlalchemy import ForeignKey, String, Boolean, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.user_dept import user_dept_table

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default="CURRENT_TIMESTAMP")

    # 新增字段
    main_dept_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"))
    direct_leader_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    position: Mapped[Optional[str]] = mapped_column(String(50))
    user_type: Mapped[Optional[str]] = mapped_column(String(20))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    updated_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now()
    )
    # role
    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("roles.id"))
    role: Mapped[Optional["Role"]] = relationship()

    # 关系
    main_dept: Mapped[Optional["Department"]] = relationship(foreign_keys=[main_dept_id])
    direct_leader: Mapped[Optional["User"]] = relationship(remote_side=[id], foreign_keys=[direct_leader_id])
    creator: Mapped[Optional["User"]] = relationship(foreign_keys=[created_by], remote_side=[id])
    updater: Mapped[Optional["User"]] = relationship(foreign_keys=[updated_by], remote_side=[id])

    # 多对多关系
    departments: Mapped[List["Department"]] = relationship(
        secondary="user_dept", back_populates="users"
    )